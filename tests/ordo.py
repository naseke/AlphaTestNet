import asyncio
from datetime import datetime,timedelta
from threading import *
from time import sleep


class ordo:

    def __init__(self):
        self.i = 0
        self.tasks = {}
        self.index = {}
        self.__continu = True

    def add_task(self, tache, recurent, *params, **quand):
        print(f"ajout de la {tache} pour execution dans {quand}")
        t = datetime.now()+timedelta(**quand)
        self.tasks.update({tache: [recurent, quand, params, t]})
        if t in self.index.keys():
            self.index[t].append(tache)
        else:
            self.index.update({t: [tache]})

    def del_task(self, tache):
        print(f"suppression de la {tache}")
        self._del_task(self.tasks[tache][len(self.tasks[tache])-1])

    def start(self):
        while self.__continu:
            sleep(0.1)
            lst_exec = [elem for elem in list(self.index.keys()) if elem < datetime.now()]
            if len(lst_exec) > 0:
                for elem in lst_exec:
                    print(f"execution de {self.index[elem]}")
                    tache = self.index[elem][0]
                    recurent = self.tasks[self.index[elem][0]][0]
                    quand = self.tasks[self.index[elem][0]][1]
                    params = self.tasks[self.index[elem][0]][2]
                    getattr(self, self.index[elem][0])(*params)
                    self._del_task(elem)
                    if recurent:
                        self.add_task(tache, recurent, *params, **quand)

    def stop(self):
        print("Arret de l'ordonnanceur")
        self.__continu = False

    def _del_task(self, tache_index):
        for elem in self.index[tache_index]:
            del self.tasks[elem]
        del self.index[tache_index]


class ordi(ordo):

    def tache1(self):
        print("Ajout de 10s")
        self.i += 10

    def tache2(self, *args):
        print("Ajout de 5s")
        self.i += 5

    def tache3(self, *args):
        asyncio.run(args[0].tache3(args[1]))

    def tache4(self, *args):
        asyncio.run(args[0].tache4(args[1]))


class serveur:

    def __init__(self):
        self.ordi = ordi()
        self.continu = False
        self.ordi_proc = None

    async def start(self):
        print('démarrage')
        self.continu = True
        self.ordi_proc = Thread(target=self.ordi.start, daemon=True)
        self.ordi_proc.start()

        #await asyncio.sleep(5)
        self.ordi.add_task('tache1', False, seconds=7)
        self.ordi.add_task('tache4', True, self, 'win !', seconds=5)
        self.ordi.add_task('tache3', False, self, 'toto', seconds=10)
        while self.continu:
            await asyncio.sleep(0.1)
        return 0

    async def tache3(self, p1):
        print("tache3", p1)

    async def tache4(self, p2):
        print("tache4", p2)


async def main():
    s = serveur()
    await s.start()


if __name__ == '__main__': asyncio.run(main())
