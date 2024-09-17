# super-market
Hackathon 2024 September

## Notes


Getting the list of *official* plugins:

```
$ curl --silent https://raw.githubusercontent.com/thin-edge/tedge-docs/main/src/data/plugins.tsx | grep 'sourceUrl: ' | tr -d "'," | cut -d / -f 4-
thin-edge/rpi-pico-client
thin-edge/python-tedge-agent
thin-edge/tedge-config2mqtt-watcher
thin-edge/tedge-services
thin-edge/tedge-services
thin-edge/tedge-services
thin-edge/tedge-services
thin-edge/tedge-services
thin-edge/tedge-services
thin-edge/c8y-command-plugin
thin-edge/c8y-textconfig-plugin
thin-edge/tedge-rugpi-image
thin-edge/meta-tedge-project
thin-edge/meta-tedge
thin-edge/meta-tedge-bin
thin-edge/modbus-plugin
thin-edge/c8y-tedge
thin-edge/tedge-benchmark
thin-edge/tedge-management-ui
thin-edge/tedge-demo-container
```


Getting latest version and packages for a plugin.


```
$ PLUGIN_REPO=thin-edge/c8y-command-plugin

$ gh api "/repos/$PLUGIN_REPO/releases/latest" | jq '{name, url: .assets[].browser_download_url}'
{
  "name": "0.0.2",
  "url": "https://github.com/thin-edge/c8y-command-plugin/releases/download/0.0.2/c8y-command-plugin-0.0.2-1.noarch.rpm"
}
{
  "name": "0.0.2",
  "url": "https://github.com/thin-edge/c8y-command-plugin/releases/download/0.0.2/c8y-command-plugin_0.0.2_all.deb"
}
{
  "name": "0.0.2",
  "url": "https://github.com/thin-edge/c8y-command-plugin/releases/download/0.0.2/c8y-command-plugin_0.0.2_noarch.apk"
}
```

## GitHub API

Get reepository's `name` and `description`.

Given that `gh` is already authenticated,

```sh
gh api /repos/thin-edge/<repo-name>
```

If not authenticated, or want to use `curl` instead, refer to https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository.

Get the latest release of the reposotory, `name` (usually version), and `assets.browser_download_url`.

```sh
gh api /repos/thin-edge/<repo-name>/releases/latest
```

Refer to https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28.
