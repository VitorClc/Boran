import pygame,sys
from Core.Window import GameWindow
from Core.Scenes import SceneManager
from Core.Text import Text

from SCENES.testScene import testScene
from SCENES.startMenu import startMenu
from SCENES.scene2 import scene2
    
targetFPS = 60

pygame.init()
gameWindow = GameWindow(1920, 1080, "Arcane")

scenes = [startMenu(),testScene(), scene2()]
sceneManager = SceneManager(scenes, 1, gameWindow)

clock = pygame.time.Clock()

while sceneManager.activeScene != None:
    #gameWindow.display.fill((255,0,0))
    sceneManager.UpdateScene(clock)
    clock.tick(targetFPS)
    pygame.display.flip()