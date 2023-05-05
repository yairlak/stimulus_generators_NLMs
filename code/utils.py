#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np

def add_features_to_dict(d, pos_tuple):
    word, pos = pos_tuple
    for i_item, (key, val) in enumerate(pos.items()):
        if i_item == 0: # Get subj/verb/object from *type* of pos
            svo = None
            if '_' in val:
                svo, svo_type = val.split('_')
                if svo_type in ['Quantifier']: # Exception
                    d[val] = word # val:subj_QuantifierTrue
                elif svo_type!='':
                    d[f'{svo}_type'] = svo_type
                    d[f'{svo}'] = word
        else: # Features of pos
            if svo is not None:
                feature_name = key
                d[f'{svo}_{feature_name}'] = val
    return d


def check_twice(sentence, E):
    matches = re.findall(E, sentence)
    return len(matches) > 1


def check_congruence(f1, f2):
    if pd.isnull(f1) or pd.isnull(f2):
        return np.nan
    else:
        return f1==f2