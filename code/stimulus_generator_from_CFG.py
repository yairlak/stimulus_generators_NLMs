#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import contextlib

from utils import add_features_to_dict, check_twice
from nltk.parse import load_parser
from nltk.parse.generate import generate
from tqdm import tqdm
import pandas as pd

path2grammar = 'grammars/grammar.fcfg'
grammars = ['SVO', 'embeddings']

fn_output = '../stimuli/stimuli_from_fcfg.csv'

# MAIN

fcfg = load_parser(path2grammar, trace=0)

d_grammar = []
for s in tqdm(list(generate(fcfg.grammar()))): # generate all sentences from grammar
    for tree in fcfg.parse(s): # enter loop only if parsablei
        d = {}
        d['sentence'] = ' '.join(s)

        # extract sentence features from tree label
        for i_item, (feature, val) in enumerate(tree.label().items()):
            if i_item == 0:
                pass
            else:
                d[f'sentence_{feature}'] = val # add sentenial features

        # extract word features from tree pos
        for pos in tree.pos(): # Loop over part of speech
            d = add_features_to_dict(d, pos)

        d_grammar.append(d)
        continue # skip if there are more possible parses (n_trees>1)

# To dataframe
df = pd.DataFrame(d_grammar)

# Move sentence to front column
cols = sorted(list(df))
cols.insert(0, cols.pop(cols.index('sentence')))
df = df.loc[:, cols]

# Remove duplicate sentences
df = df.drop_duplicates(subset=['sentence'])

# Remove sentences where a lemma is repeated
SINGLE_STRINGS = [r'dog', r'cat',
                  r'Alice', r'Bob',
                  r'know|knew', r'see|saw', r'fell|fall',
                  r'car',
                  r'boy', r'girl',
                  r'father', r'mother'
                  r'brother', r'sister'
                  ]
for E in SINGLE_STRINGS:
    df = df[~df['sentence'].apply(check_twice, E=E)]
df = df.reset_index(drop=True)

# Print and save
print(df)
df.to_csv(fn_output)
