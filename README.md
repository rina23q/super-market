# super-market
Hackathon 2024 September

## Notes


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
