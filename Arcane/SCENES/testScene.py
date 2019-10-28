import pygame, math
from Core.Scenes import SceneModel
from Core.Text import Text

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.ground = pygame.sprite.LayeredUpdates()
        self.playerLayer = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()

    def Update(self):
        pass
        
    def Render(self):
        pass