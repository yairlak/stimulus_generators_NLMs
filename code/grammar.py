from lexicon_English import Words

fn_grammar = 'grammars/grammar.fcfg'

grammar = f"""
########
# SVOs #
########

S[GROUP=?e] -> subjNP[NUM=?n, PERS=?p, ANIM=?a] VP[NUM=?n, PERS=?p, ANIM=?a, GROUP=?e]

# subject
subjNP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> subj_PropN[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
subjNP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> Det subj_N[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
subjNP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> quantifier_subj[NUM=?n, PERS=?p] subj_N[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
subjNP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> subj_PRO[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]

# verb
VP[NUM=?n, PERS=?p, ANIM=?a, GROUP=sv] -> verb_Intrans[finite=true, NUM=?n, PERS=?p, ANIM=?a]
VP[NUM=?n, PERS=?p, ANIM=?a, GROUP=svo] -> verb_Trans[finite=true, NUM=?n, PERS=?p, ANIM=?a] objNP

# object
objNP -> obj_PropN
objNP -> Det obj_N
objNP -> quantifier_obj[NUM=?n] obj_N[NUM=?n]
objNP -> obj_PRO[BOUND=false]

###########
# BINDING #
###########

# Binding (reflexives)
S[GROUP=?e] -> subjNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] objPRO[GROUP=?e, NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
objPRO[GROUP=binding_reflexives, NUM=?n, GEN=?g, PERS=?p, ANIM=?a] -> obj_PRO[NUM=?n, GEN=?g, PERS=?p, ANIM=?a, BOUND=true]

# Binding (possessives)
S[GROUP=?e] -> subjNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] possObjNP[GROUP=?e]
S[GROUP=?e] -> possSubjNP[GROUP=?e, NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] objNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
possSubjNP[GROUP=possessive_subj, NUM=?n, GEN=?g, PERS=?p, ANIM=?a, possNUM=?pn, possGEN=?pg, possPERS=?pp] -> poss_subj[possNUM=?pn, possGEN=?pg, possPERS=?pp] possN[NUM=?n, GEN=?g, ANIM=?a, PERS=?p]
possObjNP[GROUP=possessive_obj, NUM=?n, GEN=?g, PERS=?p, ANIM=?a, possNUM=?pn, possGEN=?pg, possPERS=?pp] -> poss_obj[possNUM=?pn, possGEN=?pg, possPERS=?pp] possN[NUM=?n, GEN=?g, ANIM=?a, PERS=?p]

#############
# QUESTIONS #
#############

# subject questions (intransitive verb)
S[GROUP=?e] -> subjWho[GROUP=?e] verb_Intrans[finite=true, TENSE=pres, NUM=sg, PERS=3, ANIM=true]
subjWH[GROUP=quest_subj_who_intrans] -> subj_who verb_Intrans[finite=true, NUM=sg, PERS=3, ANIM=true]
subjWH[GROUP=quest_subj_which_intrans] -> Which subj_N[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Intrans[finite=true, NUM=?n, PERS=?p, ANIM=?a]

# subject questions (transitive verb)
S[GROUP=?e] -> subjWH[GROUP=?e]
subjWH[GROUP=quest_subj_who_trans] -> subj_who verb_Trans[finite=true, NUM=sg, PERS=3, ANIM=true] Det obj_N
subjWH[GROUP=quest_subj_which_trans] -> Which subj_N[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, NUM=?n, PERS=?p, ANIM=?a] Det obj_N

# object questions
S[GROUP=?e] -> objWh[GROUP=?e] verb_Trans[finite=false, ANIM=true]
objWh[GROUP=quest_obj_who_trans, NUM=?n, PERS=?p] -> obj_WH do_Aux[NUM=?n, PERS=?p] Det subj_N[NUM=?n, PERS=?p, ANIM=true]
objWh[GROUP=quest_obj_which_trans, NUM=?n, PERS=?p] -> Which obj_N do_Aux[NUM=?n, PERS=?p] Det subj_N[NUM=?n, PERS=?p, ANIM=true]


########################
# Long-Range Agreement #
########################
S[GROUP=?e] -> Det subj_N[NUM=?n, ANIM=?a, PERS=?p] embedPP[GROUP=?e] verb_Intrans[TENSE=pres, NUM=?n, ANIM=?a, PERS=?p]
embedPP[GROUP=pp] -> P Det embedsubj_N[GROUP=pp]

##############
# EMBEDDINGS #
##############
# object RCs
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=3, ANIM=true] rel_That Objrel[GROUP=?g] verb_Intrans[finite=true, TENSE=pres, NUM=?n, PERS=3, ANIM=true]
Objrel[GROUP=objrel] -> Det embedsubj_N[NUM=?n, ANIM=true, GROUP=objrel] embedverb_Trans[finite=true, NUM=?n, TENSE=pres, PERS=3]

# subject RCs
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=3, ANIM=true] rel_That Subjrel[NUM=?n, PERS=3, ANIM=true, GROUP=?g] verb_Intrans[finite=true, TENSE=pres, NUM=?n, PERS=3, ANIM=true]
Subjrel[NUM=?n, PERS=3, ANIM=true, GROUP=subjrel] -> embedverb_Trans[finite=true, NUM=?n, TENSE=pres, PERS=3] Det embedsubj_N[NUM=?n, ANIM=true, GROUP=subjrel]

# Embedding
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=?p, ANIM=true] verb_Matrix[finite=true, NUM=?n, PERS=?p, ANIM=true] embedClause[GROUP=?g]
embedClause[GROUP=embed_that_clause] -> rel_That Det embedsubj_N[NUM=?n] embedverb_Intrans[finite=true, NUM=?n, PERS=3]
embedClause[GROUP=embed_whether_clause] -> rel_Whether Det embedsubj_N[NUM=?n] embedverb_Intrans[finite=true, NUM=?n, PERS=3]
embedClause[GROUP=embed_subjwho_clause] -> rel_who embedverb_Trans[finite=true, NUM=sg, PERS=3, ANIM=true] Det embedobj_N
embedClause[GROUP=embed_objwho_clause] -> embedObjWh[NUM=?n, PERS=?p] embedverb_Trans[finite=true, NUM=?n, PERS=?p, ANIM=true]
embedObjWh[NUM=?n, PERS=?p] -> obj_WH Det embedsubj_N[NUM=?n, PERS=?p, ANIM=true]
embedClause[GROUP=embed_which_clause] -> rel_which embedsubj_N[NUM=?n] embedverb_Intrans[finite=true, NUM=?n, PERS=3]

#######################
# Lexical Productions #
#######################

# Det
Det -> 'the'
poss_subj[NUM=sg, PERS=1] -> 'my'
poss_subj[NUM=pl, PERS=1] -> 'our'
poss_subj[PERS=2] -> 'your'
poss_subj[NUM=sg, GEN=f, PERS=3] -> 'her'
poss_subj[NUM=sg, GEN=m, PERS=3] -> 'his'
poss_subj[NUM=pl, GEN=m, PERS=3] -> 'their'
poss_subj[NUM=pl, GEN=f, PERS=3] -> 'their'
poss_obj[NUM=sg, PERS=1] -> 'my'
poss_obj[NUM=pl, PERS=1] -> 'our'
poss_obj[PERS=2] -> 'your'
poss_obj[NUM=sg, GEN=f, PERS=3] -> 'her'
poss_obj[NUM=sg, GEN=m, PERS=3] -> 'his'
poss_obj[NUM=pl, GEN=m, PERS=3] -> 'their'
poss_obj[NUM=pl, GEN=f, PERS=3] -> 'their'

# subject
subj_PRO[NUM=sg, PERS=1, ANIM=true]->'I'
subj_PRO[NUM=pl, PERS=2, ANIM=true]->'you'
subj_PRO[NUM=sg, PERS=3, GEN=m, ANIM=true]->'he'
subj_PRO[NUM=sg, PERS=3, GEN=f, ANIM=true]->'she'
subj_PRO[NUM=sg, PERS=3, ANIM=false]->'it'
subj_PRO[NUM=pl, PERS=3, ANIM=true]->'they'
subj_PRO[NUM=pl, PERS=1, ANIM=true]->'we'

subj_who[ANIM=true] -> 'who'

quantifier_subj[NUM=sg] -> '{"'|'".join(Words['quantifiers']['singular'])}'
quantifier_subj[NUM=pl] -> '{"'|'".join(Words['quantifiers']['plural'])}'

subj_N[NUM=sg, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['singular'])}'
subj_N[NUM=sg, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['singular'])}'
subj_N[NUM=pl, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['plural'])}'
subj_N[NUM=pl, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['plural'])}'

subj_N[NUM=sg, PERS=3, ANIM=false] -> '{"'|'".join(Words['nouns_inanimate']['singular'])}'
subj_N[NUM=pl, PERS=3, ANIM=false] -> '{"'|'".join(Words['nouns_inanimate']['plural'])}'

subj_PropN[NUM=sg, GEN=f, PERS=3, ANIM=true]-> '{"'|'".join(Words['proper_names']['singular']['feminine'])}'
subj_PropN[NUM=sg, GEN=m, PERS=3, ANIM=true]-> '{"'|'".join(Words['proper_names']['singular']['masculine'])}'

embedsubj_N[NUM=sg, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['singular'])}'
embedsubj_N[NUM=sg, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['singular'])}'
embedsubj_N[NUM=pl, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['plural'])}'
embedsubj_N[NUM=pl, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['plural'])}'

# object
quantifier_obj[NUM=sg] -> '{"'|'".join(Words['quantifiers']['singular'])}'
quantifier_obj[NUM=pl] -> '{"'|'".join(Words['quantifiers']['plural'])}'

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


obj_N[NUM=sg, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['singular'])}'
obj_N[NUM=sg, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['singular'])}'
obj_N[NUM=pl, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['plural'])}'
obj_N[NUM=pl, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['plural'])}'

obj_N[NUM=sg, PERS=3, ANIM=false] -> '{"'|'".join(Words['nouns_inanimate']['singular'])}'
obj_N[NUM=pl, PERS=3, ANIM=false] -> '{"'|'".join(Words['nouns_inanimate']['plural'])}'

obj_WH -> 'who'|'whom'
obj_which -> 'which'

obj_PropN[NUM=sg, GEN=f, PERS=3, ANIM=true]-> '{"'|'".join(Words['proper_names']['singular']['feminine'])}'
obj_PropN[NUM=sg, GEN=m, PERS=3, ANIM=true]-> '{"'|'".join(Words['proper_names']['singular']['masculine'])}'

embedobj_N[NUM=sg, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['singular'])}'
embedobj_N[NUM=sg, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['singular'])}'
embedobj_N[NUM=pl, GEN=m, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['masculine']['plural'])}'
embedobj_N[NUM=pl, GEN=f, PERS=3, ANIM=true] -> '{"'|'".join(Words['nouns']['feminine']['plural'])}'

# VERBS
# INTRANS ANIMATE
verb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=1, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['plural'])}'
verb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=2, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['plural'])}'
verb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=3, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['singular'])}'
verb_Intrans[finite=true, TENSE=pres,  NUM=pl, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['plural'])}'
verb_Intrans[finite=true, TENSE=past, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['past'])}'
verb_Intrans[finite=true, TENSE=future, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['future'])}'

# INTRANS ANIMATE OR INANIMATE
verb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=1] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['plural'])}'
verb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=2] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['plural'])}'
verb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=3] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['singular'])}'
verb_Intrans[finite=true, TENSE=pres,  NUM=pl] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['plural'])}'
verb_Intrans[finite=true, TENSE=past] -> '{"'|'".join(Words['verbs_intran_inanim']['past'])}'
verb_Intrans[finite=true, TENSE=future] -> '{"'|'".join(Words['verbs_intran_inanim']['future'])}'

# EMBED INTRANS ANIMATE
embedverb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=1, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['plural'])}'
embedverb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=2, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['plural'])}'
embedverb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=3, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['singular'])}'
embedverb_Intrans[finite=true, TENSE=pres,  NUM=pl, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['present']['plural'])}'
embedverb_Intrans[finite=true, TENSE=past, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['past'])}'
embedverb_Intrans[finite=true, TENSE=future, ANIM=true] -> '{"'|'".join(Words['verbs_intran_anim']['future'])}'

# EMBED INTRANS ANIMATE OR INANIMATE
embedverb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=1] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['plural'])}'
embedverb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=2] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['plural'])}'
embedverb_Intrans[finite=true, TENSE=pres,  NUM=sg, PERS=3] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['singular'])}'
embedverb_Intrans[finite=true, TENSE=pres,  NUM=pl] -> '{"'|'".join(Words['verbs_intran_inanim']['present']['plural'])}'
embedverb_Intrans[finite=true, TENSE=past] -> '{"'|'".join(Words['verbs_intran_inanim']['past'])}'
embedverb_Intrans[finite=true, TENSE=future] -> '{"'|'".join(Words['verbs_intran_inanim']['future'])}'

# TRANSITIVE (ANIMATE)
verb_Trans[finite=true, TENSE=pres,  NUM=sg, PERS=1, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['plural'])}'
verb_Trans[finite=true, TENSE=pres,  NUM=sg, PERS=2, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['plural'])}'
verb_Trans[finite=true, TENSE=pres,  NUM=sg, PERS=3, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['singular'])}'
verb_Trans[finite=true, TENSE=pres,  NUM=pl, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['plural'])}'
verb_Trans[finite=true, TENSE=past, ANIM=true] -> '{"'|'".join(Words['verbs']['past'])}'
verb_Trans[finite=true, TENSE=future, ANIM=true] -> '{"'|'".join(Words['verbs']['future'])}'
verb_Trans[finite=false, ANIM=true] -> '{"'|'".join(Words['verbs']['finite'])}'

# EMBED TRANSITIVE (ANIMATE)
embedverb_Trans[finite=true, TENSE=pres,  NUM=sg, PERS=1, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['plural'])}'
embedverb_Trans[finite=true, TENSE=pres,  NUM=sg, PERS=2, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['plural'])}'
embedverb_Trans[finite=true, TENSE=pres,  NUM=sg, PERS=3, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['singular'])}'
embedverb_Trans[finite=true, TENSE=pres,  NUM=pl, ANIM=true] -> '{"'|'".join(Words['verbs']['present']['plural'])}'
embedverb_Trans[finite=true, TENSE=past, ANIM=true] -> '{"'|'".join(Words['verbs']['past'])}'
embedverb_Trans[finite=true, TENSE=future, ANIM=true] -> '{"'|'".join(Words['verbs']['future'])}'
embedverb_Trans[finite=false, ANIM=true] -> '{"'|'".join(Words['verbs']['finite'])}'

verb_Matrix[finite=true, TENSE=pres,  NUM=sg, PERS=1, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['present']['plural'])}'
verb_Matrix[finite=true, TENSE=pres,  NUM=sg, PERS=2, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['present']['plural'])}'
verb_Matrix[finite=true, TENSE=pres,  NUM=sg, PERS=3, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['present']['singular'])}'
verb_Matrix[finite=true, TENSE=pres,  NUM=pl, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['present']['plural'])}'
verb_Matrix[finite=true, TENSE=past, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['past'])}'
verb_Matrix[finite=true, TENSE=future, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['future'])}'
verb_Matrix[finite=false, ANIM=true] -> '{"'|'".join(Words['matrix_verbs']['finite'])}'

# Other
P -> '{"'|'".join(Words['loc_preps'])}'

do_Aux[TENSE=pres, NUM=sg, PERS=1] -> 'do'
do_Aux[TENSE=pres, NUM=sg, PERS=2] -> 'do'
do_Aux[TENSE=pres, NUM=sg, PERS=3] -> 'does'
do_Aux[TENSE=pres, NUM=pl] -> 'do'
do_Aux[TENSE=past] -> 'did'
do_Aux[TENSE=future, NUM=pl] -> 'will'

rel_That -> 'that'
rel_Whether -> 'whether'
rel_which -> 'which'
rel_who -> 'who'
Which -> 'which'

possN[NUM=sg, GEN=f, PERS=3, ANIM=true] -> 'mother'
possN[NUM=sg, GEN=m, PERS=3, ANIM=true] -> 'father'
possN[NUM=sg, GEN=f, PERS=3, ANIM=true] -> 'sister'
possN[NUM=sg, GEN=m, PERS=3, ANIM=true] -> 'brother'
possN[NUM=pl, GEN=f, PERS=3, ANIM=true] -> 'sisters'
possN[NUM=pl, GEN=m, PERS=3, ANIM=true] -> 'brothers'
possN[NUM=sg, GEN=f, PERS=3, ANIM=false] -> 'cat'
possN[NUM=sg, GEN=m, PERS=3, ANIM=false] -> 'dog'
possN[NUM=pl, GEN=f, PERS=3, ANIM=false] -> 'cats'
possN[NUM=pl, GEN=m, PERS=3, ANIM=false] -> 'dogs'
"""

with open(fn_grammar, 'w') as f:
    f.write(grammar)
