import os
from lib import couleurs
from lib.alphaservernode import AlphaServerNode


class alphaserversupernode:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerSuperNode(AlphaServerNode):

    __VERSION = '0.01'

    def __init__(self, host, port, pwd=None, debug=False):
        super().__init__(host, port, pwd, debug)
        self.services.append({'supernode': [self.listener.address[0], self.listener.address[1]]})

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

                                           /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$ 
                                          /$$__  $$| $$  | $$| $$__  $$| $$_____/| $$__  $$
   _____                                 | $$  \__/| $$  | $$| $$  \ $$| $$      | $$  \ $$  _   _  ____  _____  ______                          
  / ____|                                |  $$$$$$ | $$  | $$| $$$$$$$/| $$$$$   | $$$$$$$/ | \ | |/ __ \|  __ \|  ____|                         
 | (___   ___ _ ____   _____ _   _ _ __   \____  $$| $$  | $$| $$____/ | $$__/   | $$__  $$ |  \| | |  | | |  | | |__      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__|  /$$  \ $$| $$  | $$| $$      | $$      | $$  \ $$ | . ` | |  | | |  | |  __|    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    |  $$$$$$/|  $$$$$$/| $$      | $$$$$$$$| $$  | $$ | |\  | |__| | |__| | |____  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|     \______/  \______/ |__/      |________/|__/  |__/ |_| \_|\____/|_____/|______|  \___/| .__/ \___|_| |_|
                                                                                                                                        | |               
                                                                                                                                        |_|               
              serveur : {self.listener.address[0]} 
              Port: {self.listener.address[1]}      
              """, log=self.log.logger)

