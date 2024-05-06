import rsp


class data:
    def __init__(self, value: int, label: str):
        self.value = str(value)
        self.label = label


class InitRSP:
    def __init__(self):
        self.substances_objects = []
        self.data_get_substances_list = []
        self.substances_names = rsp.VectorString()
        rsp.info.getAvailableSubstances(self.substances_names)

        i = 0
        for subst in self.substances_names:
            self.substances_objects.append(rsp.createSubstance(subst))
            self.data_get_substances_list.append(data(i, subst))
            i = i + 1


substaneces_objects_globals = InitRSP()
