import pygame, math
from pygame.math import Vector2

from Core.Scenes import SceneModel
from Core.Button import Button

class startMenu(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow

        def testClick():
            print("click!")

        self.test = Button(self.window, testClick, (255,0,0), (0,0,255), Vector2(0,0), Vector2(200,100), "Test")

    def ProcessInput(self, event, pressed_keys):
        pos = pygame.mouse.get_pos()
        
        self.test.HandleInput(pos, event)
            
    def Render(self):
        self.test.Draw()
        pygame.display.update(self.test.buttonRect)
