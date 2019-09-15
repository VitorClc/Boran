import pygame,sys
from Core.Window import GameWindow
from Core.Scenes import SceneManager
from Core.Text import Text

from SCENES.testScene import testScene

targetFPS = 60

pygame.init()
gameWindow = GameWindow(1920, 1080, "Arcane")

scenes = [testScene]
sceneManager = SceneManager(scenes, 0, gameWindow)

running = True

sceneManager.InitScene()

clock = pygame.time.Clock()
FPS = Text("FPS", 25, pygame.Vector2(1810, 0))

while running:
    gameWindow.display.fill((0,0,0))
    sceneManager.UpdateScene()
    clock.tick(targetFPS)
    pygame.display.flip()