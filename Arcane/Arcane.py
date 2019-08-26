import pygame
from Window import GameWindow
from Scenes import SceneManager

from testScene import testScene

pygame.init()
gameWindow = GameWindow(1280, 720, "Hello World")

scenes = [testScene]
sceneManager = SceneManager(scenes, 0, gameWindow)

running = False

sceneManager.InitScene()

while not running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        sceneManager.UpdateScene()
        pygame.display.flip()