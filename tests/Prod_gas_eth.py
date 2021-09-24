import fastavro

from lib import block, gas, line, stock_hdd
from etc import structure
import hashlib
import datetime



def blk_init():
    with open("blk_last", "r") as fic:
        return fic.readlines()
# findef


def main2():
    p = ""
    p_old = ""
    b = block.Block()
    b.blk_id_prev = ""
    timestamp = datetime.datetime.now().timestamp()
    print(b.blk_id, timestamp)
    while True:

        g = str(gas.Gas().dico).encode()
        m = hashlib.sha512(g)
        p = m.hexdigest()

        if p_old != p:
            l = line.Line()
            l.set_content('gasethdico', gas.Gas().dico)
            l.set_hash()
            b.add_line(l.line[0])
            print(l.line)
            p_old = p
        # finsi

        if datetime.datetime.now().timestamp() - timestamp > 5:
            prev = b.blk_id
            b.set_hash()
            #for elem in contants.BLK_KEY:
            #    print(elem, b.bloc[0][elem])
            #    fastavro.validate(b.bloc[0], structure.block, raise_errors=True, field=elem)
            #
            print("prev : ", b.bloc[0]['blk_id_prev'])
            stock_hdd.hdd().write_block(b)
            b = block.Block()
            b.bloc[0]['blk_id_prev'] = prev
            timestamp = datetime.datetime.now().timestamp()
            print(b.blk_id, timestamp)
        # finsi
        # time.sleep(2)
    # fintantque
# findef

def main3():
    pass


# findef

def main():
    b = block.Block()
    #for elem in contants.BLK_KEY:
    #    print(elem, b.bloc[0][elem])
    #    fastavro.validate(b.bloc, structure.block, raise_errors=True, field=elem)
    fastavro.validate(b.bloc[0], structure.block, raise_errors=True)

if __name__ == "__main__": main2()