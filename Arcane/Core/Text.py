import pygame

class Text(object):
    def __init__(self, text, size, position, display, color):
        self.font = pygame.font.SysFont("arial", size)
        self.text = self.font.render(str(text), True, color)
        self.size = size
        self.color = color
        self.position = position
        self.display = display

    def setText(self, text):
        self.text = self.font.render(str(text), True, self.color)

    def drawText(self):
        self.textSprite = self.display.blit(self.text, self.position)
