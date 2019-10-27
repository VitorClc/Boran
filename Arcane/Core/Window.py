import pygame, pyautogui, os

class GameWindow(object):
    def __init__(self, _width, _height, _title):
        self.windowWidth = _width
        self.windowHeight = _height

        ### Center Window
        #x = (pyautogui.size().width - self.windowWidth) / 2
        #y = (pyautogui.size().height - self.windowHeight) / 2
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
        ###

        self.display = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption(_title)