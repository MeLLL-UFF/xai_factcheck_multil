from torch.utils.data import DataLoader
import argparse
import torch
import numpy as np
import json
import random
import time
import os

from model import BERTModelForClassification
from data import PropaFakeDataset
from constants import XFACT_LABEL2IDX, XFACT_IDX2LABEL
from xfact_eval import calculate_fscore
from utils import read_data

seed = 42
# fix random seed
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.backends.cudnn.enabled = False


# configuration
parser = argparse.ArgumentParser()
parser.add_argument('--max_sequence_length', default=512, type=int)
parser.add_argument('--model_name', default='bert-base-multilingual-cased')
parser.add_argument('--warmup_epoch', default=5, type=int)
parser.add_argument('--max_epoch', default=30, type=int)
parser.add_argument('--eval_batch_size', default=10, type=int)
parser.add_argument('--n_candidates', default=5, type=int)
parser.add_argument('--n_classes', default=7, type=int)
parser.add_argument('--dataset', default='x-fact', type=str)
parser.add_argument('--test_path', required=True)
parser.add_argument('--checkpoint_path', required=True)
parser.add_argument('--retrieval_dir')
parser.add_argument('--disable_retrieval', action="store_true")
parser.add_argument('--use_mbert_retrieval', action="store_true")
parser.add_argument('--use_mdpr_retrieval', action="store_true")
parser.add_argument('--use_bm25_retrieval', action="store_true")
parser.add_argument('--use_google_search', action="store_true")
parser.add_argument('--do_monolingual_retrieval', action="store_true")
parser.add_argument('--do_monolingual_eval', action="store_true")
parser.add_argument('--remove_lang', default=None, type=str)
parser.add_argument('--training_subset_langs', nargs='+', default=[])

timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
args = parser.parse_args()
model_path = args.checkpoint_path

if args.dataset == 'x-fact':
    label2idx = XFACT_LABEL2IDX
    idx2label = XFACT_IDX2LABEL
    test_path = args.test_path
    if args.use_mbert_retrieval:
        test_name = test_path.split('\\')[-1].replace('.tsv','.mbert.json')
    elif args.use_mdpr_retrieval:
        test_name = test_path.split('\\')[-1].replace('.tsv','.json')
    elif args.use_bm25_retrieval:
        test_name = test_path.split('\\')[-1].replace('.tsv','.bm25.json')
    else:
        if args.remove_lang is None:
            test_name = test_path.split('\\')[-1].replace('.tsv','.xict.json')
        else:
            test_name = test_path.split('\\')[-1].replace('.tsv',f'.xict-rm_{args.remove_lang}.json')

    test_retrieval_path = os.path.join(args.retrieval_dir,test_name)
    test_examples = read_data(test_path, args)[0]
else:
    raise NotImplementedError

output_dir = '\\'.join(args.checkpoint_path.split('\\')[:-1])
model = BERTModelForClassification(args.model_name, args).cuda()

# init loader

test_set = PropaFakeDataset(tsv_path=test_path, retrieved_path=test_retrieval_path, args=args, label2idx=label2idx, idx2label=idx2label)
test_loader = DataLoader(test_set, batch_size=args.eval_batch_size, shuffle=False, collate_fn=test_set.collate_fn)

checkpoint = torch.load(model_path)
model.load_state_dict(checkpoint['model'])    
test_output_file = os.path.join(output_dir, 'test_pred.json')

with torch.no_grad():
    model.eval()
    test_outputs = []
    test_labels = []
    # test_candidate_outputs = []
    for _, (input_ids, attn_mask, candidate_input_ids, candidate_attention_mask, labels) in enumerate(test_loader):
        outputs = model(input_ids, attention_mask=attn_mask, 
            candidate_input_ids = candidate_input_ids,
            candidate_attention_mask = candidate_attention_mask,
        )
        outputs = outputs.view(-1, args.n_classes)
        test_outputs.append(outputs) 
        test_labels.append(labels)
        
    test_outputs = torch.cat(test_outputs, dim=0) # n_sample, n_class
    test_labels = torch.cat(test_labels, dim=0) # n_sample,
    
    from collections import Counter
    
    test_outputs = test_outputs.argmax(dim=1) # n_sample
    print(Counter(test_outputs.cpu().tolist()))
    print(Counter(test_labels.cpu().tolist()))
    f1_scores = []
    n_parts = 4  # Número de partes
    part_size = len(test_outputs) // n_parts

    for part in range(n_parts):
        start_idx = part * part_size
        end_idx = (part + 1) * part_size if part != n_parts - 1 else len(test_outputs)
    
        part_outputs = test_outputs[start_idx:end_idx]
        part_labels = test_labels[start_idx:end_idx]
        part_examples = list(test_examples.itertuples())[start_idx:end_idx]
    
        part_f1 = calculate_fscore(part_outputs.detach().cpu().numpy(), 
                               part_labels.detach().cpu().numpy(), 
                               part_examples)
        f1_scores.append(part_f1)
        print(f"F1 Score for part {part + 1}: {part_f1:.4f}")

    final_f1_score = sum(f1_scores) / len(f1_scores)
    print(f"Final F1 Score (average of parts): {final_f1_score:.4f}")

    test_outputs = [int(o) for o in test_outputs]
    print(f"Output file to {test_output_file}")
    with open(test_output_file, 'w') as f:
        json.dump({'output': test_outputs}, f)