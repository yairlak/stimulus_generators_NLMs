# stimulus_generators_NLMs

## Operations

- Change the rules of the grammar in grammar_rules.py
- Change the lexical rules in grammar_lexicon.py
- Change the lexical items in lexicon_English.py

## Workflow

1. run grammar.py to get => grammars/grammar.fcfg
2. run stimulus_generator_from_CFG.py to get the sentences => stimuli/stimuli_from_fcfg.csv
3. run stimulus_cleanup.py to clean the stimuli and add columns => stimuli/stimuli.csv

