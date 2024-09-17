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


C8Y_AUTH = HTTPBasicAuth(C8Y_TENANT + '/' + C8Y_USER, C8Y_PASSWORD)
C8Y_HEADERS = {
    'Accept': 'application/json',
    # 'X-Cumulocity-Processing-Mode': 'TRANSIENT'
}

GITHUB_URL_RELEASE = 'https://api.github.com/repos/PLUGIN_REPO'
GITHUB_URL_PLUGINS = 'https://raw.githubusercontent.com/thin-edge/tedge-docs/main/src/data/plugins.tsx'
GITHUB_HEADERS = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'Authorization': os.environ.get('TOKEN')
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
        software_id = create_software(name, plugin_description)
        return software_id
    else:
        logging.warning('Software not found')


def get_github_version(plugin_name, software_id):
    logging.info('Starting to get plugin version info')
    response = client.get(
        GITHUB_URL_RELEASE.replace('PLUGIN_REPO', plugin_name) + '/releases/latest',
        headers=GITHUB_HEADERS
    )
    if response.status_code == 200:
        logging.info('Got the latest release')
        raw_version = response.json()
        for item in raw_version['assets']:
            release_url = item['browser_download_url']
            release_type = release_url.split('.')[-1]
            release_version = item['name']
            if release_type == 'deb':
                release_type = 'apt'
            create_software_version(release_url, release_version + '::' + release_type, software_id)
    else:
        logging.warning('Release not found')


def create_software(name, description):
    logging.info('Start to create new software')
    payload = {
        "type": "c8y_Software",
        "name": name,
        "description": description,
        "c8y_Filter": {
            "type": "thin-edge.io"
        },
        "c8y_Global": {}
    }

    response = client.post(
        C8Y_BASEURL + '/inventory/managedObjects',
        auth=C8Y_AUTH,
        headers=C8Y_HEADERS,
        json=payload
    )
    if response.status_code == 201:
        logging.info('Software created')
        return response.json()['id']
    else:
        logging.error('Software failed to be created')


def create_software_version(url, version, software_id):
    logging.info('Start to create new software')
    payload = {
        "type": "c8y_SoftwareBinary",
        "c8y_Software": {
            "url": url,
            "version": version
        },
        "c8y_Global": {}
    }

    child_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/vnd.com.nsn.cumulocity.managedobject+json'
        # 'X-Cumulocity-Processing-Mode': 'TRANSIENT'
    }
    response = client.post(
        C8Y_BASEURL + f'/inventory/managedObjects/{software_id}/childAdditions',
        auth=C8Y_AUTH,
        headers=child_headers,
        json=payload
    )
    if response.status_code == 201:
        logging.info('Software version created')
    else:
        logging.error('Software version failed to be created')




if __name__ == '__main__':
    plugin_list = get_plugin_list()
    for plugin in plugin_list:
        software_id = get_github_info(plugin.strip())
        get_github_version(plugin.strip(), software_id)
