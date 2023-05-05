
# Current labels:
# ,sentence,
# congruent_subj_ANIM,congruent_subj_GEN,congruent_subj_NUM,congruent_subj_PERS,
# do,do_NUM,do_PERS,do_TENSE,do_type,
# subj,subj_ANIM,subj_GEN,subj_NUM,subj_PERS,subj_Quantifier,subj_type,
# verb,verb_ANIM,verb_NUM,verb_PERS,verb_TENSE,verb_finite,verb_type
# embedsubj,embedsubj_ANIM,embedsubj_GEN,embedsubj_NUM,embedsubj_PERS,embedsubj_type,
# embedverb,embedverb_ANIM,embedverb_NUM,embedverb_PERS,embedverb_TENSE,embedverb_finite,embedverb_type,
# obj,obj_ANIM,obj_BOUND,obj_GEN,obj_NUM,obj_PERS,obj_Quantifier,obj_type,
# poss,poss_BOUND,poss_GEN,poss_NUM,poss_PERS,poss_POSS,poss_type,
# rel,rel_type,sentence_ANIM,sentence_GEN,sentence_GROUP,
# sentence_NUM,sentence_PERS,

# In principle, we can assess binding conditions for all pairs (pronoun, DP)
# Some sentences have multiple pronouns, and multiple DPs. How do we deal with that?

import numpy as np

def binding_check(row):
    res = {
		"condition_A_violation": np.nan,
		"condition_B_violation": np.nan,
		"condition_C_violation": np.nan,
	}
    if row["subj_type"] == "PRO":
        if row["obj_type"].isnull() == False:
                agreement_match = {
                    feature: row[f"subj_{feature}"] == row[f"obj_{feature}"]
                    for feature in ["GEN", "NUM", "ANIM"]
                }
                condition_B_violation = False
                condition_C_violation = True

    if row["subj_type"] == "POSS":
        if row["obj_type"].isnull() == False:
            condition_C_violation = False
            condition_B_violation = False
            agreement_match = {
                feature: row[f"subj_{feature}"] == row[f"obj_{feature}"]
                for feature in ["GEN", "NUM", "ANIM"]
            }

    if row["obj_type"]=="PRO":
        condition_C_violation = False
        if row["subj_type"] == "POSS": # BETTER NOT TO ACCEPT TWO PRONOUNS FOR NOW?
        if row["obj_type"] == "PRO":
            condition_B_violation = not( PRO IS ANAPHORA )
            agreement_match = {
                feature: subj["feature"] == obj["feature"]
                for feature in ["GEN", "NUM", "ANIM"]
            }

    if row["subj_type"]=="POSS": # BETTER NOT TO ACCEPT TWO PRONOUNS FOR NOW?
