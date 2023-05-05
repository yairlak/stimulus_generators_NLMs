
import pandas as pd
from utils import check_twice, check_congruence

fn_sentences = '../stimuli/stimuli_from_fcfg.csv'

df = pd.read_csv(fn_sentences)

for feat in ['NUM', 'GEN', 'PERS', 'ANIM']:
    df[f'congruent_subj_{feat}'] = df.apply(lambda row:
                                            check_congruence(row[f'subj_{feat}'],
                                                             row[f'embedsubj_{feat}']),
                                            axis=1)