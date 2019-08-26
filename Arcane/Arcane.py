import pygame, pyautogui, os
from Scenes import SceneModel, SceneManager

windowWidth = 800
windowHeight = 600

### Center Window
x = (pyautogui.size().width - windowWidth) / 2
y = (pyautogui.size().height - windowHeight) / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
###

sceneTest = SceneModel()

scenes = [sceneTest]

sceneManager = SceneManager(scenes, 0)

pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Hello World!")

done = False

sceneManager.StartScene()
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        sceneManager.UpdateScene()
        pygame.display.flip()