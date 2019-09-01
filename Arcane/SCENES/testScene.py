import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.tilemap = Loader("MAPS/testScene.tmx")
        self.player = Player(0,0)

    def Update(self):
        self.tilemap.render(self.window.display)
        self.player.Update(self.window.display)