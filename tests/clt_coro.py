import asyncio
from multiprocessing.connection import Client
import hashlib
import random
import string

MOT_CLE_OBJ = "obj"


async def init(host, port, pwd=None):
    return Client((host, port), pwd)
# findef

async def create_cst_msg(conn, i):
    msg = {}
    msg[MOT_CLE_OBJ] = conn
    msg['numero'] = i
    return msg


async def send_msg(**dico):
    print(dico)
    if MOT_CLE_OBJ in dico.keys():
        conn = dico[MOT_CLE_OBJ]
        del dico[MOT_CLE_OBJ]
    dico['nom'] = await get_name()
    dico['signature'] = hashlib.sha512("ns".encode()).hexdigest()
    conn.send(dico)
# findef


async def create_bdy_msg():
    msg = {}
    msg['command'] = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    tmp = []
    for u in range(random.choice(range(10))): tmp.append("var_" + str(u))
    msg['parametres'] = tmp
    return msg
# findef


def recv_msg(conn):
    return conn.recv()
# findef

# finclass


async def get_ip():
    import socket
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


async def get_name():
    import socket
    return socket.gethostname()


async def trt(i, ip, port):
    msg = {}
    print ("boucle n°{}".format(i))
    print(len(asyncio.all_tasks()))
    c = await init(ip, port)
    tmp = await (create_cst_msg(c, i))
    msg.update(tmp)
    tmp = await create_bdy_msg()
    msg.update(tmp)
    await send_msg(**msg)
    c.close()


async def main():

    port = 8000
    #host = await get_ip()
    host = '192.168.1.9'
    tsks = []
    for i in range(10000):
        tsk = asyncio.ensure_future(trt(i, host, port))
        tsks.append(tsk)
        #await asyncio.sleep(1)
    await asyncio.wait(tsks)

# findef

if __name__ == "__main__": asyncio.run(main())