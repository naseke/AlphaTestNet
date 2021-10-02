class contants:
    __VERSION = '0.01'

    def get_VERSION(self):
        return self.__VERSION

BLK_VERSION = "0.1.0"
BLK_KEY = ['blk_id', 'blk_version', 'blk_timestamp', 'blk_id_prev', 'blk_id_snap_prev', 'blk_hash', 'blk_config', 'blk_content']
BLK_NET_NAME = 'Alphanet'
# BLK_FIRST =

CACHE_PROD = "cache"

LNE_VERSION = "0.1.0"
LNE_KEY = ['lne_id', 'lne_version', 'lne_timestamp', 'lne_hash', 'lne_config', 'lne_content']

PORT_NODE = 8000
PORT_NODE_S = 8001
PORT_CACHE = 8100
PORT_VALID = 8200

"""Chemin des composants"""

PATH_CMDS='C:\\Users\\naseke\\PycharmProjects\\Alphatestnet\\cmds'
PATH_CMDS2= '/cmds3'  # pour le test

SERVICES = {'loggeur': '1', 'node': '2'}


GAS_SPEED_KEYS = ['safeLow', 'average' , 'fast', 'fastest']
GAS_RECORD_KEYS = ['safeLow', 'average' , 'fast', 'fastest']
