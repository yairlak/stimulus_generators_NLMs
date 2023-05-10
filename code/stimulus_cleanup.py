#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import utils

fn_stimuli_from_fcfg = '../stimuli/stimuli_from_fcfg.csv'
fn_output = '../stimuli/stimuli.csv'

df = pd.read_csv(fn_stimuli_from_fcfg)
print(f'Loading dataframe: {fn_stimuli_from_fcfg}')

df = utils.remove_sentences_with_repeated_lemma(df)
df = utils.nan_NUM_of_you(df) # TODO: fix at the grammar level

print(f'Adding new columns...')
df = utils.update_subj_and_obj_type(df)
df = utils.add_word_zipf(df)
df = utils.calc_incongruence_counts(df)
df = utils.add_sentence_length(df)
df = utils.add_has_embedtype(df)
df = utils.calc_incongruence_counts(df)
df = utils.add_binding(df)


df = utils.remove_impossible_binding(df)

# Re-arange columns
df = utils.order_columns(df, ['sentence_length', 'sentence_GROUP', 'sentence'])

# Print and save
print(df)
df.to_csv(fn_output)
print(f'Dataframe saved to: {fn_output}')

['sentence_type',
 'sentence_length',
 'has_embed_',
 'has_objrel',
 'has_quest_',
 'has_subjrel',
 'incongruence_poss_obj_count',
 'incongruence_poss_subj_count',
 'incongruence_subj_embedsubj_count',
 'incongruence_subj_obj_count',
 'incongruent_subj_embedsubj_NUM',
 'mean_zipf',
 'obj_ANIM',
 'obj_GEN',
 'obj_NUM',
 'obj_PERS',
 'obj_REFL',
 'obj_type',
 'quantifier',
 'quantifier_NUM',
 'quantifier_type',
 'subj_ANIM',
 'subj_GEN',
 'subj_NUM',
 'subj_PERS',
 'subj_type',
 'verb_TENSE',
 'verb_type']
