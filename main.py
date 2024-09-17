import logging
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # filename='logs.log', filemode='w',



C8Y_BASEURL = "https://super-market.latest.stage.c8y.io"
C8Y_TENANT = 't34761664'
C8Y_USER = 'admin'
C8Y_PASSWORD = os.environ.get('C8Y_PASSWORD')

PLUGIN_REPO=''

C8Y_AUTH = HTTPBasicAuth(C8Y_TENANT + '/' + C8Y_USER, C8Y_PASSWORD)
C8Y_HEADERS = {
    'Accept': 'application/json',
    # 'X-Cumulocity-Processing-Mode': 'TRANSIENT'
}

GITHUB_URL_RELEASE = 'https://api.github.com/repos/PLUGIN_REPO'
GITHUB_URL_PLUGINS = 'https://raw.githubusercontent.com/thin-edge/tedge-docs/main/src/data/plugins.tsx'
GITHUB_HEADERS = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}


client = requests.Session()


def get_plugin_list():
    logging.info('Starting to get plugin list')
    os.system("curl --silent https://raw.githubusercontent.com/thin-edge/tedge-docs/main/src/data/plugins.tsx | grep 'sourceUrl: ' | tr -d \"',\" | cut -d / -f 4- >/tmp/pluginlist")
    f = open("/tmp/pluginlist", "r")
    plugin_list = f.readlines()
    return plugin_list


def get_github_info(plugin_name):
    logging.info('Starting to get plugins from github')
    response = client.get(
        GITHUB_URL_RELEASE.replace('PLUGIN_REPO', plugin_name),
        headers=GITHUB_HEADERS
    )
    if response.status_code == 200:
        plugin_info = response.json()
        try:
            plugin_description = plugin_info['description']
            name = plugin_info['name']
        except:
            plugin_description = 'No description'
        create_software(name, plugin_description)
    else:
        logging.warning('Software not found')


def get_github_version(plugin_name):
    logging.info()

def create_software(name, description):
    logging.info('Start to create new software')
    payload = {
        "type": "c8y_Software",
        "name": name,
        "description": description,
        "c8y_Filter": {
            "type": "thin-edge.io"
        }
    }

    response = client.post(
        C8Y_BASEURL + '/inventory/managedObjects',
        auth=C8Y_AUTH,
        headers=C8Y_HEADERS,
        json=payload
    )
    if response.status_code == 201:
        logging.info('Software created')
    else:
        logging.error('Software failed to be created')


def create_software_version():
    pass


if __name__ == '__main__':
    plugin_list = get_plugin_list()
    for plugin in plugin_list:
        get_github_info(plugin.strip())

