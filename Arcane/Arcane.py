import pygame
from Window import GameWindow
from Scenes import SceneModel, SceneManager

sceneTest = SceneModel()

scenes = [sceneTest]

sceneManager = SceneManager(scenes, 0)

pygame.init()
gameWindow = GameWindow(1280, 720, "Hello World")

done = False

sceneManager.StartScene()
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        sceneManager.UpdateScene()
        pygame.display.flip()