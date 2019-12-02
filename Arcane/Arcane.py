import pygame,sys
from Core.Window import GameWindow
from Core.Scenes import SceneManager
from Core.Text import Text

from SCENES.startMenu import startMenu
from SCENES.Academy import Academy
from SCENES.AcademyRuins import Ruins
from SCENES.City import City

targetFPS = 60

pygame.init()
gameWindow = GameWindow(1920, 1080, "Arcane")

scenes = [startMenu(),Academy(), Ruins(), City()]
sceneManager = SceneManager(scenes, 0, gameWindow)

clock = pygame.time.Clock()

while sceneManager.activeScene != None:
    #gameWindow.display.fill((255,0,0))
    sceneManager.UpdateScene(clock)
    clock.tick(targetFPS)
    pygame.display.flip()