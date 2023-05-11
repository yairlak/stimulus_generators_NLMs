#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import utils

fn_stimuli_from_fcfg = '../stimuli/stimuli_from_fcfg.csv'
fn_output = '../stimuli/stimuli.csv'

df = pd.read_csv(fn_stimuli_from_fcfg)
utils.print_time(f'> Loading dataframe: {fn_stimuli_from_fcfg}')

utils.print_time('> Modifying columns...')
df = utils.modify_tense_of_obj_quest(df)

utils.print_time(f'> Adding new columns...')
utils.print_time("Clause type")
df = utils.add_clause_type(df)
utils.print_time("Word Zipf")
df = utils.add_word_zipf(df)
utils.print_time("Incongruence counts")
df = utils.calc_incongruence_counts(df)
utils.print_time("Sentence length")
df = utils.add_sentence_length(df)
utils.print_time("has_property")
df = utils.add_has_property(df)
utils.print_time("LR agreements")
df = utils.lr_agreement_with_attractor(df)
utils.print_time("Binding")
df = utils.add_binding(df)

utils.print_time("> Remove impossible binding")
df = utils.remove_impossible_binding(df)

utils.print_time("Re-arange columns")
df = utils.order_columns(df, ['sentence_length', 'sentence_GROUP', 'sentence'])

# Print and save
print(df)
df.to_csv(fn_output)
utils.print_time(f'> Dataframe saved to: {fn_output}')
