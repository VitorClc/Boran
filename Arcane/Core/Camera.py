import pygame

class MouseControl(object):
    def __init__(self, xlimits, ylimits, startPosition, sensibility):
        self.x = startPosition[0]
        self.y = startPosition[1]

        self.xMin = xlimits[0]
        self.xMax = xlimits[1]

        self.yMin = ylimits[0]
        self.yMax = ylimits[1]
        
        self.sensibility = sensibility

    def getMovements(self, display):

        mousex, mousey = pygame.mouse.get_pos()

        if(mousex < 50 and self.x <= self.xMin):
            self.x += self.sensibility
        elif(mousex > display.get_rect().width - 50 and self.x >= self.xMax):
            self.x -= self.sensibility

        if(mousey < 50 and self.y <= self.yMin):
            self.y += self.sensibility
        elif(mousey > display.get_rect().height - 50 and self.y >= self.yMax):
            self.y -= self.sensibility
