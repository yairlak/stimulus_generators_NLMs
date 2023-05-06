#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from check_binding_conditions import calc_binding
from lexicon_English import Words


def add_features_to_dict(d, pos_tuple):
    word, pos = pos_tuple
    for i_item, (key, val) in enumerate(pos.items()):
        if i_item == 0: # Get subj/verb/object from *type* of pos
            svo = None
            if '_' in val:
                svo, svo_type = val.split('_')
                if svo_type != '':
                    d[f'{svo}_type'] = svo_type
                    d[f'{svo}'] = word
        else:  # Features of pos
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
        return (f1 == f2)


def order_columns(df, bring2front):
    # sort columns by name
    cols = sorted(list(df))

    # Move sentence to front column and save
    for name in bring2front:
        cols.insert(0, cols.pop(cols.index(name)))
        df = df.loc[:, cols]
    return df


def remove_repeated_sentences(df):
    df = df.drop_duplicates(subset=['sentence'])
    return df


def remove_sentences_with_repeated_lemma(df):
    # Remove sentences where a lemma is repeated
    # verbs are not included if one verb is trans and the other is intrans
    SINGLE_STRINGS = Words['nouns']['masculine']['singular'] + \
                     Words['nouns']['feminine']['singular'] + \
                     Words['nouns_inanimate']['singular'] + \
                     Words['proper_names']['singular']['masculine'] + \
                     Words['proper_names']['singular']['feminine']
    for E in SINGLE_STRINGS:
        df = df[~df['sentence'].apply(check_twice, E=E)]
    df = df.reset_index(drop=True)
    return df


def remove_impossible_binding(df):
    # remove "He saw him", "I saw me", etc.
    binding_problems = (
        (df["subj_type"] == "PRO") &
        (df["obj_type"] == "PRO") &
        (~(df["obj_REFL"] == True)) &
        (df["obj_congruence_all"])
    )
    for test_exclude in ["I saw me"]:
        assert (test_exclude in df[binding_problems]["sentence"]) or ( not (test_exclude in df["sentence"]) )
    for test_include in ["I saw myself"]:
        assert not (test_include in df[binding_problems]["sentence"])
    df = df[~binding_problems]
    df = df.reset_index(drop=True)
    return df


def add_agr_congruence_subj(df):
    for feat in ['NUM', 'GEN', 'PERS', 'ANIM']:
        df[f'congruent_subj_{feat}'] = df.apply(lambda row:
                                                check_congruence(row[f'subj_{feat}'],
                                                                 row[f'embedsubj_{feat}']),
                                                axis=1)
    return df


def add_sentence_length(df):
    df['sentence_length'] = df.apply(lambda row:
                                     len(row['sentence'].split()),
                                     axis=1)
    return df


def add_has_embedtype(df, groups=['subjrel', 'objrel', 'embed_', 'quest_']):
    for group in groups:
        df[f'has_{group}'] = df.apply(lambda row:
                                      row['sentence_GROUP'].startswith(f'{group}'),
                                      axis=1)
    return df


def add_binding(df):
    binding_cols = df.apply(calc_binding, axis=1, result_type="expand")
    df = pd.concat([df, binding_cols], axis=1)
    return df


def sanity_checks(sentence, tree):
    test1 = "dogs see " in sentence
    test2 = "dogs falls" in sentence
    if test1 or test2:
        print("WARNING")
        print(sentence)
        print(tree)
    return
