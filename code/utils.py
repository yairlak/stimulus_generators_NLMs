#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pandas as pd
import numpy as np
from check_binding_conditions import calc_binding
from lexicon_English import Words
import wordfreq

def sentences_to_df(sentences):
    sentences_txt = [" ".join(sentence) for sentence in sentences]
    df = pd.DataFrame({"sentence": sentences_txt})
    return df


def df_to_sentences(df):
    sentences_txt = df["sentence"]
    sentences = [sentence_txt.split(" ") for sentence_txt in sentences_txt]
    return sentences


def godown_dict_keys(d, ks):
    res = set()
    if len(ks) == 0:
        return d
    elif (type(d) is not dict):
        return res
    else:
        next_ds = [next_d for k, next_d in d.items() if re.search(ks[0], k)]
        for next_d in next_ds:
            res = res.union(godown_dict_keys(next_d, ks[1:]))
    return res


def reg_unigrams(w_list, border=r"\b"):
    return "|".join(rf"{border}{w}{border}" for w in w_list)


def reg_bigrams(w1_list, w2_list):
    return f"({reg_unigrams(w1_list)})" + r"\s" + f"({reg_unigrams(w2_list)})"


def remove_faulty_agreements(df):
    # Warning: adjency between noun and verb does not guarantee agreement
    # Here it is protected because we look at (noun, verb) pairs very early
    # Beware of RC, auxiliaries, etc.

    patterns_a = []

    noun_inanimate = godown_dict_keys(Words, ['nouns_inanimate', '.*'])
    verb_animate = godown_dict_keys(Words, [r'\bverbs\b|\bverbs_intran_anim\b', '.*', '.*'])
    pattern_animacy = "[A-Za-z]+\s" + reg_bigrams(noun_inanimate, verb_animate)

    patterns_a.append(pattern_animacy)

    pro_verb_s = ["he", "she", "it"]
    noun_sg_anim = godown_dict_keys(Words, [r'(\bnouns\b|\bnouns_inanimate\b)', '.*', 'singular'])
    noun_sg_inanim = godown_dict_keys(Words, [r'(\bnouns_inanimate\b)', 'singular'])
    noun_sg = noun_sg_anim.union(noun_sg_inanim)
    proper_names = godown_dict_keys(Words, [r'\bproper_names\b', '.*', '.*'])

    pro_verb_no_s = ["I", "you", "we", "they"]
    noun_pl = godown_dict_keys(Words, [r'\bnouns\b|\bnouns_inanimate\b', '.*', 'plural'])

    verb_sg = godown_dict_keys(Words, ['verbs', 'present', 'singular'])
    verb_pl = godown_dict_keys(Words, ['verbs', 'present', 'plural'])

    pattern_PN_sg = reg_bigrams(proper_names, verb_pl)
    pattern_noun_sg = "[A-Za-z]+\s" + reg_bigrams(noun_sg, verb_pl)
    pattern_pro_sg = reg_bigrams(pro_verb_s, verb_pl)
    pattern_pl = "[A-Za-z]+\s" + reg_bigrams(noun_pl, verb_sg)
    pattern_pro_pl = reg_bigrams(pro_verb_no_s, verb_sg)

    patterns_a.append(pattern_PN_sg)
    patterns_a.append(pattern_noun_sg)
    patterns_a.append(pattern_pro_sg)
    patterns_a.append(pattern_pl)
    patterns_a.append(pattern_pro_pl)

    patterns = []
    for pattern in patterns_a:
        patterns.append(f"^{pattern}")
        patterns.append(f"(that|whether){pattern}")

    quant_sg = ["every", "no"]
    quant_pl = ["all", "few"]
    pattern_q_sg = reg_bigrams(quant_sg, noun_pl)
    pattern_q_pl = reg_bigrams(quant_pl, noun_sg)
    patterns.append(f"{pattern_q_sg}")
    patterns.append(f"{pattern_q_pl}")

    pattern = "|".join(rf"({p})" for p in patterns)

    mask = df["sentence"].str.contains(pattern)
    df = df[~mask]

    return df


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


def check_incongruence(f1, f2, role1=None, role2=None, poss_type=None):
    if pd.isnull(f1) or pd.isnull(f2):
        return np.nan
    elif role1=='poss' and poss_type!=role2:
        # Verify that the possessive is of the current role.
        # Since, poss-subj congruence means 'poss' is the possessive of the subject
        # And poss-obj congruence means the 'poss' is of the object.
        return np.nan
    else:
        return (f1 != f2)


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
            agreement_match[feature] = check_incongruence(
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
    SINGLE_STRINGS = Words['proper_names']['singular']['masculine'] + \
                     Words['proper_names']['singular']['feminine']
    SINGLE_STRINGS = [rf"\b{w}\b" for w in SINGLE_STRINGS]
    SINGLE_PAIRS = ([
            Words['nouns']['masculine'][NUM] +
            Words['nouns']['feminine'][NUM] +
            Words['nouns_inanimate'][NUM]
            for NUM in ['singular', 'plural']])
    SINGLE_PAIRS = [
        rf"\b{n_sg}\b|\b{n_pl}\b"
        for (n_sg, n_pl) in zip(*SINGLE_PAIRS)]
    REG_EX = SINGLE_STRINGS + SINGLE_PAIRS
    for E in REG_EX:
        mask = (df['sentence'].str.count(E) <= 1)
        df = df[mask]
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
    df = calc_incongruence_feature(df, role1, role2)
    cols = [f"incongruent_{role1}_{role2}_{feat}" for feat in features]
    cols = [c for c in cols if c in df.columns]
    df[f"incongruence_{role1}_{role2}_count"] = df[cols].sum(axis=1, min_count=1)
    return df


def calc_incongruence_feature(df, role1, role2):
    for feat in ['NUM', 'GEN', 'PERS', 'ANIM']:
        if f'{role1}_{feat}' in df.columns and f'{role2}_{feat}' in df.columns:
            df[f'incongruent_{role1}_{role2}_{feat}'] = df.apply(lambda row:
                                                    check_incongruence(row[f'{role1}_{feat}'],
                                                                     row[f'{role2}_{feat}'],
                                                                     role1, role2,
                                                                     row['poss_type']),
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


def nan_NUM_of_you(df):
    df.loc[df.subj=='you', 'subj_NUM'] = np.nan
    return df


def compute_mean_zipf(row, words=['subj', 'embedsubj', 'verb', 'embedverb'],
                      lang='en'):
    zipfs = []
    for word in words:
        if not pd.isnull(row[word]):
            zipfs.append(wordfreq.zipf_frequency(row[word],
                                                 lang=lang))
    return np.mean(zipfs)

def add_word_zipf(df):   
    df['mean_zipf'] = df.apply(lambda row: compute_mean_zipf(row), axis=1)
    return df
