import os.path
import time
from lib.couleurs import AffichageColor

"""

 ####### #     # #     #  #####  ####### ### ####### #     # 
 #       #     # ##    # #     #    #     #  #     # ##    # 
 #       #     # # #   # #          #     #  #     # # #   # 
 #####   #     # #  #  # #          #     #  #     # #  #  # 
 #       #     # #   # # #          #     #  #     # #   # # 
 #       #     # #    ## #     #    #     #  #     # #    ## 
 #        #####  #     #  #####     #    ### ####### #     # 
                                                             

"""


def find_root():
    from os import getcwd
    from os import path
    if path.split(getcwd())[1] in ['lib', 'tx', 'etc', 'cache', 'cmds', 'outils', 'services', 'tests']:
        return path.split(getcwd())[0]
    else:
        return getcwd()


def get_name():
    import socket
    return socket.gethostname()


def get_ip():
    import socket
    return socket.gethostbyname(get_name())


def get_version():
    from datetime import datetime
    return datetime.utcnow().strftime('%Y%m%d%H%M%S')


def is_pickle_stream(stream):
    import pickle
    try:
        pickle.loads(stream)
        return True
    except pickle.UnpicklingError:
        return False


def affichage_block(blk, struct):

    def boucle(niveau, typ, lst, dic=None):
        from lib.couleurs import bcolors
        from pickle import loads

        char1 = " "
        increment = 4
        try:
            if typ == 'l':
                for k in lst:
                    if type(k) is list:
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'l', k)
                    elif type(k) is dict:
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'd', k.keys(), k)
                    elif type(k) is bytes:
                        if is_pickle_stream(k):
                            boucle(niveau, 'd', loads(k).line.keys(), loads(k).line)
                        else:
                            print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau, 'p', k)
                    elif type(k) is str and k[0] == "[" and k[len(k)-1] == "]":
                        k = eval(k)
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'l', k)
                    elif type(k) is str and k[0] == "{" and k[len(k) - 1] == "}":
                        k = eval(k)
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'd', k.keys(), k)
                    else:
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}",)
            elif typ == 'd':
                for k in lst:
                    if type(dic[k]) is list:
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'l', dic[k])
                    elif type(dic[k]) is dict:
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'd', list(dic[k].keys()), dic[k])
                    elif type(dic[k]) is bytes:
                        if is_pickle_stream(dic[k]):
                            boucle(niveau, 'd', loads(dic[k]).line.keys(), loads(dic[k]).line)
                        else:
                            print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k} : {bcolors.RESET}", dic[k])
                    elif dic[k] is str and dic[k][0] == "[" and dic[k][len(k) - 1] == "]":
                        dic[k] = eval(dic[k])
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'l', dic[k])
                    elif dic[k] is str and dic[k][0] == "{" and dic[k][len(k) - 1] == "}":
                        dic[k] = eval(dic[k])
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k}{bcolors.RESET}", )
                        boucle(niveau + increment, 'd', list(dic[k].keys()), dic[k])
                    else:
                        print(f"{bcolors.WARNING}{char1}" * niveau, f"{bcolors.WARNING}>", f"{bcolors.PINK}{k} : {bcolors.RESET}", dic[k])
        except Exception as err:
            #print(niveau)
            #print(typ)
            print(lst)
            #print(dic)
            #print(k)
            print(type(err))
            print(err.args)

    boucle(0, 'd', [e['name'] for e in struct['fields']], blk.bloc)

def affichage_ligne():
    pass

def total_size(o, handlers={}, verbose=False):

    from sys import getsizeof, stderr
    from itertools import chain
    from collections import deque
    try:
        from reprlib import repr
    except ImportError:
        pass

    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


def lst2bool(lst, op="and"):
    result = True
    for elem in lst:
        result = eval(f'{elem} {op} {result}')
    return result



"""

  #####  #          #     #####   #####  
 #     # #         # #   #     # #     # 
 #       #        #   #  #       #       
 #       #       #     #  #####   #####  
 #       #       #######       #       # 
 #     # #       #     # #     # #     # 
  #####  ####### #     #  #####   #####  

"""


class tools:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class ManagerClass:

    def __init__(self, chem='cmds'):
        self.path = chem
        self.package = os.path.basename(chem)
        self.__modules = self._set_modules()
        self.__structCmds = self._set_structCmds()
        self.__index = self._set_index()
        self.isempty = self.__modules == []


    def _set_modules(self):
        from os import listdir
        from os.path import isfile, join
        import importlib

        """OK c'est joli mais dans 1 semaine je vais oublier.
                Donc, pour avoir la list des objets modules :
                - je recupère la liste des fichiers | [f for f in listdir('cmds') if isfile(join('cmds', f))] | (lst_fic) 
                - je transforme la list de fichier python et nom de module (toto.py => cmds.toto)  | list(map(lambda e: f"cmds.{e.replace('.py','')}", lstfic) | (lst_name_mod)
                - je transforme la liste des noms de modules en objet module | list(map(lambda m: importlib.import_module(m), lst_name_mod) | (lst_obj_module)
                """
        return list(map(lambda m: importlib.import_module(m), list(map(lambda e: f"{self.package}.{e.replace('.py', '')}", [f for f in listdir(self.path) if isfile(join(self.path, f)) and f.find('.py') > 0]))))

    def _set_structCmds(self):

        """Pour avoir le dictionaire des commandes à partir de la liste des modules :
        - pour recuperer (la clé) le nom de la class, qui est aussi le nom d'une commande : a.__name__.split('.')[1] car a.__name__='cmds.<nom de class>
        - pour recuperer (la valeur) le reste de la structure de la commande c'est <nom de class>().get_STRUCT[<nom de class>]. La fonction getattr() le permet de façon dynamique :
        getattr(<objet>,<methode ou attribut>) =>  getattr(<objet>,<nom de class>().get_STRUCT[<nom de class>])
        - Pour finir il suffit de créer le dictionnaire grâce au mécanisme ci-contre : { <clé> : <valeur calculée par rapport à la clé> for <element contenant la clé> in list } """

        return {a.__name__.split('.')[1]: getattr(a, a.__name__.split('.')[1])().get_STRUCT()[a.__name__.split('.')[1]] for a in self.__modules}

    def _set_index(self):
        return {a.__name__.split('.')[1]: a for a in self.__modules}

    def get_module_by_class(self, cls):
        return self.__index[cls]

    def get_structCmds(self):
        return self.__structCmds

    def add_cmd(self, cmd):
        from importlib import import_module, invalidate_caches

        """
        les enfants ce que je vais vous dire va vous paraitre trivial mais docs.python.org est une grande source d'aide. 
        Attention ! encore faut-il lire cette aide JUSQU'AU BOUT !!!!!! En effet j'ai passé 1 journée pour trouver la commande ci-dessous 
        invalidate_caches() alors que l'aide dit tout simplement : 
        'If you are dynamically importing a module that was created since the interpreter began execution (e.g., created a Python source file),
        you may need to call invalidate_caches() in order for the new module to be noticed by the import system.'
        
        traduction in french pour les quiches comme moi : 
        
        'Si vous importez dynamiquement un module qui a été créé depuis le début de l'exécution de l'interpréteur (par exemple, créé un fichier source Python), 
        vous devrez peut-être appeler invalidate_caches() pour que le nouveau module soit remarqué par le système d'importation.
        
        .______    __    __  .___________.    ___       __  .__   __.     _______   _______    .___  ___.  _______ .______       _______   _______     __   __   __  
        |   _  \  |  |  |  | |           |   /   \     |  | |  \ |  |    |       \ |   ____|   |   \/   | |   ____||   _  \     |       \ |   ____|   |  | |  | |  | 
        |  |_)  | |  |  |  | `---|  |----`  /  ^  \    |  | |   \|  |    |  .--.  ||  |__      |  \  /  | |  |__   |  |_)  |    |  .--.  ||  |__      |  | |  | |  | 
        |   ___/  |  |  |  |     |  |      /  /_\  \   |  | |  . `  |    |  |  |  ||   __|     |  |\/|  | |   __|  |      /     |  |  |  ||   __|     |  | |  | |  | 
        |  |      |  `--'  |     |  |     /  _____  \  |  | |  |\   |    |  '--'  ||  |____    |  |  |  | |  |____ |  |\  \----.|  '--'  ||  |____    |__| |__| |__| 
        | _|       \______/      |__|    /__/     \__\ |__| |__| \__|    |_______/ |_______|   |__|  |__| |_______|| _| `._____||_______/ |_______|   (__) (__) (__) 
                                                                                                                                                                 
        """

        invalidate_caches()
        self.__modules.append(import_module(f'{self.package}.{cmd}'))
        #self.print_all_lst()
        self.__structCmds.update(self.get_obj_throught_module(self.__modules[len(self.__modules)-1]).get_STRUCT())
        self.__index.update({cmd: self.__modules[len(self.__modules)-1]})
        self.isempty = self.__modules == []

    def get_structCmd_by_name(self, nom):
        if nom in self.__structCmds.keys(): return self.__structCmds[nom]
        else: return None

    def get_cmd_path_file(self, cmd):
        from os.path import join
        return join(self.path, f'{cmd}.py')

    def reload_all(self):
        from importlib import reload
        self.__modules = list(map(lambda m: reload(m), self.__modules))

    def reload_one_by_name_cmd(self, cmd):
        from importlib import reload
        if cmd in self.__index.keys():
            reload(self.__index[cmd])
            return self.get_obj_throught_module(self.__index[cmd]).get_VERSION()

    def get_obj_throught_module(self, m):
        return getattr(m, m.__name__.split('.')[1])()

    def print_all_lst(self):
        AffichageColor().msg_DEBUG(repr(self.__modules))
        AffichageColor().msg_DEBUG(repr(self.__structCmds))
        AffichageColor().msg_DEBUG(repr(self.__index))

    def isexist(self, cmd):
        return cmd in self.__index.keys()

# finclass


class ManagerClassCMDS(ManagerClass):
    pass


class ManagerClassPreCMDS:

    def __init__(self, coro: bool = False):
        from importlib import import_module, invalidate_caches
        invalidate_caches()
        try:
            self.__module_name = 'lib.pre_cmds'
            self.__module = import_module(self.__module_name)
            self.isempty = self.__module is None
            self.use_in_coro = coro
        except:
            AffichageColor.msg_FAIL("Impossible d'exéctuer des commandes le module pre_cmds n'est pas dans cette arborescence !")
            raise ModuleNotFoundError
    def reload(self):
        from importlib import reload
        reload(self.__module)
        return self.__module.version()

    def get_func_throught_module(self, f):
        # return getattr(self.__module, f"{f}{'_coro' if self.use_in_coro else ''}") # doit marcher avec peut de persévérance
        if self.use_in_coro:
            return getattr(self.__module, f'{f}_coro')
        else:
            return getattr(self.__module, f)

    def get_module_name(self):
        return self.__module_name


"""

 #     #    #    ### #     # 
 ##   ##   # #    #  ##    # 
 # # # #  #   #   #  # #   # 
 #  #  # #     #  #  #  #  # 
 #     # #######  #  #   # # 
 #     # #     #  #  #    ## 
 #     # #     # ### #     # 
                             

"""

# test unitaire
def __main():
    m = ManagerClassPreCMDS()
    print(m.reload())




if __name__ == "__main__": __main()