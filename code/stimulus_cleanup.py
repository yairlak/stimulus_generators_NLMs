#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import utils

fn_stimuli_from_fcfg = '../stimuli/stimuli_from_fcfg.csv'
fn_output = '../stimuli/stimuli.csv'

df = pd.read_csv(fn_stimuli_from_fcfg)

# Clean duplicate rows or with a repeated lemma
df = utils.remove_sentences_with_repeated_lemma(df)

# Add new columns
df = utils.add_agr_congruence_subj(df)
df = utils.add_sentence_length(df)
df = utils.add_has_embedtype(df)
df = utils.add_binding(df)

# Re-arange columns
df = utils.order_columns(df, ['sentence_length', 'sentence_GROUP', 'sentence'])

# Print and save
print(df)
df.to_csv(fn_output)
