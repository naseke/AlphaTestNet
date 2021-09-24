import asyncio
from datetime import datetime

SODA_LOCK = asyncio.Lock()
#SODA_LOCK = asyncio.Semaphore(2)
BURGER_SEM = asyncio.Semaphore(4)
FRIES_COUNTER = 0
FRIES_LOCK = asyncio.Lock()

async def get_soda(client):
    async with SODA_LOCK:
        print("    > Remplissage du soda pour {}".format(client))
        await asyncio.sleep(1)
        print("    < Le soda de {} est prêt".format(client))


async def get_frites (client):
    global FRIES_COUNTER
    async with FRIES_LOCK:
        print("    > Récupération des frites pour {}".format(client))
        if FRIES_COUNTER == 0:
            print("    ** Démarrage de la cuisson des frites")
            await asyncio.sleep(4)
            FRIES_COUNTER = 8
            print("   ** Les frites sont cuites")
        FRIES_COUNTER -= 1
        print("    < Les frites de {} sont prêtes".format(client))


async def get_burger(client):
    print("    > Commande du burger en cuisine pour {}".format(client))
    async with BURGER_SEM:
        await asyncio.sleep(3)
        print("    < Le burger de {} est prêt".format(client))


async def serve(client):
    print("=> Commande passée par {}".format(client))
    start_time = datetime.now()
    await asyncio.wait(
        [
            get_soda(client),
            get_frites(client),
            get_burger(client)
        ]
    )
    total = datetime.now() - start_time
    print("<= {} servi en {}".format(client, datetime.now() - start_time))
    return total


async def perf_test(nb_requests, period, timeout):
    tasks = []
    # On lance 'nb_requests' commandes à 'period' secondes d'intervalle
    for idx in range(1, nb_requests + 1):
        client_name = "client_{}".format(idx)
        tsk = asyncio.ensure_future(serve(client_name))
        tasks.append(tsk)
        await asyncio.sleep(period)

    finished, _ = await asyncio.wait(tasks)
    success = set()
    for tsk in finished:
        if tsk.result().seconds < timeout:
            success.add(tsk)

    print("{}/{} clients satisfaits".format(len(success), len(finished)))


def main():

    loop = asyncio.get_event_loop()
    #loop.run_until_complete(asyncio.wait([serve("A"), serve("B")]))
    #loop.run_until_complete(asyncio.wait([serve(clt) for clt in 'ABCDEFGHIJ']))
    loop.run_until_complete(asyncio.wait([perf_test(10, 0.5 , 5)]))
    #loop.run_until_complete(asyncio.wait([perf_test(10000, 0.000000001, 2)]))

if __name__ == "__main__": main()