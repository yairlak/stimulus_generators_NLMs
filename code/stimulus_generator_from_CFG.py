#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import utils
from utils import sanity_checks
from nltk.parse import load_parser
from nltk.parse.generate import generate
from tqdm import tqdm
import pandas as pd
import argparse

import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', default=False)
args = parser.parse_args()

path2grammar = 'grammars/grammar.fcfg'
fn_output = '../stimuli/stimuli_from_fcfg.csv'

fcfg = load_parser(path2grammar, trace=0)


def process_sentence(s):
    sentence = ' '.join(s)
    for tree in fcfg.parse(s):  # enter loop only if parsable
        d = {}
        d['sentence'] = sentence
        sanity_checks(sentence, tree)  # e.g., agreement ('dog see') - not a full proof test

        # extract sentence features from tree label
        for i_item, (feature, val) in enumerate(tree.label().items()):
            if feature == 'GROUP':
                d[f'sentence_{feature}'] = val  # add sentential features

        # extract word features from tree pos
        for pos in tree.pos():  # Loop over part of speech
            d = utils.add_features_to_dict(d, pos)

        return d
    return None


if __name__ == "__main__":
    if args.verbose:
        print(fcfg.grammar())

    print("Generating all sentences...")
    sentences = list(generate(fcfg.grammar()))  # Exhausting generator for tqdm counter.
    print(f"- Number of sentences: {len(sentences)}")

    df = utils.sentences_to_df(sentences)

    print("Removing duplicate sentences, duplicate lemmas...")
    df = utils.remove_repeated_sentences(df)
    print(f"- Number of sentences: {len(df)}")
    df = utils.remove_sentences_with_repeated_lemma(df)
    print(f"- Number of sentences: {len(df)}")

    print("Parsing sentences...")
    sentences = utils.df_to_sentences(df)
    process_pool = multiprocessing.Pool(processes=os.cpu_count())
    d_grammar = list(tqdm(process_pool.imap(process_sentence, sentences), total=len(sentences)))

    d_grammar = [s for s in d_grammar if s is not None]

    # To dataframe
    df = pd.DataFrame(d_grammar)

    df.to_csv(fn_output)
    print(df)
    print(f'Stimuli saved to {fn_output}')
