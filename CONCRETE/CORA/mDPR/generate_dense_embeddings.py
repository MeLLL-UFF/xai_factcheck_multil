import os
import pathlib

import argparse
import csv
import logging
import pickle
from typing import List, Tuple
import charamel

import numpy as np
from glob import glob
import torch
from torch import nn

from dpr.models import init_biencoder_components
from dpr.options import add_encoder_params, setup_args_gpu, print_args, set_encoder_params_from_state, \
    add_tokenizer_params, add_cuda_params
from dpr.utils.data_utils import Tensorizer
from dpr.utils.model_utils import add_missing_position_ids, setup_for_distributed_mode, get_model_obj, load_states_from_checkpoint,move_to_device

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if (logger.hasHandlers()):
    logger.handlers.clear()
console = logging.StreamHandler()
logger.addHandler(console)

def gen_ctx_vectors(ctx_rows: List[Tuple[object, str, str]], model: nn.Module, tensorizer: Tensorizer,
                    insert_title: bool = True) -> List[Tuple[object, np.array]]:
    n = int(len(ctx_rows))
    bsz = int(args.batch_size)
    total = 0
    results = []
    for _, batch_start in enumerate(range(0, n, bsz)):

        batch_token_tensors = [tensorizer.text_to_tensor(ctx[1], title=ctx[2] if insert_title else None) for ctx in
                               ctx_rows[batch_start:batch_start + bsz]]

        ctx_ids_batch = move_to_device(torch.stack(batch_token_tensors, dim=0),args.device)
        ctx_seg_batch = move_to_device(torch.zeros_like(ctx_ids_batch),args.device)
        ctx_attn_mask = move_to_device(tensorizer.get_attn_mask(ctx_ids_batch),args.device)
        with torch.no_grad():
            _, out, _ = model(ctx_ids_batch, ctx_seg_batch, ctx_attn_mask)
        out = out.cpu()

        ctx_ids = [r[0] for r in ctx_rows[batch_start:batch_start + bsz]]

        assert len(ctx_ids) == out.size(0)

        total += len(ctx_ids)

        results.extend([
            (ctx_ids[i], out[i].view(-1).numpy())
            for i in range(out.size(0))
        ])

        if total % 10 == 0:
            logger.info('Encoded passages %d', total)

    return results


def main(args):
    saved_state = load_states_from_checkpoint(args.model_file)
    set_encoder_params_from_state(saved_state.encoder_params, args)
    print_args(args)
    
    tensorizer, encoder, _ = init_biencoder_components(args.encoder_model_type, args, inference_only=True)

    encoder = encoder.ctx_model

    encoder, _ = setup_for_distributed_mode(encoder, None, args.device, args.n_gpu,
                                            args.local_rank,
                                            args.fp16,
                                            args.fp16_opt_level)
    encoder.eval()
    saved_state
    # load weights from the model file
    model_to_load = get_model_obj(encoder)
    logger.info('Loading saved model state ...')
    logger.debug('saved model keys =%s', saved_state.model_dict.keys())

    prefix_len = len('ctx_model.')
    ctx_state = {key[prefix_len:]: value for (key, value) in saved_state.model_dict.items() if
                 key.startswith('ctx_model.')}
    
    ctx_state = add_missing_position_ids(ctx_state)

    model_to_load.load_state_dict(ctx_state)

    logger.info('reading data from file=%s', args.ctx_file)
    # logger.info('ignore shards.')
    language = args.out_file.split('emb_')[-1].split('.pkl')[0]
    print(language)
    # the id and the title are dummy
    # rows = [(f'{language}-{idx}','',open(f,'r').read()) for idx, f in enumerate(sorted(glob(os.path.join(args.ctx_file,'*.txt'))))]
    
    # rows = [(f'{language}-{idx}','',open(f,'r').read().split('<sep>')[1]) for idx, f in enumerate(sorted(glob(os.path.join(args.ctx_file,'*.txt'))))]
    txt_files = sorted(glob(os.path.join(args.ctx_file, '*.txt')))

    rows = []
    for idx, file_path in enumerate(txt_files):
        with open(file_path, 'rb') as file:
            detector = charamel.Detector()
            result = detector.detect(file.read())
            file.close()
        # Lê o conteúdo do arquivo
        with open(file_path, 'r', encoding=result.value, errors='ignore') as file:
            file_content = file.read()
    
        parts = file_content.split('<sep>')
    
        if len(parts) > 1:
            content_after_sep = parts[1]
        else:
            content_after_sep = ''
    
    # Adiciona a tupla à lista
        rows.append((f'{language}-{idx}', '', content_after_sep))

    logger.info(f'read {len(rows)} passages')
    # rows = []
    # with open(args.ctx_file) as tsvfile:
    #     reader = csv.reader(tsvfile, delimiter='\t')
    #     # file format: doc_id, doc_text, title
    #     rows.extend([(row[0], row[1], row[2]) for row in reader if row[0] != 'id'])

    shard_size = int(len(rows) / int(args.num_shards))
    start_idx = args.shard_id * shard_size
    end_idx = start_idx + shard_size

    logger.info('Producing encodings for passages range: %d to %d (out of total %d)', start_idx, end_idx, len(rows))
    rows = rows[start_idx:end_idx]

    data = gen_ctx_vectors(rows, encoder, tensorizer, True)

    file = args.out_file #+ '_' + str(args.shard_id)
    pathlib.Path(os.path.dirname(file)).mkdir(parents=True, exist_ok=True)
    logger.info('Writing results to %s' % file)
    with open(file, mode='wb') as f:
        pickle.dump(data, f)

    logger.info('Total passages processed %d. Written to %s', len(data), file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    add_encoder_params(parser)
    add_tokenizer_params(parser)
    add_cuda_params(parser)

    parser.add_argument('--ctx_file', type=str, default=None, help='Path to passages set .tsv file')
    parser.add_argument('--out_file', required=True, type=str, default=None,
                        help='output .tsv file path to write results to ')
    parser.add_argument('--shard_id', type=int, default=0, help="Number(0-based) of data shard to process")
    parser.add_argument('--num_shards', type=int, default=1, help="Total amount of data shards")
    parser.add_argument('--batch_size', type=int, default=32, help="Batch size for the passage encoder forward pass")
    args = parser.parse_args()

    assert args.model_file, 'Please specify --model_file checkpoint to init model weights'

    setup_args_gpu(args)

    main(args)