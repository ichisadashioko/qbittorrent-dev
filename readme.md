# notes

- torrent file (torrent meta data) contains the following fields:

```python
{
    # 'announce': str,
    # 'announce-list': [str],
    # 'comment': str,
    # 'created by': str,
    # 'creation date': int,
    'info': {
        'length': int,
        'name': str,
        'piece length': int,
        'pieces': bytes,
        'files': [ # TODO figure out how to calculate hashes and their order in multi-file torrents
            {
                'length': int,
                'path': str,
            },
        ], # if the torrent contain multiple files
    }
}
```

The torrent hash is the SHA1 hash of the bencoded data.

---

- qbittorrent fastresume file contains the following fields:

```python
{
    # 'active_time': int,
    # 'added_time': int,
    # 'allocation': str,
    # 'apply_ip_filter': int,
    # 'auto_managed': int,
    # 'completed_time': int,
    # 'disable_dht': int,
    # 'disable_lsd': int,
    # 'disable_pex': int,
    # 'download_rate_limit': int,
    # 'file-format': str,
    # 'file-version': int,
    # 'file_priority': [int],
    # 'finished_time': int,
    # 'httpseeds': list,
    # 'info-hash': bytes,
    # 'last_download': int,
    # 'last_seen_complete': int,
    # 'last_upload': int,
    # 'libtorrent-version': str,
    # 'max_connections': int,
    # 'max_uploads': int,
    # 'num_complete': int,
    # 'num_downloaded': int,
    # 'num_incomplete': int,
    # 'paused': int,
    # 'peers': bytes,
    # 'peers6': bytes,
    'pieces': bytes,
    # 'qBt-category': bytes,
    # 'qBt-contentLayout': str,
    # 'qBt-firstLastPiecePriority': int,
    # 'qBt-name': bytes,
    # 'qBt-ratioLimit': int,
    'qBt-savePath': str,
    # 'qBt-seedStatus': int,
    # 'qBt-seedingTimeLimit': int,
    # 'qBt-tags': list,
    'save_path': str,
    # 'seed_mode': int,
    # 'seeding_time': int,
    # 'sequential_download': int,
    # 'share_mode': int,
    # 'stop_when_ready': int,
    # 'super_seeding': int,
    # 'total_downloaded': int,
    # 'total_uploaded': int,
    # 'trackers': [[str]],
    # 'upload_mode': int,
    # 'upload_rate_limit': int,
    # 'url-list': list,
}
```

I will mostly need to care about the un-commented fields.
