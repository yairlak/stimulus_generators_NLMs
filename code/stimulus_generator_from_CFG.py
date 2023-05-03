#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import contextlib

from utils import add_features_to_dict
from nltk.parse import load_parser
from nltk.parse.generate import generate
from tqdm import tqdm
import pandas as pd

path2grammars = 'grammars/'
grammars = ['embeddings']#, 'SVO']

fn_output = '../stimuli/stimuli_from_fcfg.csv'

# MAIN
d_grammars = []
for grammar in grammars:
    fn_grammar = f'grammar_{grammar}.fcfg'
    fcfg = load_parser(os.path.join(path2grammars, fn_grammar), trace=1)
    
    d_grammar = []
    with contextlib.redirect_stdout(open(os.devnull, "w")): # disable NLTK prints
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
    
    d_grammars.extend(d_grammar)
    print(pd.DataFrame(d_grammar))
    
# To dataframe
df = pd.DataFrame(d_grammars)

# Move sentence to front column
cols = sorted(list(df))
cols.insert(0, cols.pop(cols.index('sentence')))
df = df.loc[:, cols]

# Remove cases where subject and object are the same (e.g., the dog watches the dog)
# TODO: should be done at the lemma level
#df_sentences = df_sentences.query("subj!=obj")
#df_sentences = df_sentences.query("subj!=embed")

# Print and save
print(df)
df.to_csv(fn_output)
