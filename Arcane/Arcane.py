import pygame,sys
from Core.Window import GameWindow
from Core.Scenes import SceneManager
from Core.Text import Text

from SCENES.testScene import testScene
from SCENES.startMenu import startMenu

targetFPS = 60

pygame.init()
gameWindow = GameWindow(1920, 1080, "Arcane")

scenes = [startMenu(),testScene()]
sceneManager = SceneManager(scenes, 0, gameWindow)

clock = pygame.time.Clock()

while sceneManager.activeScene != None:
    gameWindow.display.fill((0,0,0))
    sceneManager.UpdateScene()
    clock.tick(targetFPS)
    print (clock.get_fps())
    pygame.display.flip()
