#from __future__ import print_function
from collections import deque
from lib.ordonnanceur import Ordonnanceur
from threading import *
import fastavro
from lib import block, gas, line, stock_hdd,tools
from etc import structure
import hashlib
import datetime
import os



class ordo(Ordonnanceur):

    def producteur(self, *args):
        args[0].producteur()

    def fabrik_block(self, *args):
        args[0].fabrik_block_close()
        args[0].fabrik_block_init()

    def fabrik_add_ligne(self, *args):
        args[0].fabrik_add_ligne()


class GestDeque:

    def __init__(self):
        self.ordo = ordo()
        self.deque = deque()
        self.ordo_thread = Thread(target=self.ordo.start, daemon=True)
        self.ordo_thread.start()
        self.prev = ''
        self.bloc = ''

    def producteur(self):
        g = str(gas.Gas().dico).encode()
        m = hashlib.sha512(g)
        p = m.hexdigest()
        p_old = ""

        if p_old != p:
            l = line.Line()
            l.set_content('gasethdico', gas.Gas().dico)
            l.set_hash()
            #b.add_line(l.line[0])
            self.deque.append(l.line[0])
            print(l.line)
            p_old = p

    def fabrik_block_init(self):
        self.bloc = block.Block()
        self.bloc.bloc[0]['blk_id_prev'] = self.prev
        timestamp = datetime.datetime.now().timestamp()
        print(self.bloc.blk_id, timestamp)

    def fabrik_block_close(self):
        self.prev = self.bloc.blk_id
        self.bloc.set_hash()
        print("prev : ", self.bloc.bloc[0]['blk_id_prev'])
        stock_hdd.hdd().write_block(self.bloc)


    def fabrik_add_ligne(self):
        if len(self.deque) > 0:
            self.bloc.add_line(self.deque.popleft())
        print(len(self.deque))


def main():
    from time import sleep


    gd = GestDeque()
    gd.ordo.add_task('producteur', True, gd, seconds=1)
    gd.ordo.add_task('fabrik_add_ligne', True, gd, seconds=1)
    gd.ordo.add_task('fabrik_block', True, gd, minutes=1)
    gd.fabrik_block_init()
    while True:
        try:
            sleep(0.1)
        except KeyboardInterrupt:
            stock_hdd.hdd().liste_bloc(os.path.join(tools.find_root(), "cache"))

def main2():
    import sys
    from lib.tools import total_size

    print(stock_hdd.hdd().liste_bloc(os.path.join(tools.find_root(), "cache")))
    print(stock_hdd.hdd().liste_bloc(os.path.join(tools.find_root(), "cache")).__sizeof__())
    print(sys.getsizeof(stock_hdd.hdd().liste_bloc(os.path.join(tools.find_root(), "cache"))))
    print(total_size(stock_hdd.hdd().liste_bloc(os.path.join(tools.find_root(), "cache")), verbose=False))



if __name__ == "__main__": main2()