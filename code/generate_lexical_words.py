#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
import pandas as pd
from wordfreq import get_frequency_dict, freq_to_zipf
# nltk.download('averaged_perceptron_tagger')

df_wordfreq = pd.DataFrame(get_frequency_dict(lang='en',
                                              wordlist='best').items(),
                           columns=['word', 'freq'])


def tag_pos(row):
    pos = nltk.pos_tag([row['word']])
    return pos[0][1]

df_wordfreq['pos'] = df_wordfreq.apply(lambda row: tag_pos(row),
                                        axis=1)


df_wordfreq['zipf'] = df_wordfreq.apply(lambda row: freq_to_zipf(row['freq']),
                                        axis=1)

df_wordfreq.sort_values(by=['zipf'], ascending=False, inplace=True)

df_NNS_high = df_wordfreq.query("pos=='NNS' & zipf>=5")
df_NNS_med = df_wordfreq.query("pos=='NNS' & zipf>=4 & zipf<5")
df_NNS_low = df_wordfreq.query("pos=='NNS' & zipf>=3 & zipf<4")


df_VBZ_high = df_wordfreq.query("pos=='VB' & zipf>=5")
df_VBZ_med = df_wordfreq.query("pos=='VB' & zipf>=4 & zipf<5")
df_VBZ_low = df_wordfreq.query("pos=='VB' & zipf>=3 & zipf<4")