import gitlab
import os
import json


class Component(object):
    def __init__(self, project_name, creation_date, last_activity_date, short_name):
        self.project_name = project_name
        self.creation_date = creation_date
        self.last_activity_date = last_activity_date
        self.short_name = short_name


# Clase que maneja la conexión a GitLab a través de una autenticación por token. Necesita el host al que se debe
# conectar y el token de autenticación generado en GitLab
class GitLabConnect(object):
    def __init__(self, gitlab_host, gitlab_token):
        self.gitlab_host = gitlab_host
        self.gitlab_token = gitlab_token

    def connect(self):
        # private token or personal token authentication
        gl = gitlab.Gitlab(self.gitlab_host, private_token=self.gitlab_token)
        # Make an API request to create the gl.user object. This is mandatory if you
        # use the username/password authentication.
        gl.auth()
        return gl


# Clase que expone varios métodos para gestionar la información a extraer de GitLab. La funcionalidad principal es
# recibir por parámetro una lista de strings para buscar repositorios en gitlab que coincidan con los criterios de
# búsqueda y exportarlos como un array de objetos JSON.
class GitlabProjects(object):
    def __init__(self, gl):
        self.gl = gl

    def find_projects_by_filters_array(self, search_array):
        projects_unified = []
        for search in search_array:
            final_list = json.loads(self.find_projects_by_filter(search))
            projects_unified = projects_unified + final_list
        return json.dumps(projects_unified)

    # Funcion que acepta por parametro un string para buscar coincidencias de repositorios en GitLab
    def find_projects_by_filter(self, search):
        frontend_projects = self.gl.projects.list(search=search, all=True)
        final_list = self.__get_projects_list(frontend_projects)
        return json.dumps(final_list)

    # Funcion que acepta por parámetro un array con los IDs de proyectos gitlab, hace una petición
    def __get_projects_list(self, projects_array):
        projects_list = []
        for f1 in projects_array:
            gitlab_project = self.gl.projects.get(f1.id)
            short_name = self.__split_project_name(gitlab_project.name)
            project_object = Component(gitlab_project.name, gitlab_project.created_at, gitlab_project.last_activity_at,
                                       short_name)
            json_obj = {
                "creation_date": project_object.creation_date,
                "short_name": project_object.short_name,
                "project_name": project_object.project_name,
                "last_activity_date": project_object.last_activity_date
            }
            projects_list.append(json_obj)
        return projects_list

    # Funcion que acorta los nombres para generar un alias sin el prefijo con el objetivo de comparar posteriormente
    # para buscar coincidencias y duplicidades.
    # TODO Automate this method by receiving the search criteria array and returning the divided project name
    @staticmethod
    def __split_project_name(name):
        if name.find('WEBCOMPONENT_') > -1:
            return name.replace('WEBCOMPONENT_', '')
        elif name.find('ANOTHER_PREFIX_') > -1:
            return name.replace('ANOTHER_PREFIX_', '')
        else:
            return name

# TODO Modificar estas funciones para hacerlas genéricas y añadirlas a la clase principal de tratamiento de gitlab.
# @staticmethod
#     # Metodo para encontrar valores en un objeto JSON según una propiedad del mismo
#     def __find_values(id, json_repr) -> object:
#         results = []
#
#         def __decode_dict(a_dict):
#             try:
#                 results.append(a_dict[id])
#             except KeyError:
#                 pass
#             return a_dict
#
#         json.loads(json_repr, object_hook=__decode_dict)  # Return value ignored.
#         return results
#
#     # Funcion que recibe un proyecto gitlab por parámetro y busca en un fichero del repositorio, lo decodifica y lo
#     lee.
#     def get_file_info(self, project):
#         angular_components = []
#         try:
#             package_file = project.files.get("package.json", ref="develop").decode()
#             package_file = package_file.decode("utf8")
#             package_artifact = self.__find_values('name', package_file)
#         except:
#             package_artifact = 'undefined'
#         project = ComponentOSP('nameExample', package_artifact)
#         tdc_project = '<project path="' + str(
#             project.artifact_name[0]) + '-library-typescript" name="' + project.name + '" />'
#         angular_components.append(tdc_project)
#         print(tdc_project)
#
