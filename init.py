import rsp


class data:
    def __init__(self, value: int, label: str):
        self.value = str(value)
        self.label = label


class InitRSP:
    def __init__(self):
        # список объектов веществ (в которых методы для вычисления свойств)
        self.substances_objects = []

        # список информационных контейнеров по каждому веществу
        self.substances_info = []

        # список доступных режимов вычисления для каждого вещества
        self.substances_calc_modes = []

        # вектор строковых имен веществ ("H2O_IF97", "N2", "CO2" ...)
        self.substances_names = rsp.VectorString()

        # список объектов для getAvailableSubstances
        self.data_get_substances_list = []

        # получаем из бибилиотеки наименования доступных веществ
        rsp.info.getAvailableSubstances(self.substances_names)

        # двумерный список объектов для getCalcModesInfo (первая размерность конкретное вещество, вторая размерность - конкретный режим вычислений)
        self.data_get_calc_modes_info = []

        #GET /getCalcModesInfo?id={}, где id - id вещества
#
        #Response - array of object
        #{
        #   value: string; //id режима
        #   label: string; //наименование режима
        #}

        i = 0
        for subst in self.substances_names:
            # создаем объекты веществ
            self.substances_objects.append(rsp.createSubstance(subst))

            # заполняем список объектов для getAvailableSubstances
            self.data_get_substances_list.append(data(i, subst))

            # получаем информацию о текущем веществе (список доступных режимов вычисления и свойств)
            self.substances_info.append(rsp.info.SubstanceInfo())
            rsp.info.getSubstanceInfo(self.substances_objects[i], self.substances_info[i])
            
            # получаем информацию о доступных режимах вычиления для данного вещества
            modes = rsp.VectorString()
            self.substances_info[i].getCalcModesInfo(modes)
            self.substances_calc_modes.append(modes)

            # заполняем список объектов для getCalcModesInfo
            self.data_get_calc_modes_info.append([])
            for j in range(len(modes)):
                self.data_get_calc_modes_info[i].append(data(j, modes[j]))

            i = i + 1
