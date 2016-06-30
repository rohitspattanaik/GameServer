from AbstractGame import AbstractGame
from GameRoom import GameRoom
import errorCodes

class WordDefinitionGame(AbstractGame):


    def __init__(self, **kwargs):
        self.name = ''
        self.room = GameRoom()


    def load(self, **kwargs):
        if kwargs.has_key('name'):
            self.name = kwargs['name']

        if kwargs.has_key('room'):
            self.room = kwargs['room']
        else:
            return errorCodes.gameRoomUnspecified


    def startGame(self, **kwargs):
        pass


    def terminate(self, **kwargs):
        pass