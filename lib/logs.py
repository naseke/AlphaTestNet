import logging


class logs:
    __VERSION = '0.01'

    @classmethod
    def get_VERSION(self):
        return self.__VERSION


class Log:

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    def __init__(self, nom, fic_nom, niveau=logging.DEBUG):
        if nom in list(logging.Logger.manager.loggerDict.keys()):
            self.logger = logging.getLogger(nom)
        else:
            handler = logging.FileHandler(fic_nom)
            handler.setFormatter(self.formatter)
            self.logger = logging.getLogger(nom)
            self.logger.setLevel(niveau)
            self.logger.addHandler(handler)
