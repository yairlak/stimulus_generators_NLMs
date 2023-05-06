import numpy as np
import pandas as pd


def get_agreement_match(row, role1, role2):
    agreement_match = {}
    agr_features = ["GEN", "NUM", "PERS", "ANIM"]
    for feature in agr_features:
        agreement_match[feature] = (
            (row[f"{role1}_{feature}"] == row[f"{role2}_{feature}"])
            or (pd.isnull(row[f"{role1}_{feature}"]))
            or (pd.isnull(row[f"{role2}_{feature}"]))
        )
    agreement_match["all"] = all(agreement_match[feature] for feature in agr_features)
    return agreement_match


def calc_single_binding(row, pronoun_position: str, target_position: str):
    pronoun_type = np.nan
    agreement_match = np.nan
    valid_conditionA = np.nan
    valid_conditionB = np.nan
    valid_conditionC = np.nan
    binding_quantifier = np.nan
    binding_pronoun = np.nan

    if row[f"{pronoun_position}_type"] == "PRO":
        pronoun_type = "PRO"
        if not pd.isnull(row[f"{target_position}_type"]):
            agreement_match = get_agreement_match(row, pronoun_position, target_position)
            valid_conditionC = (pronoun_position == "subj")
            if (pronoun_position == "obj") and row[f"{pronoun_position}_REFL"] == "true":
                pronoun_type = "REFL"
                valid_conditionA = True
            else:
                valid_conditionB = False
        binding_quantifier = (not pd.isnull(row["quantifier"]))
        binding_pronoun = (row[f"{target_position}_type"] == "PRO")

    elif row[f"{pronoun_position}_type"] == "POSS":
        pronoun_type = "POSS"
        if not pd.isnull(row[f"{target_position}_type"]):
            agreement_match = get_agreement_match(row, "poss_N", target_position)
            valid_conditionC = True
            valid_conditionB = True
            binding_quantifier = (not pd.isnull(row["quantifier"]))
            binding_pronoun = (row[f"{target_position}_type"] == "PRO")

    res = {
        "agreement_match": agreement_match,
        "valid_conditionA": valid_conditionA,
        "valid_conditionB": valid_conditionB,
        "valid_conditionC": valid_conditionC,
        "binding_quantifier": binding_quantifier,
        "binding_pronoun": binding_pronoun,
        "pronoun_type": pronoun_type
    }
    return res


def format_binding(bindings):
    res = {}
    for pronoun_type, binding in bindings.items():
        for prop, val in binding.items():
            if prop == "agreement_match":
                if not pd.isnull(val):
                    for feature, val2 in val.items():
                        res[f"{pronoun_type}_congruence_{feature}"] = val2
            else:
                res[f"{pronoun_type}_{prop}"] = val
    return res


def calc_binding(row):
    bindings = {}
    bindings["subj"] = calc_single_binding(row, pronoun_position="subj", target_position="obj")
    bindings["obj"] = calc_single_binding(row, pronoun_position="obj", target_position="subj")
    res = format_binding(bindings)
    return res
