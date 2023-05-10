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


def remove_faulty_agreements(df):
    # Warning: adjency between noun and verb does not guarantee agreement
    # Here it is protected because we look at (noun, verb) pairs very early
    # Beware of RC, auxiliaries, etc.
    def flatten(list_list):
        return [item for sublist in list_list for item in sublist]

    patterns = []

    noun_inanimate = Words['nouns_inanimate']['singular'] + Words['nouns_inanimate']['plural']
    verb_animate = set(flatten(Words['verbs'].values()) + flatten(Words['verbs_intran_anim']))
    pattern_animacy = "([A-Za-z]+\s)(" + "|".join(noun_inanimate) + ")\s(" + "|".join(verb_animate) + r")\b"

    patterns.append(pattern_animacy)

    pro_verb_s = ["he", "she", "it"]
    # noun_sg = ["man", "brother", "actor", "woman", "sister", "actress", "book", "plate", "pencil"]
    noun_sg =  Words['nouns']['masculine']['singular'] + \
               Words['nouns']['feminine']['singular'] + \
               Words['nouns_inanimate']['singular']    
    proper_names = Words['proper_names']['singular']['masculine'] + Words['proper_names']['singular']['feminine']

    # verb_pl = ["see", "stop", "play", "sing", "sneeze", "fall", "disappear", "vanish", "know", "remember", "declare"]
    verb_pl = Words['verbs']['present']['plural'] + \
              Words['verbs_intran_anim']['present']['plural'] + \
              Words['verbs_intran_inanim']['present']['plural'] + \
              Words['matrix_verbs']['present']['plural']
              
    pattern_noun_sg = "([A-Za-z]+\s){0,1}(" + "|".join(noun_sg+proper_names) + ")\s(" + "|".join(verb_pl) + r")\b"
    pattern_pro_sg = "(" + "|".join(pro_verb_s) + ")\s(" + "|".join(verb_pl) + r")\b"

    patterns.append(pattern_noun_sg)
    patterns.append(pattern_pro_sg)

    pro_verb_no_s = ["I", "you", "we", "they"]
    noun_pl = [n+'s' for n in noun_sg] + ["men", "women", "actresses"]
    noun_pl.remove("mans")
    noun_pl.remove("womans")
    noun_pl.remove("actresss")
    verb_sg = [v+'s' for v in verb_pl] + ["vanishes"]
    verb_sg.remove("vanishs")
    pattern_pl = "([A-Za-z]+\s)(" + "|".join(noun_pl) + ")\s(" + "|".join(verb_sg) + r")\b"
    pattern_pro_pl = "(" + "|".join(pro_verb_no_s) + ")\s(" + "|".join(verb_sg) + r")\b"

    patterns.append(pattern_pl)
    patterns.append(pattern_pro_pl)

    pattern = "|".join(f"((that|whether)\s{p})" for p in patterns)
    pattern += "|"
    pattern += "|".join(f"(^{p})" for p in patterns)

    quant_sg = ["every", "no"]
    quant_pl = ["all", "few"]
    pattern_q_sg = "(" + "|".join(quant_sg) + ")\s(" + "|".join(noun_pl) + r")\b"
    pattern_q_pl = "(" + "|".join(quant_pl) + ")\s(" + "|".join(noun_sg) + r")\b"

    pattern += f"|({pattern_q_sg})"
    pattern += f"|({pattern_q_pl})"

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
