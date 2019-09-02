import pygame

class MouseControl(object):
    def __init__(self):
        self.velx = 0
        self.vely = 0

    def getMovements(self, display):
        mousex, mousey = pygame.mouse.get_pos()

        if(mousex < 50):
            self.velx += 5
        elif(mousex > display.get_rect().width - 50):
            self.velx -= 5

        if(mousey < 50):
            self.vely += 5
        elif(mousey > display.get_rect().height - 50):
            self.vely -= 5
