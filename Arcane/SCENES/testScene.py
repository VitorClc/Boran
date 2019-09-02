import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import MouseControl
from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.camera = MouseControl()
        self.tilemap = Loader("MAPS/testScene.tmx")
        #self.player = Player(0,0)

    def Update(self):
        self.camera.getMovements(self.window.display)

        self.tilemap.Render(self.window.display, self.camera.velx, self.camera.vely)
        #self.player.Render(self.window.display)