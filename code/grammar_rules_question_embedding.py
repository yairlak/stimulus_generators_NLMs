grammar_rules = """ \

# Main clause
VP[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> verb_Intrans[finite=?f, NUM=?n, ANIM=?a, PERS=?p]
VP[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> verb_Trans[finite=?f, NUM=?n, ANIM=?a, PERS=?p] Det obj_N

S[EMBED=false, CLAUSE=that] -> Det subj_N[NUM=?n, ANIM=?a] VP[finite=true, NUM=?n, PERS=3, ANIM=?a]
S[EMBED=false, CLAUSE=whether] -> do_Aux[NUM=?n, PERS=3] Det subj_N[NUM=?n, ANIM=?a] VP[finite=false, NUM=?n, ANIM=?a, PERS=3] QM
S[EMBED=false, CLAUSE=subjwho] -> subj_who VP[finite=true, NUM=sg, PERS=3] QM
S[EMBED=false, CLAUSE=subjwhich] -> subj_which subj_N[NUM=?n, ANIM=?a] VP[finite=true, NUM=?n, PERS=3, ANIM=?a] QM
S[EMBED=false, CLAUSE=objwho] -> obj_who do_Aux[NUM=?n, PERS=3] Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=false, ANIM=?a] QM
S[EMBED=false, CLAUSE=objwhich] -> obj_which obj_N do_Aux[NUM=?n, PERS=3] Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=false, ANIM=?a] QM

# Embedded clause
embedVP[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> embedverb_Intrans[finite=?f, NUM=?n, ANIM=?a, PERS=?p]
embedVP[finite=?f, NUM=?n, ANIM=?a, PERS=?p] -> embedverb_Trans[finite=?f, NUM=?n, ANIM=?a, PERS=?p] Det embedobj_N

S[EMBED=true, CLAUSE=?c] -> Det subj_N[NUM=?n, PERS=?p, ANIM=true] verb_Matrix[finite=true, NUM=?n, PERS=?p, ANIM=true, TENSE=pres] embedS[CLAUSE=?c]

embedS[CLAUSE=that] -> rel_That Det embedsubj_N[NUM=?n, ANIM=?a] embedVP[finite=true, NUM=?n, PERS=3, ANIM=?a]
embedS[CLAUSE=whether] -> rel_Whether Det embedsubj_N[NUM=?n, ANIM=?a] embedVP[finite=true, NUM=?n, ANIM=?a, PERS=3]
embedS[CLAUSE=subjwho] -> subj_who embedVP[finite=true, NUM=sg, PERS=3]
embedS[CLAUSE=subjwhich] -> subj_which embedsubj_N[NUM=?n, ANIM=?a] embedVP[finite=true, NUM=?n, PERS=3, ANIM=?a]
embedS[CLAUSE=objwho] -> obj_who Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=true, NUM=?n, PERS=3, ANIM=?a]
embedS[CLAUSE=objwhich] -> obj_which obj_N Det subj_N[NUM=?n, ANIM=?a] verb_Trans[finite=true, NUM=?n, PERS=3, ANIM=?a]

"""
