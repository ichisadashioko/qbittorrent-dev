# looping through qbittorrent torrent files and check for the torrent file name
import os
import argparse

if os.name == 'nt':
    QBITTORRENT_CACHE_DATA_PATH = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\qBittorrent\\BT_backup'
else:
    raise Exception('I have not done research about qBitTorrent cache data path on this OS')

parser = argparse.ArgumentParser(description='Detect duplicate torrent file name')
parser.add_argument('-d', '--dir', help='qBittorrent cache data path', default=QBITTORRENT_CACHE_DATA_PATH)
args = parser.parse_args()
print('args', args)
