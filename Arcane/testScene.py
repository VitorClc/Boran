import pygame
from Scenes import SceneModel

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.gameWindow = _gameWindow

    def Update(self):
        pygame.draw.rect(self.gameWindow.display, (0, 128, 255), pygame.Rect(30, 30, 60, 60))