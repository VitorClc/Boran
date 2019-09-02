import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.tilemap = Loader("MAPS/testScene.tmx")
        self.player = Player(0,0)
        self.x = 0

    def Update(self):
        self.window.display.fill((25,25,25))
        self.x+=2
        
        self.tilemap.Render(self.window.display, self.x)
        self.player.Render(self.window.display)