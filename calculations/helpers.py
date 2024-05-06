import rsp


def get_calc_model_subs():
    substances = rsp.VectorString()
    rsp.info.getAvailableSubstances(substances)
    return list(substances)
