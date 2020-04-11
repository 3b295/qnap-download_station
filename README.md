# Qnap DownloadStation

This software is an unofficial client for the QNAP api. May be unavailable due to QANP API upgrade.

This is the python version of [this library](https://github.com/cyclotron3k/qnap-download_station).

# Install
```bash
    pip install git+https://github.com/3b295/qnap-download_station.git
```

# Usage

```python
>>> from qnap_downloadstation import DownloadStation
>>> app = DownloadStation('nas.3b295.com:8080', 'user', 'password')
>>> app.task_status()
>>> app.data
{'active': 1, 'all': 112, 'bt': 112, 'completed': 103, 'down_rate': 1075, 'downloading': 8, 'inactive': 111, 'paused': 0, 'seeding': 1, 'stopped': 0, 'up_rate': 0, 'url': 0}
```

download

```python
# download from url
# params：
#   url: such as [http://, https://, ftp://, ftps://, qqdl://, thunder:// flashget://, magnet]
#   move: save path
#   tmp(optional): temporary file path
>>> app.task_add_url('<url>', 'Download/', 'Download/tmp')

# download torrent file
>>> app.task_add_torrent('<torrent-file-path>', 'Download/', 'Download/tmp/')

```

tasks message
```python
>>> res = app.task_query()
>>> res.data
[{'files': [{filename': '<filename>', 'hash': '<hash>', 'priority': 1, 'size': 155789}, ...}]

# sorted by field
>>> res = app.task_query(field='create_time', reverse=False)

# limit return the number of result sets
>>> res = app.task_query(limit=1)

# view task file information,
>>> res = app.task_get_file('<hash>')
```

task operation
```python
>>> app.task_stop('<hash>')
>>> app.task_start('<hash>')
>>> app.task_pause('<hash>')
>>> app.task_remove('<hash>')
```



## Available methods

**Account methods**

- account_add
- account_query
- account_remove
- account_update

**Addon methods**

- addon_enable
- addon_install
- addon_query
- addon_search
- addon_uninstall
- addon_verify

**Config methods**

- config_get
- config_set

**Misc methods**

- misc_dir
- misc_env
- misc_login
- misc_logout
- misc_socks_5

**RSS methods**

- rss_add
- rss_add_job
- rss_query
- rss_query_feed
- rss_query_job
- rss_remove
- rss_remove_job
- rss_update
- rss_update_feed
- rss_update_job

**Tasks**

- task_add_torrent
- task_add_url
- task_get_file
- task_get_torrent_file
- task_pause
- task_priority
- task_query
- task_remove
- task_set_file
- task_start
- task_status
- task_stop