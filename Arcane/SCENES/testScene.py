import pygame, math

from Core.Scenes import SceneModel
from Core.Tilemap import Loader

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.ground = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", self.ground)

    def Update(self):
        self.ground.update()
        
    def Render(self):
        self.ground.draw(self.window.display)
