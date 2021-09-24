import asyncio
from lib import block, gas, line, stock_hdd,tools
from lib.AlphaClient import AlphaClientFabrik
from lib.tools import get_ip
from lib.parametres import Params
import hashlib
import datetime
import os
from time import sleep


async def envoie_ligne2(obj):
    from pickle import dumps
    from base64 import standard_b64encode
    print(get_ip(), int(Params().PARAMS['PORT_FABRIK']))
    print(obj.line)

    AlphaClientFabrik.send_cmd(get_ip(), int(Params().PARAMS['PORT_FABRIK']), 0, 'trsf_ligne', 'AlphaClientFabrik', debug=False, chaine=repr(obj.line))


async def envoie_ligne(obj):
    from pickle import dumps
    from base64 import standard_b64encode

    if 'IP_NODE' in Params().PARAMS.keys() and Params().PARAMS['IP_NODE'] != '':
        AlphaClientFabrik.send_cmd(Params().PARAMS['IP_NODE'], int(Params().PARAMS['PORT_NODE']), 0, 'trsf_ligne', 'AlphaClientFabrik', debug=False, chaine=repr(obj.line))
    else:
        AlphaClientFabrik.send_cmd(get_ip(), int(Params().PARAMS['PORT_NODE']), 0, 'trsf_ligne', 'AlphaClientFabrik', debug=False, chaine=repr(obj.line))


async def main():
    p_old = ""
    while True:
        g = str(gas.Gas().dico).encode()
        m = hashlib.sha512(g)
        p = m.hexdigest()
        sleep(1)
        if p_old != p:
            l = line.Line('GasEth','V0.01')
            l.set_content('gasethdico', gas.Gas().dico)
            l.set_hash()
            # b.add_line(l.line[0])
            #self.deque.append(l.line[0])
            await envoie_ligne(l)
            print(l.line)
            p_old = p



if __name__ == "__main__": asyncio.run(main())