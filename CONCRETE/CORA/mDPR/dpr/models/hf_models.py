#!/usr/bin/env python3
import logging
from typing import Tuple

import torch
from torch import Tensor as T
from torch import nn
from transformers import BertModel, AdamW, AutoTokenizer, AutoConfig

from dpr.utils.data_utils import Tensorizer
from .biencoder import BiEncoder
from .reader import Reader

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)


def get_bert_biencoder_components(args, inference_only: bool = False, **kwargs):
    dropout = getattr(args, 'dropout', 0.0)
    question_encoder = HFBertEncoder.init_encoder(args.pretrained_model_cfg,
                                                  projection_dim=args.projection_dim, dropout=dropout, **kwargs)
    ctx_encoder = HFBertEncoder.init_encoder(args.pretrained_model_cfg,
                                             projection_dim=args.projection_dim, dropout=dropout, **kwargs)

    fix_ctx_encoder = getattr(args, 'fix_ctx_encoder', False)
    print(f"fix context encoder: {fix_ctx_encoder}")
    biencoder = BiEncoder(question_encoder, ctx_encoder, fix_ctx_encoder=fix_ctx_encoder)

    optimizer = None if inference_only else get_optimizer(
        biencoder, learning_rate=args.learning_rate,
        adam_eps=args.adam_eps, weight_decay=args.weight_decay
    )

    tensorizer = get_bert_tensorizer(args)
    return tensorizer, biencoder, optimizer


def get_bert_reader_components(args, inference_only: bool = False, **kwargs):
    dropout = getattr(args, 'dropout', 0.0)
    encoder = HFBertEncoder.init_encoder(args.pretrained_model_cfg,
                                         projection_dim=args.projection_dim, dropout=dropout)

    hidden_size = encoder.config.hidden_size
    reader = Reader(encoder, hidden_size)

    optimizer = None if inference_only else get_optimizer(
        reader, learning_rate=args.learning_rate,
        adam_eps=args.adam_eps, weight_decay=args.weight_decay
    )

    tensorizer = get_bert_tensorizer(args)
    return tensorizer, reader, optimizer


def get_bert_tensorizer(args, tokenizer=None):
    tokenizer = tokenizer or AutoTokenizer.from_pretrained(args.pretrained_model_cfg, do_lower_case=args.do_lower_case, use_fast=False)
    return BertTensorizer(tokenizer, args.sequence_length)


def get_optimizer(model: nn.Module, learning_rate: float = 1e-5, adam_eps: float = 1e-8, weight_decay: float = 0.0) -> torch.optim.Optimizer:
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    return AdamW(optimizer_grouped_parameters, lr=learning_rate, eps=adam_eps)


class HFBertEncoder(BertModel):
    def __init__(self, config, project_dim: int = 0):
        super().__init__(config)
        assert config.hidden_size > 0, 'Encoder hidden_size cannot be zero'
        self.encode_proj = nn.Linear(config.hidden_size, project_dim) if project_dim != 0 else None
        self.init_weights()

    @classmethod
    def init_encoder(cls, cfg_name: str, projection_dim: int = 0, dropout: float = 0.1, **kwargs) -> BertModel:
        cfg = AutoConfig.from_pretrained(cfg_name or 'bert-base-uncased')
        if dropout != 0:
            cfg.attention_probs_dropout_prob = dropout
            cfg.hidden_dropout_prob = dropout
        return cls.from_pretrained(cfg_name, config=cfg, project_dim=projection_dim, **kwargs)

    def forward(self, input_ids: T, token_type_ids: T, attention_mask: T) -> Tuple[T, ...]:
        outputs = super().forward(input_ids=input_ids, 
                              token_type_ids=token_type_ids, 
                              attention_mask=attention_mask)

        sequence_output = outputs.last_hidden_state
        hidden_states = outputs.hidden_states
        pooled_output = sequence_output[:, 0, :]

        if self.encode_proj:
            pooled_output = self.encode_proj(pooled_output)

        return sequence_output, pooled_output, hidden_states

    def get_out_size(self):
        return self.encode_proj.out_features if self.encode_proj else self.config.hidden_size


class BertTensorizer(Tensorizer):
    def __init__(self, tokenizer: AutoTokenizer, max_length: int, pad_to_max: bool = True):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.pad_to_max = pad_to_max

    def text_to_tensor(self, text: str, title: str = None, add_special_tokens: bool = True):
        text = text[0] if isinstance(text, list) and len(text) == 1 else text.strip()

        token_ids = self.tokenizer.encode(title, text_pair=text, add_special_tokens=add_special_tokens,
                                          max_length=self.max_length, pad_to_max_length=False, truncation=True) if title else \
                    self.tokenizer.encode(text, add_special_tokens=add_special_tokens, max_length=self.max_length,
                                          pad_to_max_length=False, truncation=True)

        seq_len = self.max_length
        if self.pad_to_max and len(token_ids) < seq_len:
            token_ids.extend([self.tokenizer.pad_token_id] * (seq_len - len(token_ids)))
        elif len(token_ids) > seq_len:
            token_ids = token_ids[:seq_len]
            token_ids[-1] = self.tokenizer.sep_token_id

        return torch.tensor(token_ids)

    def get_pair_separator_ids(self) -> T:
        return torch.tensor([self.tokenizer.sep_token_id])

    def get_pad_id(self) -> int:
        return self.tokenizer.pad_token_type_id

    def get_attn_mask(self, tokens_tensor: T) -> T:
        return tokens_tensor != self.get_pad_id()

    def is_sub_word_id(self, token_id: int):
        token = self.tokenizer.convert_ids_to_tokens([token_id])[0]
        return token.startswith("##") or token.startswith(" ##")

    def to_string(self, token_ids, skip_special_tokens=True):
        return self.tokenizer.decode(token_ids, skip_special_tokens=skip_special_tokens)

    def set_pad_to_max(self, do_pad: bool):
        self.pad_to_max = do_pad


class RobertaTensorizer(BertTensorizer):
    def __init__(self, tokenizer, max_length: int, pad_to_max: bool = True):
        super().__init__(tokenizer, max_length, pad_to_max=pad_to_max)