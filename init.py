from libs import rsp


class data:
    def __init__(self, value: str, label: str):
        self.value = value
        self.label = label


class InitRSP:
    def __init__(self):
        # список объектов веществ (в которых методы для вычисления свойств)
        self.substances_objects = []

        # список информационных контейнеров по каждому веществу
        self.substances_info = []

        # список доступных режимов вычисления для каждого вещества
        self.substances_calc_modes_id = []

        # список пояснений к режимам вычисления
        self.substances_calc_modes_descriptions = []

        # вектор строковых имен веществ ("H2O_IF97", "N2", "CO2" ...)
        self.substances_names = rsp.VectorString()

        # список объектов для getAvailableSubstances
        self.data_get_substances_list = []

        # получаем из бибилиотеки наименования доступных веществ
        rsp.info.getAvailableSubstances(self.substances_names)

        # двумерный список объектов для getCalcModesInfo (первая размерность конкретное вещество, вторая размерность - конкретный режим вычислений)
        self.data_get_calc_modes_info = []

        # список объектов для getPropertiesLists
        self.data_get_properties_lists = []

        # список доступных свойств для каждого режима вычисления по веществам
        self.available_properties = []
        
        self.properties = []

        # список пояснений для доступных свойств для каждого режима вычисления по веществам
        self.properties_descriptions = []

        for subst, i in zip(self.substances_names, range(len(self.substances_names))):
            # создаем объекты веществ
            self.substances_objects.append(rsp.createSubstance(subst))

            # заполняем список объектов для getAvailableSubstances
            self.data_get_substances_list.append(data(str(i), subst))

            # получаем информацию о текущем веществе (список доступных режимов вычисления и свойств)
            self.substances_info.append(rsp.info.SubstanceInfo())
            rsp.info.getSubstanceInfo(self.substances_objects[i], self.substances_info[i])
            
            # # получаем информацию о доступных режимах вычиления для данного вещества
            # modes = rsp.VectorString()
            # self.substances_info[i].getCalcModesInfo(modes)
            # self.substances_calc_modes_id.append(modes)

            # mode_descriptions = rsp.info.InfoTable()
            # self.substances_info[i].getModeDecomposition(mode_descriptions)

            # self.substances_calc_modes_descriptions.append(mode_descriptions)

            # # заполняем список объектов для getCalcModesInfo
            # self.data_get_calc_modes_info.append([])
            # for j in range(len(modes)):
            #     self.data_get_calc_modes_info[i].append(data(modes[j], mode_descriptions[modes[j]]))

            
            # объявляем информационную таблицу для литералов свойств (ассоциативный массив, 
            # в котором ключ - литерал режима вычисления, а значение - соответствуюющий массив
            # доступных для вычисления свойств)
            properties = rsp.info.InfoTable()

            # объявляем информационную таблицу для пояснений литералов свойств (ассоциативный массив, 
            # в котором ключ - литерал режима вычисления, а значение - соответствуюющий массив
            # доступных для вычисления свойств). Например, литералу 'D' соотвтетсвует пояснение 'Density'
            prop_descriptions = rsp.info.InfoTable()

            # объявляем информационную таблицу для пояснений литералов режимов вычисления (ассоциативный массив, 
            # в котором ключ - литерал режима вычисления, а значение - пояснение соответствующих параметров: для 
            # "PT": ["Pressure", "Temperature"]).
            mode_descriptions = rsp.info.InfoTable()

            self.substances_info[i].getInfoTables(properties, prop_descriptions, mode_descriptions)

            # доступные свойства  
            self.available_properties.append(properties)

            # пояснение к свойствам
            self.properties_descriptions.append(prop_descriptions)

            self.properties.append({})
            for mode in mode_descriptions.keys():
                # self.properties[i] = {}
                self.properties[i][str(mode)] = dict(zip(
                    list(self.available_properties[i][str(mode)]),
                    list(self.properties_descriptions[i][str(mode)])
            ))

            # # массив для getPropertiesLists
            # self.data_get_properties_lists.append([])
            # for property, description in zip(self.available_properties[i], self.properties_descriptions[i]):
            #      self.data_get_properties_lists[i].append(data(str(property),str(description)))

            # режимы вычисления
            self.substances_calc_modes_id.append([])
            for mode_id in mode_descriptions.keys():
                self.substances_calc_modes_id[i].append(str(mode_id))

            # пояснения к режимам вычисления
            self.substances_calc_modes_descriptions.append([])
            for descriptions in mode_descriptions.values():
                self.substances_calc_modes_descriptions[i].append([])
                for description in descriptions:
                    self.substances_calc_modes_descriptions[i][-1].append(str(description))

            # массив для getCalcModesInfo
            self.data_get_calc_modes_info.append([])
            for j in range(len(self.substances_calc_modes_id[i])):
                self.data_get_calc_modes_info[i].append(data(str(self.substances_calc_modes_id[i][j]), str(self.substances_calc_modes_descriptions[i][j])))
