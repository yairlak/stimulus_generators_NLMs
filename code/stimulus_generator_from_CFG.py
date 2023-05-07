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


def process_sentence(s):
    sentence = ' '.join(s)
    for tree in fcfg.parse(s):  # enter loop only if parsablei
        d = {}
        d['sentence'] = sentence
        sanity_checks(sentence, tree) # e.g., agreement ('dog see') - not a full proof test

        # extract sentence features from tree label
        for i_item, (feature, val) in enumerate(tree.label().items()):
            if feature == 'GROUP':
                d[f'sentence_{feature}'] = val  # add sentential features

        # extract word features from tree pos
        for pos in tree.pos():  # Loop over part of speech
            d = add_features_to_dict(d, pos)

        return d
    return None


d_grammar = [process_sentence(s) for s in tqdm(list(generate(fcfg.grammar())))]
d_grammar = [s for s in d_grammar if s is not None]

# To dataframe
df = pd.DataFrame(d_grammar)

df = remove_repeated_sentences(df)

df.to_csv(fn_output)
print(df)
