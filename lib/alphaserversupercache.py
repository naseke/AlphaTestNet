import os
from lib import couleurs
from lib.alphaservercache import AlphaServerCache


class alphaserversupercache:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerSuperCache(AlphaServerCache):

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.services.append({'supercache': [self.listener.address[0], self.listener.address[1]]})

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

                                           /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$ 
                                          /$$__  $$| $$  | $$| $$__  $$| $$_____/| $$__  $$
   _____                                 | $$  \__/| $$  | $$| $$  \ $$| $$      | $$  \ $$   _____          _____ _    _ ______                          
  / ____|                                |  $$$$$$ | $$  | $$| $$$$$$$/| $$$$$   | $$$$$$$/  / ____|   /\   / ____| |  | |  ____|                         
 | (___   ___ _ ____   _____ _   _ _ __   \____  $$| $$  | $$| $$____/ | $$__/   | $$__  $$ | |       /  \ | |    | |__| | |__      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__|  /$$  \ $$| $$  | $$| $$      | $$      | $$  \ $$ | |      / /\ \| |    |  __  |  __|    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    |  $$$$$$/|  $$$$$$/| $$      | $$$$$$$$| $$  | $$ | |____ / ____ \ |____| |  | | |____  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|     \______/  \______/ |__/      |________/|__/  |__/  \_____/_/    \_\_____|_|  |_|______|  \___/| .__/ \___|_| |_|
                                                                                                                                        | |               
                                                                                                                                        |_|               
              serveur : {self.listener.address[0]} 
              Port: {self.listener.address[1]}      
              """, log=self.log.logger)

    def init_index(self):
        from lib.stock_hdd import hdd
        from lib.tools import find_root
        index = {"id_obj_prev": hdd().liste_bloc(os.path.join(find_root(), "cache"))}  # TODO mettre la mecanique de l'index ailleurs que dans stock_hdd
        return index
