#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import add_features_to_dict
from utils import check_twice, check_congruence
from utils import compute_new_features, order_columns
from utils import remove_repeated_lemma_and_sentences
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
        if "dogs see " in d['sentence']:
            print("WARNING")
            print(d['sentence'])
            print(tree)

        # extract sentence features from tree label
        for i_item, (feature, val) in enumerate(tree.label().items()):
            if feature=='GROUP':
                d[f'sentence_{feature}'] = val # add sentenial features

        # extract word features from tree pos
        for pos in tree.pos(): # Loop over part of speech
            d = add_features_to_dict(d, pos)

        d_grammar.append(d)
        continue # skip if there are more possible parses (n_trees>1)

# To dataframe
df = pd.DataFrame(d_grammar)

# Clean duplicate rows or with a repeated lemma
df = remove_repeated_lemma_and_sentences(df)

# Add new columns
df = compute_new_features(df)

# Re-arange columns
df = order_columns(df, ['sentence_length', 'sentence_GROUP', 'sentence'])

df.to_csv(fn_output)
print(df)