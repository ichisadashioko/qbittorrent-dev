import os

def get_default_qbittorrent_cache_data_dir():
    if os.name == 'nt':
        return f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\qBittorrent\\BT_backup'
    else:
        raise Exception('I have not done research about qBitTorrent cache data path on this OS')


def get_qbittorrent_torrent_files(data_dir=get_default_qbittorrent_cache_data_dir()):
    child_filename_list = os.listdir(data_dir)
    child_filepath_list = [os.path.join(data_dir, child_filename) for child_filename in child_filename_list]
    normal_file_child_filepath_list = [child_filepath for child_filepath in child_filepath_list if os.path.isfile(child_filepath)]
    torrent_filepath_list = [torrent_filepath for torrent_filepath in normal_file_child_filepath_list if torrent_filepath.endswith('.torrent')]
    return torrent_filepath_list


def get_qbittorrent_id_list(data_dir=get_default_qbittorrent_cache_data_dir()):
    torrent_filepath_list = get_qbittorrent_torrent_files(data_dir)
    id_list = [os.path.splitext(os.path.basename(torrent_filepath))[0] for torrent_filepath in torrent_filepath_list]
    return id_list


def get_qbittorrent_torrent_file_by_id(torrent_id: str, data_dir=get_default_qbittorrent_cache_data_dir()):
    torrent_filepath = os.path.join(data_dir, f'{torrent_id}.torrent')
    if os.path.exists(torrent_filepath):
        return torrent_filepath
    else:
        raise Exception(f'{torrent_id} is not found in qBittorrent cache data dir')


def get_qbittorrent_fastresume_file_by_id(torrent_id: str, data_dir=get_default_qbittorrent_cache_data_dir()):
    fastresume_filepath = os.path.join(data_dir, f'{torrent_id}.fastresume')
    if os.path.exists(fastresume_filepath):
        return fastresume_filepath
    else:
        raise Exception(f'{torrent_id} is not found in qBittorrent cache data dir')


def get_qbittorrent_torrent_file_content_by_id(torrent_id: str, data_dir=get_default_qbittorrent_cache_data_dir()):
    torrent_filepath = get_qbittorrent_torrent_file_by_id(torrent_id, data_dir)
    with open(torrent_filepath, 'rb') as f:
        content = f.read()
    return content


def get_qbittorrent_fastresume_file_content_by_id(torrent_id: str, data_dir=get_default_qbittorrent_cache_data_dir()):
    fastresume_filepath = get_qbittorrent_fastresume_file_by_id(torrent_id, data_dir)
    with open(fastresume_filepath, 'rb') as f:
        content = f.read()
    return content
