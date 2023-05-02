#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def add_features_to_dict(d, pos_tuple):
    word, pos = pos_tuple
    for i_item, (key, val) in enumerate(pos.items()):
        if i_item == 0: # Get subj/verb/object from *type* of pos
            svo = None
            if '_' in val:
                svo, svo_type = val.split('_')
                if svo_type in ['Quantifier', 'Det']: # Exception
                    d[val] = word # val:subj_QuantifierTrue
                else:
                    d[f'{svo}_type'] = svo_type
                    d[f'{svo}'] = word
        else: # Features of pos
            if svo is not None:
                feature_name = key
                d[f'{svo}_{feature_name}'] = val
    return d

