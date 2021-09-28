# import fastavro
from etc import contants
from lib.tools import find_root
import os
import pickle
import json


class stock_hdd:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class hdd:

    def __init__(self, blk_schem=None):
        if blk_schem is not None:
            self.schema = blk_schem
        self.protocol = 4

    def read_block(self, fic):
        with open(os.path.join(find_root(), contants.CACHE_PROD, fic), 'rb') as blk_fic:
            return pickle.load(blk_fic)

    def write_block(self,blk):
        with open(os.path.join(find_root(), contants.CACHE_PROD, self.generate_name_fic_via_blk(blk)), 'wb') as blk_fic:
            pickle.dump(blk, blk_fic, self.protocol)

    def read_block_j(self, fic):
        with open(os.path.join(find_root(), contants.CACHE_PROD, fic), 'rb') as blk_fic:
            return json.load(blk_fic)

    def write_block_j(self,blk):
        with open(os.path.join(find_root(), contants.CACHE_PROD, self.generate_name_fic_via_blk(blk)), 'wb') as blk_fic:
            json.dump(blk, blk_fic)

    def generate_name_fic_via_blk(self, blk):
        return blk.blk_id.replace("-", "")

    def generate_name_fic_via_str(self, id):
        return id.replace("-", "")

    def liste_bloc(self, dir_cache):
        from operator import itemgetter

        lst = [name for name in os.listdir(dir_cache) if os.path.isfile(os.path.join(dir_cache, name))]
        lst2 = list(map(lambda o: open(os.path.join(dir_cache, o), 'br'), lst))
        lst3 = list(map(lambda o: pickle.load(o), lst2))
        lst2 = list(map(lambda o: o.close(), lst2))
        lst4 = list(map(lambda o: o.blk_id_prev, lst3))
        lst5 = list(map(lambda o: o.blk_id, lst3))
        lst6 = list(zip(lst5, lst3, lst4))
        lst_t = [min(lst6, key=itemgetter(2))]
        while len(lst_t) < len(lst5):
            lst_t.append(lst6[lst4.index(lst_t[len(lst_t)-1][0])])
        return lst_t

    def __close(self,fic):
        pass

# finclass


def main():
    from etc import structure
    import block
    import os
    from lib.tools import find_root

    #b = block.Block()
    #hdd().write_block(b)
    #r = hdd().read_block(hdd().generate_name_fic(b))
    #print(r)
    #print(type(r))

    l = hdd().liste_bloc(os.path.join(find_root(),'cache'))
    print(l)


# findef


if __name__ == "__main__": main()
