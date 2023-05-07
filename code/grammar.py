from grammar_rules import grammar_rules
from grammar_lexicon import grammar_lexicon

fn_grammar = 'grammars/grammar.fcfg'

grammar = ""

grammar += "####################\n# PRODUCTION RULES #\n####################\n\n"
grammar += grammar_rules
grammar += "#################\n# LEXICAL RULES #\n#################\n\n"
grammar += grammar_lexicon

with open(fn_grammar, 'w') as f:
    f.write(grammar)
