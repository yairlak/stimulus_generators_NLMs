#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from check_binding_conditions import calc_binding
from lexicon_English import Words


def extract_verb(POS, anim_feature, Wkey):
    if (POS == "embedverb_Matrix"):
        return ""
    W = Words[Wkey]
    res = ""
    res = f"""
{POS}[finite=true, TENSE=pres, NUM=sg, PERS=1{anim_feature}] -> '{"'|'".join(W['present']['plural'])}'
{POS}[finite=true, TENSE=pres, NUM=sg, PERS=2{anim_feature}] -> '{"'|'".join(W['present']['plural'])}'
{POS}[finite=true, TENSE=pres, NUM=sg, PERS=3{anim_feature}] -> '{"'|'".join(W['present']['singular'])}'
{POS}[finite=true, TENSE=pres, NUM=pl{anim_feature}] -> '{"'|'".join(W['present']['plural'])}'
{POS}[finite=true, TENSE=past{anim_feature}] -> '{"'|'".join(W['past'])}'
{POS}[finite=true, TENSE=future{anim_feature}] -> '{"'|'".join(W['future'])}'"""
    if "-finite" in W.keys():
        res += f"""
{POS}[finite=false{anim_feature}] -> '{"'|'".join(W['-finite'])}'"""
    res += "\n"
    return res


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


def get_agreement_match(row, role1, role2, agr_features=None):
    if agr_features is None:
        agr_features = ["GEN", "NUM", "PERS", "ANIM"]
    agreement_match = {}
    if pd.isnull(row[f"{role1}_type"]) or pd.isnull(row[f"{role1}_type"]):
        # How do we mark that?
        # return np.nan?
        # agreement_match = {feature: np.nan for feature in agr_features}
        pass
    else:
        for feature in agr_features:
            agreement_match[feature] = check_congruence(
                row[f"{role1}_{feature}"],
                row[f"{role2}_{feature}"])
    agreement_match["all"] = all(agreement_match[feature] for feature in agr_features)
    return agreement_match


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
    for test_exclude in ["I saw me", "She saw her"]:
        assert (test_exclude in df[binding_problems]["sentence"]) or ( not (test_exclude in df["sentence"]) )
    for test_include in ["I saw myself", "She saw herself"]:
        assert not (test_include in df[binding_problems]["sentence"])
    df = df[~binding_problems]
    df = df.reset_index(drop=True)
    return df


def calc_incongruence_counts(df):
    df = calc_incongruence_count(df, "subj", "obj")
    df = calc_incongruence_count(df, "poss", "subj")
    df = calc_incongruence_count(df, "poss", "obj")
    df = calc_incongruence_count(df, "subj", "embedsubj")
    return df


def calc_incongruence_count(df, role1, role2, features=None):
    if features is None:
        features = ['NUM', 'GEN', 'PERS', 'ANIM']
    df = add_agr_congruence(df, role1, role2)
    cols = [f"congruent_{role1}_{role2}_{feat}" for feat in features]
    df[f"{role1}_{role2}_incongruence_count"] = df[cols].eq(False).sum(axis=1)
    return df


def add_agr_congruence(df, role1, role2):
    for feat in ['NUM', 'GEN', 'PERS', 'ANIM']:
        df[f'congruent_{role1}_{role2}_{feat}'] = df.apply(lambda row:
                                                check_congruence(row[f'{role1}_{feat}'],
                                                                 row[f'{role2}_{feat}']),
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
    for fragment_test in [
        "dog see ",  # not a perfect test: "The boy that saw the dogs see the man"
        "dogs falls"  # not a perfect test: "The boy that saw the dogs falls"
    ]:
        if fragment_test in sentence:
            print("WARNING")
            print(sentence)
            print(tree)
        return
