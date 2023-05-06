#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import add_features_to_dict, remove_repeated_sentences
from utils import sanity_checks
from nltk.parse import load_parser
from nltk.parse.generate import generate
from tqdm import tqdm
import pandas as pd

path2grammar = 'grammars/grammar.fcfg'
fn_output = '../stimuli/stimuli_from_fcfg.csv'

fcfg = load_parser(path2grammar, trace=0)

d_grammar = []
for s in tqdm(list(generate(fcfg.grammar()))):  # generate all sentences from grammar
    for tree in fcfg.parse(s):  # enter loop only if parsablei
        s = ' '.join(s)
        for d in d_grammar:
            if s==d['sentence']: break # Skip if sentence already exists
        
        d = {}
        d['sentence'] = s
        sanity_checks(d['sentence'], tree) # e.g., agreement ('dog see')
        
        # extract sentence features from tree label
        for i_item, (feature, val) in enumerate(tree.label().items()):
            if feature == 'GROUP':
                d[f'sentence_{feature}'] = val  # add sentenial features

        # extract word features from tree pos
        for pos in tree.pos():  # Loop over part of speech
            d = add_features_to_dict(d, pos)

        d_grammar.append(d)
        break  # skip if there are more possible parses (n_trees>1)

# To dataframe
df = pd.DataFrame(d_grammar)

df = remove_repeated_sentences(df) # can be probably removed

df.to_csv(fn_output)
print(df)
