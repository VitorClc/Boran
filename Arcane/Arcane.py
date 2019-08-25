import pygame
import pyautogui
import os

windowWidth = 800
windowHeight = 600

### Center Window
x = (pyautogui.size().width - windowWidth) / 2
y = (pyautogui.size().height - windowHeight) / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
###

pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Hello World!")

done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        pygame.display.flip()