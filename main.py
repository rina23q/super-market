import logging
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # filename='logs.log', filemode='w',



# C8Y_BASEURL = os.environ.get('C8Y_BASEURL')
# C8Y_TENANT = os.environ.get('C8Y_TENANT')
# C8Y_USER = os.environ.get('C8Y_USER')
# C8Y_PASSWORD = os.environ.get('C8Y_PASSWORD')

PLUGIN_REPO=''

# C8Y_AUTH = HTTPBasicAuth(C8Y_TENANT + '/' + C8Y_USER, C8Y_PASSWORD)
C8Y_HEADERS = {
    'Accept': 'application/json',
    # 'X-Cumulocity-Processing-Mode': 'TRANSIENT'
}

GITHUB_URL_RELEASE = f'https://api.github.com/repos/{PLUGIN_REPO}/releases/latest'
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
        GITHUB_URL_RELEASE,
        headers=GITHUB_HEADERS
    )
    if response.status_code == 200:
        response.json()

def create_software():
    pass

def create_software_version():
    pass


if __name__ == '__main__':
    plugin_list = get_plugin_list()
    for plugin in plugin_list:
        get_github_info(plugin.strip())
