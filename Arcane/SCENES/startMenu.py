import pygame, math
from pygame.math import Vector2

from Core.Scenes import SceneModel
from Core.Button import Button

class startMenu(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow

        self.screenCenter = Vector2(self.window.windowWidth / 2, self.window.windowHeight / 2)
        print(self.screenCenter)
        
        def startGame():
            print("click!")

        self.startButton = Button(self.window, (255,0,0), (0,0,255), Vector2(self.screenCenter.x, self.screenCenter.y - 100), Vector2(300,80), "Iniciar Jogo", startGame)

    def ProcessInput(self, event, pressed_keys):
        pos = pygame.mouse.get_pos()
        
        self.startButton.HandleInput(pos, event)
            
    def Render(self):
        self.startButton.Draw()
        pygame.display.update(self.startButton.buttonRect)
