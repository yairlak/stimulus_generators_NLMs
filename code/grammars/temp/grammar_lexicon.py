from lexicon_English import Words

grammar_lexicon = ""

# SUBJECT/OBJECT nouns and DPs
for role in ["subj", "obj", "embedsubj", "embedobj"]:
    grammar_lexicon += f"""
poss_{role}[NUM=sg, PERS=1, BOUND=TESTFEATUREMATCH] -> 'my'
poss_{role}[NUM=pl, PERS=1, BOUND=TESTFEATUREMATCH] -> 'our'
poss_{role}[PERS=2, BOUND=TESTFEATUREMATCH] -> 'your'
poss_{role}[NUM=sg, GEN=f, PERS=3, BOUND=TESTFEATUREMATCH] -> 'her'
poss_{role}[NUM=sg, GEN=m, PERS=3, BOUND=TESTFEATUREMATCH] -> 'his'
poss_{role}[NUM=pl, GEN=m, PERS=3, BOUND=TESTFEATUREMATCH] -> 'their'
poss_{role}[NUM=pl, GEN=f, PERS=3, BOUND=TESTFEATUREMATCH] -> 'their'

{role}_who[ANIM=true] -> 'who'

quantifier_{role}[NUM=sg] -> '{"'|'".join(Words['quantifiers']['singular'])}'
quantifier_{role}[NUM=pl] -> '{"'|'".join(Words['quantifiers']['plural'])}'

{role}_N[NUM=sg, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['singular'])}'
{role}_N[NUM=sg, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['singular'])}'
{role}_N[NUM=pl, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['plural'])}'
{role}_N[NUM=pl, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['plural'])}'
{role}_N[NUM=sg, PERS=3, ANIM=false] -> '{"'|'".join(Words['nouns_inanimate']['singular'])}'
{role}_N[NUM=pl, PERS=3, ANIM=false] -> '{"'|'".join(Words['nouns_inanimate']['plural'])}'

{role}_PropN[NUM=sg, GEN=f, PERS=3, ANIM=true]-> '{"'|'".join(Words['proper_names']['singular']['feminine'])}'
{role}_PropN[NUM=sg, GEN=m, PERS=3, ANIM=true]-> '{"'|'".join(Words['proper_names']['singular']['masculine'])}'
"""

# relative nouns
grammar_lexicon += f"""
possN[NUM=sg, GEN=f, PERS=3, ANIM=true] -> 'mother'|'father'
possN[NUM=sg, GEN=f, PERS=3, ANIM=true] -> 'sister'|'brother'
possN[NUM=pl, GEN=f, PERS=3, ANIM=true] -> 'sisters'|'brothers'
possN[NUM=sg, GEN=f, PERS=3, ANIM=false] -> 'cat'|'dog'
possN[NUM=pl, GEN=f, PERS=3, ANIM=false] -> 'cats'|'dogs'
            """

# PRONOUNS
# subject pronouns
grammar_lexicon += f"""
subj_PRO[NUM=sg, PERS=1, ANIM=true]->'I'
subj_PRO[NUM=pl, PERS=2, ANIM=true]->'you'
subj_PRO[NUM=sg, PERS=3, GEN=m, ANIM=true]->'he'
subj_PRO[NUM=sg, PERS=3, GEN=f, ANIM=true]->'she'
subj_PRO[NUM=sg, PERS=3, ANIM=false]->'it'
subj_PRO[NUM=pl, PERS=3, ANIM=true]->'they'
subj_PRO[NUM=pl, PERS=1, ANIM=true]->'we'
"""
# object pronouns
grammar_lexicon += f"""
obj_PRO[NUM=sg, PERS=1, ANIM=true, BOUND=false]->'me'
obj_PRO[NUM=sg, PERS=1, ANIM=true, BOUND=true]->'myself'
obj_PRO[PERS=2, ANIM=true, BOUND=false]->'you'
obj_PRO[PERS=2, NUM=sg, ANIM=true, BOUND=true]->'yourself'
obj_PRO[PERS=2, NUM=pl, ANIM=true, BOUND=true]->'yourselves'
obj_PRO[NUM=sg, GEN=m, PERS=3, ANIM=true, BOUND=false]->'him'
obj_PRO[NUM=sg, GEN=m, PERS=3, ANIM=true, BOUND=true]->'himself'
obj_PRO[NUM=sg, GEN=f, PERS=3, ANIM=true, BOUND=false]->'her'
obj_PRO[NUM=sg, GEN=f, PERS=3, ANIM=true, BOUND=true]->'herself'
obj_PRO[NUM=sg, GEN=m, PERS=3, ANIM=false, BOUND=false]->'it'
obj_PRO[NUM=sg, GEN=m, PERS=3, ANIM=false, BOUND=true]->'itself'
obj_PRO[NUM=pl, PERS=3, ANIM=true, BOUND=false]->'them'
obj_PRO[NUM=pl, PERS=3, ANIM=true, BOUND=true]->'themselves'
obj_PRO[NUM=pl, PERS=1, ANIM=true, BOUND=false]->'us'
obj_PRO[NUM=pl, PERS=1, ANIM=true, BOUND=true]->'ourselves'
"""

# VERBS

for verb_type, anim_feature, Wkey in [
    ("Intrans", ", ANIM=true", "verbs_intran_anim"),
    ("Intrans", "", "verbs_intran_inanim"),
    ("Trans", ", ANIM=true", "verbs"),
    ("Matrix", ", ANIM=true", "matrix_verbs")
    ]:
    for role in ["verb", "embedverb"]:
        if not ((role == "embedverb") and (verb_type == "Matrix")):
            W = Words[Wkey]
            grammar_lexicon += f"""
{role}_{verb_type}[finite=true, TENSE=pres, NUM=sg, PERS=1{anim_feature}] -> '{"'|'".join(W['present']['plural'])}'
{role}_{verb_type}[finite=true, TENSE=pres, NUM=sg, PERS=2{anim_feature}] -> '{"'|'".join(W['present']['plural'])}'
{role}_{verb_type}[finite=true, TENSE=pres, NUM=sg, PERS=3{anim_feature}] -> '{"'|'".join(W['present']['singular'])}'
{role}_{verb_type}[finite=true, TENSE=pres, NUM=pl{anim_feature}] -> '{"'|'".join(W['present']['plural'])}'
{role}_{verb_type}[finite=true, TENSE=past{anim_feature}] -> '{"'|'".join(W['past'])}'
{role}_{verb_type}[finite=true, TENSE=future{anim_feature}] -> '{"'|'".join(W['future'])}'
{role}_{verb_type}[finite=false, {anim_feature}] -> '{"'|'".join(W['finite'])}'
            """

# AUX
grammar_lexicon += f"""
do_Aux[TENSE=pres, NUM=sg, PERS=1] -> 'do'
do_Aux[TENSE=pres, NUM=sg, PERS=2] -> 'do'
do_Aux[TENSE=pres, NUM=sg, PERS=3] -> 'does'
do_Aux[TENSE=pres, NUM=pl] -> 'do'
do_Aux[TENSE=past] -> 'did'
do_Aux[TENSE=future, NUM=pl] -> 'will'
"""

# OTHER
grammar_lexicon += f"""
Det -> 'the'
P -> '{"'|'".join(Words['loc_preps'])}'

rel_That -> 'that'
rel_Whether -> 'whether'
rel_which -> 'which'
rel_who -> 'who'
obj_WH -> 'whom'
Which -> 'which'
"""
print(grammar_lexicon)