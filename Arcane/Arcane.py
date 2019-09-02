import pygame,sys
from Core.Window import GameWindow
from Core.Scenes import SceneManager

from SCENES.testScene import testScene

pygame.init()
gameWindow = GameWindow(1920, 1080, "Arcane")

scenes = [testScene]
sceneManager = SceneManager(scenes, 0, gameWindow)

running = True

sceneManager.InitScene()

while running:        
    sceneManager.UpdateScene()
    pygame.display.flip()