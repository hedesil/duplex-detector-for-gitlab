from gitlabapi.gitlabConnect import GitLabConnect
from gitlabapi.gitlabConnect import GitlabProjects
from comparer.fuzzy_comparer import RepositoriesCoincidencesByName
import json

# Example of repositories which we will looking for in our GitLab: WEBCOMPONENT_COLLAPSIBLE, WEBCOMPONENT_TABLE,
# WEBCOMPONENT_TABLETEAM1, ANOTHER_PREFIX_TABLE...
# ¡OH MY GOD! 'Our developers are duplicating source code repositories and changing our nomenclature!


# First of all we do connection to GitLab
gitlab_connection = GitLabConnect('https://your.gitlab.domain', 'yourToken').connect()

# Instantiation class GitlabProject with gitlab connection
gitlab_instance = GitlabProjects(gitlab_connection)

# Get all GitLab projects by searching projects that match with any nomenclature we decide. In this version you must
# change manually private method __split_project_name() adding your criteria
all_projects = gitlab_instance.find_projects_by_filters_array(search_array=['WEBCOMPONENT_', 'ANOTHER_PREFIX_'])
print(all_projects)

# Response example of gitlab projects with our search criteria
all_projects = [  # It could be thousands of repositories!
    {
        "short_name": "COLLAPSIBLE",
        "project_name": "WEBCOMPONENT_COLLAPSIBLE",
        "last_activity_date": "2019-02-28T12:02:45.178Z",
        "creation_date": "2018-06-22T10:03:11.031Z"
    },
    {
        "short_name": "TABLE",
        "project_name": "WEBCOMPONENT_TABLE",
        "last_activity_date": "2018-11-14T21:29:38.168Z",
        "creation_date": "2018-06-22T08:27:08.683Z"
    },
    {
        "short_name": "TABLETEAM1",
        "project_name": "WEBCOMPONENT_TABLETEAM1",
        "last_activity_date": "2018-11-22T13:20:37.978Z",
        "creation_date": "2018-06-22T07:51:55.691Z"
    },
    {
        "short_name": "TABLE",
        "project_name": "ANOTHER_PREFIX_TABLE",
        "last_activity_date": "2018-11-14T21:20:57.588Z",
        "creation_date": "2018-06-22T07:47:43.665Z"
    }
]

# Get all coincidences with other repositories for each repository from  the previous list (we actually use mocked data
# from all_projects array example.
projects_with_comparison = RepositoriesCoincidencesByName.get_repositories_list_with_coincidences(
    _components_array=json.loads(all_projects), cutoff_percent=70)

# This is an example of the response that we receive from the get_repositories_list_with_coincidences() method ^^
projects_with_comparison_example = [
    # Boolean values are returned in the right way by the program, I adapted it only here
    {
        "name": "WEBCOMPONENT_COLLAPSIBLE",
        "coincidences_list": [],
        "have_coincidences": False,
        "last_activity_date": "2019-02-28T12:02:45.178Z",
        "creation_date": "2018-06-22T10:03:11.031Z"
    },
    {
        "name": "WEBCOMPONENT_TABLE",
        "coincidences_list": [
            {
                "name": "WEBCOMPONENT_TABLETEAM1",
                "percent": 85
            },
            {
                "name": "WEBCOMPONENT_TABLETEAM2",
                "percent": 85
            },
            {
                "name": "ANOTHER_PREFIX_TABLE",
                "percent": 100
            }
        ],
        "have_coincidences": True,
        "last_activity_date": "2019-02-28T12:02:45.178Z",
        "creation_date": "2018-06-22T10:03:11.031Z"
    },
    {
        "name": "WEBCOMPONENT_TABLETEAM1",
        "coincidences_list": [
            {
                "name": "WEBCOMPONENT_TABLE",
                "percent": 85
            },
            {
                "name": "WEBCOMPONENT_TABLETEAM2",
                "percent": 95
            },
            {
                "name": "ANOTHER_PREFIX_TABLE",
                "percent": 85
            }
        ],
        "have_coincidences": True,
        "last_activity_date": "2019-02-28T12:02:45.178Z",
        "creation_date": "2018-06-22T10:03:11.031Z"
    },
    {
        "name": "ANOTHER_PREFIX_TABLE",
        "coincidences_list": [
            {
                "name": "WEBCOMPONENT_TABLETEAM1",
                "percent": 85
            },
            {
                "name": "WEBCOMPONENT_TABLE",
                "percent": 100
            }
        ],
        "have_coincidences": True,
        "last_activity_date": "2019-02-28T12:02:45.178Z",
        "creation_date": "2018-06-22T10:03:11.031Z"
    }
]

print(projects_with_comparison)
