import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import MouseControl
from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.camera = MouseControl([500, -700], [500, -700], 10)

        self.tilemap = Loader("MAPS/testScene.tmx", 50, 350)
        self.tilemap.Render(self.window.display)
        #self.player = Player(0,0)

    def Update(self):
        self.camera.getMovements(self.window.display)
        self.tilemapSprite = self.window.display.blit(self.tilemap.tileSurface, (self.camera.x,self.camera.y))
        #self.player.Render(self.window.display)

    def Render(self):
        pygame.display.update(self.tilemapSprite)
