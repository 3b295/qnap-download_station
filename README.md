```python
>>> from qnap_downstation import DownloadStation
>>> app = DownloadStation('nas.3b295.com:8080', 'user', 'password')
>>> app.task_query()
... app.data
... [{'activity_time': 2850204, ...}]
>>> app.task_add_url('baidu.com', "Download", "Download")
>>> app.task_add_torrent('filename.torrent', 'Download/x')
```