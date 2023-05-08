grammar_rules = """ \
# SVOs

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
objNP -> obj_PRO[REFL=false]

# BINDING

# Binding (reflexives)
S[GROUP=?e] -> subjNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, NUM=?n, PERS=?p, ANIM=?a] objPRO[GROUP=?e, NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
objPRO[GROUP=binding_reflexives, NUM=?n, GEN=?g, PERS=?p, ANIM=?a] -> obj_PRO[NUM=?n, GEN=?g, PERS=?p, ANIM=?a, REFL=true]

# Binding (possessives)
S[GROUP=?e] -> subjNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] possObjNP[GROUP=?e]
S[GROUP=?e] -> possSubjNP[GROUP=?e, NUM=?n, GEN=?g, PERS=?p, ANIM=?a] verb_Trans[finite=true, TENSE=?t, NUM=?n, PERS=?p, ANIM=?a] objNP[NUM=?n, GEN=?g, PERS=?p, ANIM=?a]
possSubjNP[GROUP=possessive_subj, NUM=?n, GEN=?g, PERS=?p, ANIM=?a, possNUM=?pn, possGEN=?pg, possPERS=?pp] -> poss_subj[possNUM=?pn, possGEN=?pg, possPERS=?pp] subj_N[NUM=?n, GEN=?g, ANIM=?a, PERS=?p, REL=true]
possObjNP[GROUP=possessive_obj, NUM=?n, GEN=?g, PERS=?p, ANIM=?a, possNUM=?pn, possGEN=?pg, possPERS=?pp] -> poss_obj[possNUM=?pn, possGEN=?pg, possPERS=?pp] obj_N[NUM=?n, GEN=?g, ANIM=?a, PERS=?p, REL=true]

# ASSERTIONS AND QUESTIONS

# Main clause
VPthe[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> verb_Intrans[finite=?f, NUM=?n, ANIM=?a, PERS=?p]
VPthe[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> verb_Trans[finite=?f, NUM=?n, ANIM=?a, PERS=?p] Det obj_N

# Sentences of the first type below are already in:
# S[GROUP=main_that_clause] -> Det subj_N[NUM=?n, ANIM=?a] VPthe[finite=true, NUM=?n, PERS=3, ANIM=?a]
S[GROUP=main_whether_clause] -> do_Aux[NUM=?n, PERS=3] Det subj_N[NUM=?n, ANIM=?a] VPthe[finite=false, NUM=?n, ANIM=?a, PERS=3]
S[GROUP=main_subjwho_clause] -> subj_who VPthe[finite=true, NUM=sg, PERS=3]
S[GROUP=main_subjwhich_clause] -> subj_which subj_N[NUM=?n, ANIM=?a] VPthe[finite=true, NUM=?n, PERS=3, ANIM=?a]
S[GROUP=main_objwho_clause] -> obj_who do_Aux[NUM=?n, PERS=3] Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=false, ANIM=?a]
S[GROUP=main_objwhich_clause] -> obj_which obj_N do_Aux[NUM=?n, PERS=3] Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=false, ANIM=?a]

# Embedded clause
embedVPthe[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> embedverb_Intrans[finite=?f, NUM=?n, ANIM=?a, PERS=?p]
embedVPthe[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> embedverb_Trans[finite=?f, NUM=?n, ANIM=?a, PERS=?p] Det embedobj_N

S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=?p, ANIM=true] verb_Matrix[finite=true, NUM=?n, PERS=?p, ANIM=true] embedS[GROUP=?g]

embedS[GROUP=embed_that_clause] -> rel_That Det embedsubj_N[NUM=?n, ANIM=?a] embedVPthe[finite=true, NUM=?n, PERS=3, ANIM=?a]
embedS[GROUP=embed_whether_clause] -> rel_Whether Det embedsubj_N[NUM=?n, ANIM=?a] embedVPthe[finite=false, NUM=?n, ANIM=?a, PERS=3]
embedS[GROUP=embed_subjwho_clause] -> subj_who embedVPthe[finite=true, NUM=sg, PERS=3]
embedS[GROUP=embed_subjwhich_clause] -> subj_which embedsubj_N[NUM=?n, ANIM=?a] embedVPthe[finite=true, NUM=?n, PERS=3, ANIM=?a]
embedS[GROUP=embed_objwho_clause] -> obj_who Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=true, NUM=?n, PERS=3, ANIM=?a]
embedS[GROUP=embed_objwhich_clause] -> obj_which obj_N Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=true, NUM=?n, PERS=3, ANIM=?a]

# LONG-RANGE AGREEMENT

S[GROUP=?e] -> Det subj_N[NUM=?n, ANIM=?a, PERS=?p] embedPP[GROUP=?e] verb_Intrans[TENSE=pres, NUM=?n, ANIM=?a, PERS=?p]
embedPP[GROUP=pp] -> P Det embedsubj_N[GROUP=pp]

# EMBEDDINGS

# object RCs
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=3, ANIM=true] rel_That Objrel[GROUP=?g] verb_Intrans[finite=true, TENSE=pres, NUM=?n, PERS=3, ANIM=true]
Objrel[GROUP=objrel] -> Det embedsubj_N[NUM=?n, ANIM=true, GROUP=objrel] embedverb_Trans[finite=true, NUM=?n, TENSE=pres, PERS=3]

# subject RCs
S[GROUP=?g] -> Det subj_N[NUM=?n, PERS=3, ANIM=true] rel_That Subjrel[NUM=?n, PERS=3, ANIM=true, GROUP=?g] verb_Intrans[finite=true, TENSE=pres, NUM=?n, PERS=3, ANIM=true]
Subjrel[NUM=?n, PERS=3, ANIM=true, GROUP=subjrel] -> embedverb_Trans[finite=true, NUM=?n, TENSE=pres, PERS=3] Det embedobj_N[ANIM=true, GROUP=subjrel]

"""
