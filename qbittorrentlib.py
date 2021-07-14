import os
import time
import shutil

import bencode

MODULE_PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TMP_DIRECTORY = os.path.join(MODULE_PARENT_DIRECTORY, 'tmp')


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


def qbittorrent_change_fastresume_download_directory(fastresume_obj: dict, new_download_directory: str):
    fastresume_obj['qBt-savePath'] = new_download_directory
    fastresume_obj['save_path'] = new_download_directory


def are_two_path_in_the_same_drive(
    path_1: str,
    path_2: str,
):
    if not os.name == 'nt':
        return True

    path_1 = os.path.abspath(path_1)
    path_2 = os.path.abspath(path_2)
    drive_1 = os.path.splitdrive(path_1)[0]
    drive_2 = os.path.splitdrive(path_2)[0]
    return drive_1.lower() == drive_2.lower()


def qbittorrent_change_fastresume_file_content(fastresume_obj: dict, fastresume_filepath: str):
    # backup old fastresume file
    if not os.path.exists(TMP_DIRECTORY):
        os.mkdir(TMP_DIRECTORY)

    if os.path.exists(fastresume_filepath):
        backup_fastresume_filepath = os.path.join(
            TMP_DIRECTORY,
            f'{time.time_ns()}-{os.path.basename(fastresume_filepath)}',
        )

        # on Windows, rename is not supported if the destination and the source are on different drives.
        # so, we have to check if the destination is on the same drive as the source and if it is, then we can use rename
        # if are_two_path_in_the_same_drive(fastresume_filepath, backup_fastresume_filepath):
        shutil.move(fastresume_filepath, backup_fastresume_filepath)

    open(fastresume_filepath, mode='wb').write(bencode.encode(fastresume_obj))


def get_object_scheme(obj):
    if isinstance(obj, dict):
        return {k: get_object_scheme(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        if len(obj) == 0:
            return list

        type_list = []
        for item in obj:
            item_type = get_object_scheme(item)
            if item_type not in type_list:
                type_list.append(item_type)
        return type_list
    else:
        return type(obj)


def bencode_decode_string_key_and_value(obj):
    if isinstance(obj, dict):
        return {bencode_decode_string_key_and_value(k): bencode_decode_string_key_and_value(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        if len(obj) == 0:
            return obj
        return [bencode_decode_string_key_and_value(item) for item in obj]
    elif isinstance(obj, bytes):
        if len(obj) == 0:
            return obj

        try:
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            return obj
    else:
        return obj


class QBitTorrentInfo:
    def __init__(
        self,
        torrent_id: str,
        # info from the torrent file (metadata)
        torrent_metadata: dict,
        # info from the fastresume file (resume data)
        fastresume_data: dict = None,
        # info generated by the indexing platform
        torrent_file_path: str = None,
        fastresume_file_path: str = None,
    ):
        self.torrent_id = torrent_id
        self.torrent_metadata = torrent_metadata
        self.fastresume_data = fastresume_data
        self.torrent_file_path = torrent_file_path
        self.fastresume_file_path = fastresume_file_path


class QBitTorrentManager:
    # I want to import qbittorrent from another machine.
    # I can copy the the downloaded torrent files to the local machine.
    # I then want to import multiple qbittorrent cache directories.
    # - check to see if there are already some torrents with the same ids.
    # - modify the qbittorrent fastresume files to point to the correct local torrent files.
    # - check for possible filenames collisions.
    # - TODO (hard to implement) perform hash check on the local files ourself and update the fastresume files accordingly.
    def __init__(self):
        pass
