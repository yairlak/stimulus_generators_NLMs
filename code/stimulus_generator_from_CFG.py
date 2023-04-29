#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 22:53:26 2023

@author: yair
"""

from nltk.parse import load_parser
from nltk.parse.generate import generate

n_debug = 100

fn_grammar = 'grammar.fcfg'
fn_output = '../stimuli/stimuli_from_fcfg.csv'
fcfg = load_parser(fn_grammar, trace=1)

with open(fn_output, 'w') as f:
    for s in list(generate(fcfg.grammar())):
        for tree in fcfg.parse(s): # enter loop only if parsable
            f.write(' '.join(s)+'\n')
            print(tree.pos())
            print(tree.pformat())