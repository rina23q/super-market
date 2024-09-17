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


