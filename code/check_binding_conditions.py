import numpy as np
import pandas as pd

def get_agreement_match(row, role1, role2):
    agreement_match = {}
    for feature in ["GEN", "NUM", "ANIM"]:
        agreement_match[feature] = row[f"{role1}_{feature}"] == row[f"{role2}_{feature}"]
    return agreement_match


def calc_single_binding(row, pronoun_type: str):
    # pronoun_type is from: ["PRO", "POSS"]
    agreement_match = np.nan
    valid_conditionA = np.nan
    valid_conditionB = np.nan
    valid_conditionC = np.nan
    binding_quantifier = np.nan
    binding_pronoun = np.nan

    subj_type, obj_type = row["subj_type"], row["obj_type"]
    if row["poss_type"] == "subj":
        subj_type = "POSS"
    if row["poss_type"] == "obj":
        obj_type = "POSS"

    if subj_type == pronoun_type:
        if not pd.isnull(row["obj_type"]):
            agreement_match = get_agreement_match(row, "subj", "obj")
            # valid_conditionA not relevant: no reflexive in subject position
            valid_conditionB = True
            if pronoun_type == "POSS":
                valid_conditionC = True
            else:
                valid_conditionC = False
    if obj_type == pronoun_type:
        agreement_match = get_agreement_match(row, "obj", "subj")
        if row["obj_REFL"] == "true":
            valid_conditionA = True
        else:
            valid_conditionB = False
        valid_conditionC = True
        if not pd.isnull(row["quantifier"]):
        # Can we do something like: if row["subj_quantifier"] == "quantifier":
            binding_quantifier = (not pd.isnull(row["quantifier"]))
        if row["subj_type"] == "PRO":
            binding_pronoun = True
    res = {
        "agreement_match": agreement_match,
        "valid_conditionA": valid_conditionA,
        "valid_conditionB": valid_conditionB,
        "valid_conditionC": valid_conditionC,
        "binding_quantifier": binding_quantifier,
        "binding_pronoun": binding_pronoun
    }
    return res


def format_binding(bindings):
    res = {}
    for pronoun_type, binding in bindings.items():
        for prop, val in binding.items():
            if prop == "agreement_match" and (not pd.isnull(val)):
                for feature, val2 in val.items():
                    res[f"{pronoun_type}_congruence_{feature}"] = val2
            else:
                res[f"{pronoun_type}_{prop}"] = val
    return res


def calc_binding(row):
    bindings = {}
    bindings["pro"] = calc_single_binding(row, pronoun_type="PRO")
    bindings["poss"] = calc_single_binding(row, pronoun_type="POSS")
    res = format_binding(bindings)
    return res
