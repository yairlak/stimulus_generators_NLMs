#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 22:53:26 2023

@author: yair
"""

from nltk.parse import load_parser
from nltk.parse.generate import generate
import pandas as pd

fn_grammar = 'grammar.fcfg'
fn_output = '../stimuli/stimuli_from_fcfg.csv'
fcfg = load_parser(fn_grammar, trace=1)


def init_features_dict():
    d = {}
    # subj
    d['subj_type'] = None
    d['subj_NUM'] = None
    d['subj_GEN'] = None
    
    # obj
    d['obj_type'] = None
    d['obj_NUM'] = None
    d['obj_GEN'] = None
    
    # v
    d['verb_TENSE'] = None
    return d


def add_features_to_dict(d, pos):
    for i_item, (key, val) in enumerate(pos.items()):
        if i_item == 0: # Get subj/verb/object from *type* of pos
            if '_' in val:
                svo, svo_type = val.split('_')
                if svo in ['subj', 'obj']:
                    d[f'{svo}_type'] = svo_type
            elif val.endswith('V'):
                svo = 'verb'
            else: # determiner
                svo = None
        else: # Features of pos
            if svo is not None:
                feature_name = key
                d[f'{svo}_{feature_name}'] = val
    return d

# MAIN
list_dicts = []
with open(fn_output, 'w') as f:
    for s in list(generate(fcfg.grammar())):
        for tree in fcfg.parse(s): # enter loop only if parsable
            
            d = init_features_dict()
            d['sentence'] = ' '.join(s)
            
            for pos in tree.pos(): # Loop over part of speech
                d = add_features_to_dict(d, pos[1])
        list_dicts.append(d)

# To dataframe
df_sentences = pd.DataFrame(list_dicts)  
cols = sorted(list(df_sentences))
cols.insert(0, cols.pop(cols.index('sentence')))
df_sentences = df_sentences.loc[:, cols]
print(df_sentences)
df_sentences.to_csv(fn_output)