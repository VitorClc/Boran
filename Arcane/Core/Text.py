import pygame

class Text(object):
    def __init__(self, text, size, position):
        self.font = pygame.font.SysFont("comicsansms", size)
        self.text = self.font.render(str(text), True, (0, 128, 0))
        self.size = size
        self.position = position

    def setText(self, text):
        self.text = self.font.render(str(text), True, (0, 128, 0))  

    def Render(self, display):
        display.blit(self.text, self.position)
