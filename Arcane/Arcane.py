import pygame,sys
from Core.Window import GameWindow
from Core.Scenes import SceneManager

from testScene import testScene

pygame.init()
gameWindow = GameWindow(1280, 720, "Hello World")

scenes = [testScene]
sceneManager = SceneManager(scenes, 0, gameWindow)

running = True

sceneManager.InitScene()

while running:        
    sceneManager.UpdateScene()
    pygame.display.flip()