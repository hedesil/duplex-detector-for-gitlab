from fuzzywuzzy import process, fuzz
from functools import partial
from operator import itemgetter
import json


class ComponentCoincidences:

    def __init__(self, component_name, coincidences_list, have_coincidences, creation_date, last_modification_date):
        self.component_name = component_name
        self.coincidences_list = coincidences_list
        self.have_coincidences = have_coincidences
        self.creation_date = creation_date
        self.last_modification_date = last_modification_date

    def __repr__(self):
        return "" + str(self.component_name) + str(self.coincidences_list) + str(self.have_coincidences)


class RepositoriesCoincidencesByName:
    # Función que recibe un array de componentes y devuelve un diccionario con índice, project_name y short_name de cada
    # componente
    @staticmethod
    def __get_options(array):
        my_dict = {}
        count = 1
        for item in array:
            my_dict[count] = {'names': [item['project_name'], item['short_name']]}
            count += 1
        return my_dict

    # Método que acepta el diccionario con posibles coincidencias, el diccionario nombre / alias y un número de corte
    # para retornar una lista con las coincidencias que cumplan el umbral mínimo seleccionado en cutoff.
    @staticmethod
    def __score_cuttof(matches_4_repository, names_alias_dictionary, cutoff):
        matches_score_cutoff = []
        for match in matches_4_repository:
            if matches_4_repository[match][1] > cutoff:
                tiny_dict = {"name": names_alias_dictionary[match]['names'][0],
                             "percent": matches_4_repository[match][1]}
                matches_score_cutoff.append(tiny_dict)
        return matches_score_cutoff

    @staticmethod
    def __delete_self_repository_coincidence(name, coincidences_list):
        for ratio in coincidences_list:
            if ratio['name'] == name:  # component['project_name']:
                coincidences_list.remove(ratio)
            return coincidences_list

    # Función que determina si un componente tiene posibilidad de estar duplicado o no en base a si el array de
    # coincidencias está vacío o tiene algún elemento.
    @staticmethod
    def __get_coincidences(ratios_list):
        if len(ratios_list) > 1:
            possible_coincidences = True
        else:
            possible_coincidences = False
        return possible_coincidences

    # Funcion que utiliza una lista de repositorios de GitLab para devolver una lista de los mismos repositorios con sus
    # posibles coincidencias por un encima de un umbral
    @staticmethod
    def get_repositories_list_with_coincidences(_components_array, cutoff_percent=70):
        final_components_list = []
        # Invoco a la función que trae el diccionario con índice, project_name y short_name de cada componente
        # Ejemplo: { 1: {'names': ['FUN_ANG_EXAMPLE', 'EXAMPLE']}, 2: {'names': ['FUN_ANG_EXAMPLE2', 'EXAMPLE2']}}
        names_dictionary = RepositoriesCoincidencesByName.__get_options(_components_array)

        # Itero sobre el array completo de componentes ya que quiero comparar el nombre de cada componente con el nombre de
        # cada uno de los demás componentes para saber en que porcentaje coinciden
        for component in _components_array:
            # input_str será el nombre corto del componente (sin los prefijos FUN_, FRONTALUNIFICADO_, etc)
            input_str = component['short_name']

            # Creo una función parcial que combina el ratio de la libreria fuzzy_wuzzy usando el input_str para comparar
            fuzzy_wuzzy = partial(fuzz.ratio, input_str)

            # Primero: genero un nuevo diccionario a partir del anterior únicamente los short_name manteniendo los índices
            # originales para saber regoger más tarde el project_name.
            # Ejemplo: {1: 'EXAMPLE', 2: 'EXAMPLE2'}
            short_name_dict = {k: names_dictionary[k]['names'][1] for k in names_dictionary}

            # Segundo: a cada elemento del nuevo diccionario le aplico la función ratio de comparar con el input_str,
            # generando así un nuevo diccionario con el index origen, el short_name comparado y el porcentaje.
            # Ejemplo: {1: (EXAMPLE, 90), 2: (EXAMPLE2, 80)}
            matches = {i: (short_name_dict[i], fuzzy_wuzzy(short_name_dict[i])) for i in short_name_dict}

            # Tercero: recorro diccionario anterior con el objetivo de generar una lista con el nombre original del
            # repositorio y su porcentaje de concidencia con el actual. Además se va a aplicar un umbral mínimo de
            # coincidencia del 73% de concidencia (según fuzz.ratio)
            matches_score_cutoff = RepositoriesCoincidencesByName.__score_cuttof(matches, names_dictionary,
                                                                                 cutoff_percent)

            # Cuarto: Se genera y ordena una lista repositorios que tienen más de un % de coincidencia con el
            # repositorio de esta interaccion (input_str) incluido él mismo
            ratios_list = sorted(matches_score_cutoff, key=itemgetter('percent'), reverse=True)

            # Elimino del array la coincidencia del 100% que tiene el componente de esta interacción consigo mismo
            # EJ: Si estoy comparando FUN_ANG_EXAMPLE elimino FUN_ANG_EXAMPLE del array de coincidencias.
            ratios_list = RepositoriesCoincidencesByName.__delete_self_repository_coincidence(component['project_name'],
                                                                                              ratios_list)

            have_coincidences = RepositoriesCoincidencesByName.__get_coincidences(ratios_list)

            component_instance = ComponentCoincidences(component['project_name'], ratios_list, have_coincidences,
                                                       component["creation_date"], component["last_activity_date"])
            component_dictionary = {
                "name": component_instance.component_name,
                "coincidences_list": component_instance.coincidences_list,
                "creation_date": component_instance.creation_date,
                "last_activity_date": component_instance.last_modification_date,
                "have_coincidences": component_instance.have_coincidences
            }

            final_components_list.append(component_dictionary)

        return json.dumps(final_components_list)
