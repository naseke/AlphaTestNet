import asyncio
from datetime import datetime,timedelta


class ordonnanceur:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class Ordonnanceur: # TODO à mettre dans la log

    def __init__(self):
        self.tasks = {}
        self.index = {}
        self.__continu = False

    def add_task(self, tache, recurent, *params, **quand):
        print(f"ajout de la {tache} pour execution dans {quand}")
        t = datetime.now() + timedelta(**quand)
        self.tasks.update({tache: [recurent, quand, params, t]})
        if t in self.index.keys():
            self.index[t].append(tache)
        else:
            self.index.update({t: [tache]})

    def del_task(self, tache):
        print(f"suppression de la {tache}")
        self._del_task(self.tasks[tache][len(self.tasks[tache])-1], tache)

    def _del_task(self, tache_index, tache):
        try:
            if len(self.index[tache_index]) > 1:
                del self.index[tache_index][self.index[tache_index].index(tache)]
            else:
                del self.index[tache_index]
        except KeyError:
            return -1
        try:
            del self.tasks[tache]
        except KeyError:
            return -1
        return 0


    def stop(self):
        if self.__continu:
            print("Arret de l'ordonnanceur")
            self.__continu = False

    def start(self):
        from time import sleep

        self.__continu = True
        print("démarrage de l'ordonnanceur")
        while self.__continu:
            sleep(0.001)
            lst_exec = [elem for elem in list(self.index.keys()) if elem < datetime.now()]
            if len(lst_exec) > 0:
                for elem in lst_exec:
                    print(f"execution de {self.index[elem]}")
                    tache = self.index[elem][0]
                    recurent = self.tasks[self.index[elem][0]][0]
                    quand = self.tasks[self.index[elem][0]][1]
                    params = self.tasks[self.index[elem][0]][2]
                    getattr(self, self.index[elem][0])(*params)
                    if not self._del_task(elem, tache):
                        if recurent:
                            self.add_task(tache, recurent, *params, **quand)

    def execute(self,tache):
        return tache in self.tasks.keys()


class OrdoNode(Ordonnanceur):
    def test_service_CACHE(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))

    def test_service_FABRIK(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))

    def test_service_VALIDATOR(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))

    def test_service_WALLET(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))

    def trt_config_FABRIK(self, *args):
        asyncio.run(args[0].trt_config(args[1]))
        #args[0].trt_config(args[1])

    def trt_config_VALIDATOR(self, *args):
        asyncio.run(args[0].trt_config(args[1]))

class OrdoCache(Ordonnanceur):
    def test_service(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))

class OrdoFabrik(Ordonnanceur):
    def test_service(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))

    def trt_blk(self, *args):
        asyncio.run(args[0].close_block())
        asyncio.run(args[0].send_block())
        asyncio.run(args[0].init_block())

    def ins_ligne(self, *args):
        asyncio.run(args[0].ins_ligne())


class OrdoValidator(Ordonnanceur):
    def test_service(self, *args):
        asyncio.run(args[0].test_service(args[1], args[2], args[3]))