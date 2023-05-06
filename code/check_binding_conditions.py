def get_agreement_match(row, role1, role2):
    agreement_match = {}
    for feature in ["GEN", "NUM", "ANIM"]:
        agreement_match[feature] = row[f"{role1}_{feature}"] == row[f"{role2}_{feature}"]
    return agreement_match


def calc_single_binding(row, pronoun_type: str):
    # pronoun_type is from: ["PRO", "POSS"]
    agreement_match = None
    valid_conditionA = None
    valid_conditionB = None
    valid_conditionC = None
    binding_quantifier = None
    binding_pronoun = None
    if row["subj_type"] == pronoun_type:
        if not (row["obj_type"] is None):  # TODO: does that work for empty values?
            agreement_match = get_agreement_match(row, "subj", "obj")
            # valid_conditionA not relevant: no reflexive in subject position
            valid_conditionB = True
            valid_conditionC = False
    # PRO=obj, DP=subj
    if row["obj_type"] == pronoun_type:
        agreement_match = get_agreement_match(row, "obj", "subj")
        if row["obj_REFL"] == "true":
            valid_conditionA = True
        else:
            valid_conditionB = False
        valid_conditionC = True
        if row["quantifier"] is not None:
        # Can we do something like: if row["subj_quantifier"] == "quantifier":
            binding_quantifier = (row["quantifier"] is not None)
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
            if prop == "agreement_match" and (val is not None):
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
