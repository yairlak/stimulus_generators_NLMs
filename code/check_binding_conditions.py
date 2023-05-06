# Current labels:
#
# sentence,sentence_GROUP,sentence_length,
# congruent_subj_ANIM,congruent_subj_GEN,congruent_subj_NUM,congruent_subj_PERS,
# contain_objrel,contain_subjrel,
# do,do_NUM,do_PERS,do_TENSE,do_type,
# subj,subj_ANIM,subj_GEN,subj_NUM,subj_PERS,subj_type,
# obj,obj_ANIM,obj_BOUND,obj_GEN,obj_NUM,obj_PERS,obj_type,
# embedobj,embedobj_ANIM,embedobj_GEN,embedobj_NUM,embedobj_PERS,embedobj_type,
# embedsubj,embedsubj_ANIM,embedsubj_GEN,embedsubj_NUM,embedsubj_PERS,embedsubj_type,
# embedverb,embedverb_ANIM,embedverb_NUM,embedverb_PERS,embedverb_TENSE,embedverb_finite,embedverb_type,
# poss,poss_BOUND,poss_GEN,poss_NUM,poss_PERS,poss_type,
# quantifier,quantifier_NUM,quantifier_type,
# rel,rel_type,
# verb,verb_ANIM,verb_NUM,verb_PERS,verb_TENSE,verb_finite,verb_type,
# has_subjrel,has_objrel,has_embed_,has_quest_
#
# In principle, we can assess binding conditions for all pairs (pronoun, DP)
# Some sentences have multiple pronouns, and multiple DPs. How do we deal with that?

def get_agreement_match(row, role1, role2):
    agreement_match = {}
    for feature in ["GEN", "NUM", "ANIM"]:
        agreement_match[feature] = row[f"{role1}_{feature}"] == row[f"{role2}_{feature}"]
    return agreement_match


def single_binding_check(row, pronoun_type: str):
    # pronoun_type is from: ["PRO", "POSS"]
    agreement_match = None
    condition_A_violation = None
    condition_B_violation = None
    condition_C_violation = None
    quantifier_binding = None
    pronoun_binding = None
    if row["subj_type"] == pronoun_type:
        if not (row["obj_type"].isnull()):
            agreement_match = get_agreement_match(row, "subj", "obj")
            #TODO: condition_A_violation =
            condition_B_violation = False
            condition_C_violation = True
    # PRO=obj, DP=subj
    if row["obj_type"] == pronoun_type:
        agreement_match = get_agreement_match(row, "obj", "subj")
        #TODO: condition_A_violation = (row["obj_REFL"] == "true")
        condition_B_violation = (row["obj_REFL"] != "true")
        condition_C_violation = False
        if row["quantifier"] is not None:
        # Can we do something like: if row["subj_quantifier"] == "quantifier":
            quantifier_binding = (row["quantifier"] is not None)
        if row["subj_type"] == "PRO":
            pronoun_binding = True
    res = {
        "agreement_match": agreement_match,
        "condition_A_violation": condition_A_violation,
        "condition_B_violation": condition_B_violation,
        "condition_C_violation": condition_C_violation,
        "quantifier_binding": quantifier_binding,
        "pronoun_binding": pronoun_binding
    }
    return res


def binding_check(row):
    bindings = {}
    bindings["pro"] = single_binding_check(row, pronoun_type="PRO")
    bindings["poss"] = single_binding_check(row, pronoun_type="POSS")
    return bindings
