
grammar_rules = ""

# SVOs
grammar_rules += f"""
S[GROUP=?e] -> subjNP[NUM=?n, PERS=?p, ANIM=?a] VP[NUM=?n, PERS=?p, ANIM=?a, GROUP=?e]
"""
## verb
grammar_rules += f"""
VP[NUM=?n, PERS=?p, ANIM=?a, GROUP=sv] -> verb_Intrans[finite=true, NUM=?n, PERS=?p, ANIM=?a]
VP[NUM=?n, PERS=?p, ANIM=?a, GROUP=svo] -> verb_Trans[finite=true, NUM=?n, PERS=?p, ANIM=?a] objNP
"""
## nouns
for role in ["subj", "obj"]:
    grammar_rules += f"""
# subject
{role}NP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> {role}_PropN[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
{role}NP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> Det {role}_N[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
{role}NP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> quantifier_subj[NUM=?n, PERS=?p] {role}_N[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
{role}NP[NUM=?n, PERS=?p, GEN=?g, ANIM=?a] -> {role}_PRO[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
"""

# BINDING
## Binding (reflexives)
grammar_rules += f"""
S[GROUP=?e] -> subjNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] objPRO[GROUP=?e, NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
objPRO[GROUP=binding_reflexives, NUM=?n, GEN=?g, PERS=?p, ANIM=?a] -> obj_PRO[NUM=?n, GEN=?g, PERS=?p, ANIM=?a, BOUND=true]
"""
## Binding (possessives)
grammar_rules += f"""
S[GROUP=?e] -> subjNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] possObjNP[GROUP=?e]
S[GROUP=?e] -> possSubjNP[GROUP=?e, NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] objNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
"""
### possNP
for role in ["subj", "obj"]:
    grammar_rules += f"""
poss{role.capitalize()}NP[GROUP=possessive_{role}, NUM=?n, GEN=?g, PERS=?p, ANIM=?a, possNUM=?pn, possGEN=?pg, possPERS=?pp] -> poss_{role}[possNUM=?pn, possGEN=?pg, possPERS=?pp, BOUND=TESTFEATUREMATCH] possN[NUM=?n, GEN=?g, ANIM=?a, PERS=?p]
"""

# QUESTIONS #
grammar_rules += f"""

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
"""

# Long-Range Agreement #
grammar_rules += f"""
S[GROUP=?e] -> Det subj_N[NUM=?n, ANIM=?a, PERS=?p] nestedPP[GROUP=?e] verb_Intrans[TENSE=pres, NUM=?n, ANIM=?a, PERS=?p]
nestedPP[GROUP=pp] -> P Det embedsubj_N[GROUP=pp]
"""

# EMBEDDINGS #
## object RCs
grammar_rules += f"""
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=3, ANIM=true] rel_That Objrel[GROUP=?g] verb_Intrans[finite=true, TENSE=pres, NUM=?n, PERS=3, ANIM=true]
Objrel[GROUP=objrel] -> Det embedsubj_N[NUM=?n, ANIM=true, GROUP=objrel] embedverb_Trans[finite=true, NUM=?n, TENSE=pres, PERS=3]
"""
## subject RCs
grammar_rules += f"""
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=3, ANIM=true] rel_That Subjrel[NUM=?n, PERS=3, ANIM=true, GROUP=?g] verb_Intrans[finite=true, TENSE=pres, NUM=?n, PERS=3, ANIM=true]
Subjrel[NUM=?n, PERS=3, ANIM=true, GROUP=subjrel] -> embedverb_Trans[finite=true, NUM=?n, TENSE=pres, PERS=3] Det embedsubj_N[NUM=?n, ANIM=true, GROUP=subjrel]
"""
## Embedding
grammar_rules += f"""
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=?p, ANIM=true] verb_Matrix[finite=true, NUM=?n, PERS=?p, ANIM=true] nestedClause[GROUP=?g]
nestedClause[GROUP=embed_that_clause] -> rel_That Det embedsubj_N[NUM=?n, GROUP=embed_clause] embedverb_Intrans[finite=true, NUM=?n, PERS=3]
nestedClause[GROUP=embed_whether_clause] -> rel_Whether Det embedsubj_N[NUM=?n, GROUP=embed_clause] embedverb_Intrans[finite=true, NUM=?n, PERS=3]
nestedClause[GROUP=embed_subjwho_clause] -> rel_who embedverb_Trans[finite=true, NUM=sg, PERS=3, ANIM=true] Det embedobj_N
nestedClause[GROUP=embed_objwho_clause] -> nestedbjWh[GROUP=?e, NUM=?n, PERS=?p] embedverb_Trans[finite=true, NUM=?n, PERS=?p, ANIM=true]
nestedbjWh[GROUP=embed_objwho_clause, NUM=?n, PERS=?p] -> obj_WH Det embedsubj_N[NUM=?n, PERS=?p, ANIM=true]
nestedClause[GROUP=embed_which_clause] -> rel_which embedsubj_N[NUM=?n] embedverb_Intrans[finite=true, NUM=?n, PERS=3]
"""

fn_grammar = 'grammars/grammar.fcfg'
with open(fn_grammar, 'w') as f:
    f.write(grammar)
