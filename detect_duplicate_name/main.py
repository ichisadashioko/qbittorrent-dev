# looping through qbittorrent torrent files and check for the torrent file name
import os
import argparse
import bencode
import collections

if os.name == 'nt':
    QBITTORRENT_CACHE_DATA_PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\qBittorrent\\BT_backup'
else:
    raise Exception('I have not done research about qBitTorrent cache data path on this OS')

parser = argparse.ArgumentParser(description='Detect duplicate torrent file name')
parser.add_argument('-d', '--dir', help='qBittorrent cache data path', default=QBITTORRENT_CACHE_DATA_PATH)
args = parser.parse_args()
print('args', args)

file_name_list_in_cache_data_dir = os.listdir(args.dir)

torrent_file_name_list = []
resume_file_name_list = []
unknown_file_name_list = []

for file_name in file_name_list_in_cache_data_dir:
    if file_name.endswith('.torrent'):
        torrent_file_name_list.append(file_name)
    elif file_name.endswith('.fastresume'):
        resume_file_name_list.append(file_name)
    else:
        unknown_file_name_list.append(file_name)

if len(unknown_file_name_list) > 0:
    print(f'Unknown file name list: {unknown_file_name_list}')

torrent_map = {}

for torrent_filename in torrent_file_name_list:
    torrent_id = os.path.splitext(torrent_filename)[0]
    torrent_filepath = os.path.join(args.dir, torrent_filename)
    torrent_file_content_bs = open(torrent_filepath, 'rb').read()
    torrent_file_content = bencode.bdecode(torrent_file_content_bs)
    # print(torrent_file_content)

    # print('='*64)
    # print(f'torrent_id {torrent_id}')
    # print('='*64)
    # print(torrent_file_content['info']['name'])

    torrent_map[torrent_id] = torrent_file_content['info']['name']

duplicated_torrent_list_map = collections.defaultdict(list)

for torrent_id, file_name in torrent_map.items():
    duplicated_torrent_list_map[file_name].append(torrent_id)

for file_name, torrent_id_list in duplicated_torrent_list_map.items():
    if len(torrent_id_list) > 1:
        print(f'Duplicated file name: {file_name}')
        for torrent_id in torrent_id_list:
            print(f'\t{torrent_id}')
