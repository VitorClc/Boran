import pygame, math
from pygame.math import Vector2

from Core.Scenes import SceneModel
from Core.Button import Button

class startMenu(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.test = Button(self.window, (255,0,0), Vector2(0,0), Vector2(200,100), "Test")

    def Update(self):
        pass

    def Render(self):
        self.test.Draw()
        pygame.display.update(self.test.buttonRect)
