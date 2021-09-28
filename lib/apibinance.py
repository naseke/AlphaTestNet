# desc#
# desc##########################################################################
# desc# Class Binance_api
# desc##########################################################################
# desc# Description : Centralise les appelles à l'api de binance
# desc##########################################################################
# desc# V0.1		# N.SALLARES # init
# desc##########################################################################
# desc#

from lib import parametres
import lib.Singleton

from binance.client import Client

class apibinance:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION

class Binance_api(metaclass=lib.Singleton.SingletonMeta):

    def __init__(self):
        p = parametres.Params()
        self.apibin = Client(p.PARAMS['PB_api_key'], p.PARAMS['PB_api_secret'])

    # findef

    def __str__(self):
        return str(id(self))
# findef

# def __getattribute__(arg):
#	return super.__getattribute__(arg)
# findef

# finClass
