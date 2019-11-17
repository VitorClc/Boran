import pygame, math
from pygame.math import Vector2

from Core.Scenes import SceneModel
from Core.Button import Button

class startMenu(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow
        self.sceneManager = sceneManager
        
        self.screenCenter = Vector2(self.window.windowWidth / 2, self.window.windowHeight / 2)
        
        def startGame():
            self.fade(1920, 1080)
            self.SwitchToScene(self.sceneManager.scenesArray[1])
            self.startButton.destroy()
            pygame.display.flip()

        self.startButton = Button(self.window, (255,0,0), (0,0,255), Vector2(self.screenCenter.x, self.screenCenter.y - 100), Vector2(300,80), "Iniciar Jogo", startGame)

    def fade(self, width, height): 
        fade = pygame.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            pygame.display.update()
            self.window.display.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(2)
        
    def ProcessInput(self, event, pressed_keys):
        pos = pygame.mouse.get_pos()
        
        self.startButton.HandleInput(pos, event)
            
    def Render(self):
        self.startButton.Draw()
        pygame.display.update(self.startButton.buttonRect)