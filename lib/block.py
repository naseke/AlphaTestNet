#import pickle

from etc import contants, structure
import uuid
#import fastavro
import datetime
import hashlib


class block:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class Block:

    def __init__(self, dic=None, version=None):
        if version is None:
            if contants.BLK_VERSION == "0.1.0":
                self.bloc = self.__init_blk_new_0_01()
        elif version == "0.1.0":
                self.bloc = self.__init_blk_0_01(dic)

    def __init_blk_new_0_01(self) -> []:
        blk = {
            "blk_id": str(uuid.uuid5(uuid.uuid4(), contants.BLK_NET_NAME)),
            "blk_timestamp": int(datetime.datetime.now().timestamp() * 1000000),
            "blk_id_prev": "",
            "blk_id_snap_prev": "",
            "blk_version": contants.BLK_VERSION,
            "blk_hash": "",
            "blk_signature": "",
            "blk_config": {'blk_config_key': ['blk_config_var_overload'], 'blk_config_var_overload': []},
            "blk_content": [],
        }
        return blk

    def __init_blk_0_01(self, dic) -> []:
        if dic:
            blk = {}
            blk.update(dic)
            return blk
        else:
            return self.__init_blk_new_0_01()

    def __getattribute__(self,arg):
        cles = [e['name'] for e in structure.block['fields']]
        if arg in cles: return self.bloc[arg]
        else: return super().__getattribute__(arg)
        # finsi
    # findef

    def add_line(self, lne):
        #self.bloc['blk_content'].append(pickle.dumps(lne))
        self.bloc['blk_content'].append(lne)
    # findef

    def set_hash(self):
        if self.bloc['blk_content'] == {}:
            raise ValueError('block incomplet')
        elif self.bloc['blk_hash'] != "":
            raise ValueError('block verouillé')
        else:
            self.bloc['blk_hash'] = hashlib.sha512(str(self.bloc).encode()).hexdigest()
        # finsi

    def set_config(self, k_c, v_c, overload=False):
        if k_c not in self.bloc['blk_config']['blk_config_key']:
            self.bloc['blk_config']['blk_config_key'].append(k_c)
        self.bloc['blk_config'][k_c] = v_c
        if overload:
            self.bloc['blk_config']['blk_config_var_overload'].append(k_c)

    def get_config(self, k_c):
        if k_c in self.bloc['blk_config']['blk_config_key']:
            return self.bloc['blk_config'][k_c]

    def set_config_version(self):
        from lib.tools import get_version
        self.set_config('blk_config_version', get_version())

    def get_config_version(self):
        return self.blk_config['blk_config_version']

    def __str__(self):
        return str(self.bloc)
    # findef

# finclass


def main():

    from lib import stock_hdd

    r = stock_hdd.hdd().read_block("2bb5f07dc752514abca9b06c8bde2f4c", structure.block)
    print(r['blk_version'])
    bl = Block(version=r['blk_version'], dic=r)
    print(bl.bloc)


# findef


if __name__ == "__main__": main()
