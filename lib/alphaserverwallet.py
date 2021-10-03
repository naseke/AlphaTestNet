import asyncio
import datetime
import hashlib
import os
from collections import deque
from multiprocessing.connection import Listener
from operator import itemgetter
from threading import *
from etc.contants import PATH_CMDS
from lib import couleurs, tools
from lib.ordonnanceur import OrdoNode, OrdoCache, OrdoFabrik
from lib.logs import Log
from lib.alphaserver import AlphaServer


class alphaserverwallet:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class AlphaServerwallet(AlphaServer):

    __VERSION = '0.01'

    def msg_welcome(self):
        couleurs.AffichageColor().msg_INFO(msg=f"""

   _____                                  __  __  ____  _    _ _                                        
  / ____|                                |  \/  |/ __ \| |  | | |        /\                             
 | (___   ___ _ ____   _____ _   _ _ __  | \  / | |  | | |  | | |       /  \      ___  _ __   ___ _ __  
  \___ \ / _ \ '__\ \ / / _ \ | | | '__| | |\/| | |  | | |  | | |      / /\ \    / _ \| '_ \ / _ \ '_ \ 
  ____) |  __/ |   \ V /  __/ |_| | |    | |  | | |__| | |__| | |____ / ____ \  | (_) | |_) |  __/ | | |
 |_____/ \___|_|    \_/ \___|\__,_|_|    |_|  |_|\____/ \____/|______/_/    \_\  \___/| .__/ \___|_| |_|
                                                                                      | |               
                                                                                      |_|               
                    serveur : {self.listener.address[0]} 
                    Port: {self.listener.address[1]}      
                    """)

    def load_config(self):
        return 0, {'PORT_WALLET': '8040'}

