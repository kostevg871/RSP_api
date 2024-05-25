from fastapi import HTTPException
import rsp

property_dim_si = {
    "T": "K",
    "P": "Pa",
    "D": "kg*m^-3",
    "V": "m^3*kg^-1",
    "U": "J*kg^-1",
    "S": "J*kg^-1*K^-1",
    "H": "J*kg^-1",
    "G": "J*kg^-1",
    "F": "J*kg^-1",
    "CV": "J*kg^-1*K^-1",
    "CP": "J*kg^-1*K^-1",
    "W": "m*s^-1",
    "K": "",
    "KINVIS": "m^2*s^-1",
    "DYNVIS": "Pa*",
    "THERMCOND": "Wt*m^-1",
    "PRANDTLE": "",
    "JOULETHOMPSON": "",
    "X": "",
    
    "TS": "K",
    "PS": "Pa",

    "DSS": "kg*m^-3",
    "VSS": "m^3*kg^-1",
    "USS": "J*kg^-1",
    "SSS": "J*kg^-1*K^-1",
    "HSS": "J*kg^-1",
    "GSS": "J*kg^-1",
    "FSS": "J*kg^-1",
    "CVSS": "J*kg^-1*K^-1",
    "CPSS": "J*kg^-1*K^-1",
    "WSS": "m*s^-1",
    "KSS": "",
    "KINVISSS": "m^2*s^-1",
    "DYNVISSS": "Pa*",
    "THERMCONDSS": "Wt*m^-1",
    "PRANDTLESS": "",
    "JOULETHOMPSONSS": "",

    "DSW": "kg*m^-3",
    "VSW": "m^3*kg^-1",
    "USW": "J*kg^-1",
    "SSW": "J*kg^-1*K^-1",
    "HSW": "J*kg^-1",
    "GSW": "J*kg^-1",
    "FSW": "J*kg^-1",
    "CVSW": "J*kg^-1*K^-1",
    "CPSW": "J*kg^-1*K^-1",
    "WSW": "m*s^-1",
    "KSW": "",
    "KINVISSW": "m^2*s^-1",
    "DYNVISSW": "Pa*",
    "THERMCONDSW": "Wt*m^-1",
    "PRANDTLESW": "",
    "JOULETHOMPSONSW": "",
}


def rsp_callProperty(
        substance: rsp.Substance,
        property: str,
        mode: str,
        values: list[float],
        der_literals: list[str] = [""]
):
    val = 0.

    try:
        val = float(rsp.callProperty(
            substance,
            property,
            mode,
            values,
            rsp.VectorString(der_literals)
        ))
    except RuntimeError as e:
        raise HTTPException(
            status_code=500, detail='RSP core error: {}'.format(e))
    # except Exception as e:
        # raise HTTPException(
        # status_code=500, detail='Unknown RSP core error: {}'.format(e))

    return val


class data_get_calc_modes_info():
    def __init__(self, value: str, filter_params: str):
        self.value = value
        self.filter_params = filter_params


class data_get_available_substances():
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
        self.data_get_calc_modes_info: list = []

        # список объектов для getPropertiesLists
        self.data_get_properties_lists = []

        # список доступных свойств для каждого режима вычисления по веществам
        self.available_properties = []

        self.properties = []

        # список словарей режимов вычисления по каждому веществу (ключ - режим, значение - массив с названиями параметров)
        self.mode_descriptions = []

        # список пояснений для доступных свойств для каждого режима вычисления по веществам
        self.properties_descriptions = []

        for subst, i in zip(self.substances_names, range(len(self.substances_names))):
            # создаем объекты веществ
            self.substances_objects.append(rsp.createSubstance(subst))

            # заполняем список объектов для getAvailableSubstances
            self.data_get_substances_list.append(
                data_get_available_substances(str(i), subst))

            # получаем информацию о текущем веществе (список доступных режимов вычисления и свойств)
            self.substances_info.append(rsp.info.SubstanceInfo())
            rsp.info.getSubstanceInfo(
                self.substances_objects[i], self.substances_info[i])

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
            self.mode_descriptions.append(rsp.info.InfoTable())

            self.substances_info[i].getInfoTables(
                properties, prop_descriptions, self.mode_descriptions[i])

            # доступные свойства
            self.available_properties.append(properties)

            # пояснение к свойствам
            self.properties_descriptions.append(prop_descriptions)

            self.properties.append({})
            for mode in self.mode_descriptions[i].keys():
                # self.properties[i] = {}
                self.properties[i][str(mode)] = dict(zip(
                    list(self.available_properties[i][str(mode)]),
                    list(self.properties_descriptions[i][str(mode)])
                ))
                # убираем из списка доступных свойств производные, потому что для них свой запрос
                if 'DZDXY' in self.properties[i][str(mode)].keys():
                    del self.properties[i][str(mode)]['DZDXY']
                if 'DZDXYSS' in self.properties[i][str(mode)].keys():
                    del self.properties[i][str(mode)]['DZDXYSS']
                if 'DZDXYSW' in self.properties[i][str(mode)].keys():
                    del self.properties[i][str(mode)]['DZDXYSW']

            # режимы вычисления
            self.substances_calc_modes_id.append([])
            for mode_id in self.mode_descriptions[i].keys():
                self.substances_calc_modes_id[i].append(str(mode_id))

            # пояснения к режимам вычисления
            self.substances_calc_modes_descriptions.append([])
            for descriptions in self.mode_descriptions[i].values():
                self.substances_calc_modes_descriptions[i].append([])
                for description in descriptions:
                    self.substances_calc_modes_descriptions[i][-1].append(
                        str(description))

            # массив для getCalcModesInfo
            self.data_get_calc_modes_info.append([])
            for j in range(len(self.substances_calc_modes_id[i])):
                self.data_get_calc_modes_info[i].append(data_get_calc_modes_info(str(self.substances_calc_modes_id[i][j]),
                                                                                 self.substances_calc_modes_descriptions[i][j]))
