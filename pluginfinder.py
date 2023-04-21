import requests
import json

SERVICE_ADDRESS = 'https://yoursentry.com/api/0/'  # insert here your sentry url
# Or use {'cookie':''} if you dont have token
AUTH = {"Authorization": "Bearer >>TOKEN HERE<<"}

"""
Сломалась legacy integration c youtrack. Искать по горе организаций => еще большему количеству проектов руками - боль.
Этот скрипт ищет указанный ВКЛЮЧЕННЫЙ плагин во всех проектах всех организаций и выводит их в терминал.
"""


def get_organisations_list():
    """Return list of all organizations with info"""
    organizations_request = requests.get(
        SERVICE_ADDRESS+'organizations/', headers=AUTH)
    list_of_organizations = json.loads(organizations_request.content)
    return list_of_organizations


# URL EXAMPLE TO GET PROJECTS https://yoursentry.com/api/0/organizations/org_slug/
def get_projects_in_org(org_slug):
    list_of_projects_slug_in_org = []
    proj_request = requests.get(
        SERVICE_ADDRESS+"organizations/"+org_slug+"/", headers=AUTH)
    all_projects_info = json.loads(proj_request.content)
    for project in all_projects_info['projects']:
        project_slug = (project['slug'])
        list_of_projects_slug_in_org.append(project_slug)
    return list_of_projects_slug_in_org

# URL EXAMPLE TO GET PLUGINS https://yoursentry.com/api/0/projects/org_slug/proj_slug/plugins/


def get_project_enabled_plugins(org_slug, proj):
    list_of_enabled_plugins = []
    plugin_request = requests.get(
        SERVICE_ADDRESS+"projects/"+org_slug+"/"+proj+"/plugins/", headers=AUTH)
    pl = json.loads(plugin_request.content)
    for plugin in pl:
        if plugin['enabled'] == True:
            list_of_enabled_plugins.append(plugin)
    return list_of_enabled_plugins


def find_plugin(list_of_plugins, plugin_name):
    plugin_name = plugin_name.lower()
    for plugin in list_of_plugins:
        if plugin_name in plugin['shortName'].lower() or plugin_name in plugin['id'].lower():
            return True


if __name__ == '__main__':
    print('start')
    organizations = get_organisations_list()
    for org in organizations:
        org_slug = org['slug']
        projects_in_org = get_projects_in_org(org_slug)
        for project in projects_in_org:
            enabled_plugins = get_project_enabled_plugins(org_slug, project)
            # 'youtrack'  = name of plugin you want to find. Just change it if you need
            if find_plugin(enabled_plugins, 'youtrack'):
                print('found enabled plugin in org: %s, project: %s ' %
                      (org_slug, project))
    print('done')
