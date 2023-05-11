import numpy as np
import pandas as pd
import utils


def calc_simple_binding(row):
    bound_variable = np.nan
    coref_variable = np.nan
    if not (row["sentence_GROUP"] in ["svo", "binding_reflexives", "possessive_obj", "possessive_subj"]):
        pass
    elif pd.isnull(row['quantifier']):
        if (row['subj_type'] == "PRO"):
            coref_variable = (row["obj_REFL"] == "True")
        elif (row['poss_type'] == "subj"):
            agreement_mismatch = utils.get_agreement_mismatch(row, "poss", "obj")
            coref_variable = not agreement_mismatch["overall"]
        elif (row['obj_type'] in "PRO"):
            coref_variable = (row["obj_REFL"] == "True")
        elif (row['poss_type'] == "obj"):
            agreement_mismatch = utils.get_agreement_mismatch(row, "poss", "subj")
            coref_variable = not agreement_mismatch["overall"]
    elif not (pd.isnull(row['quantifier'])):
        if (row['obj_type'] == "PRO"):
            bound_variable = (row["obj_REFL"] == "True")
        elif (row['poss_type'] == "obj"):
            agreement_mismatch = utils.get_agreement_mismatch(row, "poss", "subj")
            bound_variable = not agreement_mismatch["overall"]
    return {
        'bound_variable': bound_variable,
        'coref_variable': coref_variable}


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
            agreement_mismatch = utils.get_agreement_mismatch(row, pronoun_position, target_position)
            agreement_match = not agreement_mismatch
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
            agreement_mismatch = utils.get_agreement_mismatch(row, "poss_N", target_position)
            agreement_match = not agreement_mismatch
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