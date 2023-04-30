#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from utils import add_features_to_dict
from nltk.parse import load_parser
from nltk.parse.generate import generate
import pandas as pd

fn_grammar = 'grammar.fcfg'
fn_output = '../stimuli/stimuli_from_fcfg.csv'
fcfg = load_parser(fn_grammar, trace=1)


# MAIN
list_dicts = []
with open(fn_output, 'w') as f:
    for s in list(generate(fcfg.grammar())): # generate all sentences from grammar
        for tree in fcfg.parse(s): # enter loop only if parsable
            d = {}
            d['sentence'] = ' '.join(s)
            for pos in tree.pos(): # Loop over part of speech
                d = add_features_to_dict(d, pos)
                
            list_dicts.append(d)
            continue # skip if there are more possible parses (n_trees>1)

# To dataframe
df_sentences = pd.DataFrame(list_dicts)

# Move sentence to front column
cols = sorted(list(df_sentences))
cols.insert(0, cols.pop(cols.index('sentence')))
df_sentences = df_sentences.loc[:, cols]

# Remove cases where subject and object are the same (e.g., the dog watches the dog)
df_sentences = df_sentences.query("subj!=obj")

# Print and save
print(df_sentences)
df_sentences.to_csv(fn_output)