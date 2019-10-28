import pygame, math
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import PlayerFollow
from Core.Text import Text

from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.group = pygame.sprite.LayeredUpdates()

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", 4, pygame.math.Vector2(0, -1), self.group)
        
    def Update(self):
        self.group.update()
        
    def Render(self):
        self.group.draw(self.window.display)
