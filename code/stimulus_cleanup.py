#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import utils

fn_stimuli_from_fcfg = '../stimuli/stimuli_from_fcfg.csv'
fn_output = '../stimuli/stimuli.csv'

df = pd.read_csv(fn_stimuli_from_fcfg)
print(f'Loading dataframe: {fn_stimuli_from_fcfg}')

print('Removing repeated lemmas...')
df = utils.remove_sentences_with_repeated_lemma(df)

print('Modifying columns...')
df = utils.nan_NUM_of_you(df) # TODO: fix at the grammar level
df = utils.modify_tense_of_obj_quest(df)

print(f'Adding new columns...')
df = utils.add_clause_type(df)
df = utils.add_word_zipf(df)
df = utils.calc_incongruence_counts(df)
df = utils.add_sentence_length(df)
df = utils.add_has_property(df)
df = utils.calc_incongruence_counts(df)
df = utils.lr_agreement_with_attractor(df)
df = utils.add_binding(df)


df = utils.remove_impossible_binding(df)

# Re-arange columns
df = utils.order_columns(df, ['sentence_length', 'sentence_GROUP', 'sentence'])

# Print and save
print(df)
df.to_csv(fn_output)
print(f'Dataframe saved to: {fn_output}')