from etc import contants, structure
from lib import stock_hdd, block
from lib.tools import find_root
import os

def parcours():
    for fich in os.listdir(os.path.join(find_root(), "cache")):
        if os.path.isfile(os.path.join(find_root(), "cache", fich)):
            print('-' * 79)
            print(fich)
            print('-' * 79)
            b = stock_hdd.hdd().read_block(fich, structure.block)
            bl = block.Block(version=b['blk_version'], dic=b)
            for elem in contants.BLK_KEY:
                if elem != "blk_content":
                    print(elem, bl.bloc[0][elem])
                else:
                    for elem2 in bl.bloc[0][elem]:
                        print(elem2)


def chaine():

   print(stock_hdd.hdd().liste_bloc(os.path.join(find_root(), "cache"), structure.block))


def index():

    index = {"blk_id": list(reversed(stock_hdd.hdd().liste_bloc(os.path.join(find_root(), "cache"), structure.block)))}
    index.update({"obj-block": [block.Block(version=stock_hdd.hdd().read_block(o.replace("-", ""),structure.block)['blk_version'], dic=stock_hdd.hdd().read_block(o.replace("-", ""),structure.block)) for o in index['blk_id']]})

    print(index['blk_id'])
    print(repr([o.blk_id_prev for o in index['obj-block']]))


# index()


chaine()