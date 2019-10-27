import pygame

class Button():
    def __init__(self, gameWindow, onClick, color, hoveredColor, position, size, text=""):
        self.gameWindow = gameWindow

        self.color = color
        self.normalColor = color
        self.hoveredColor = hoveredColor
        
        self.x = position.x
        self.y = position.y

        self.width = size.x
        self.height = size.y

        self.text = text
        self.hover = False

        self.onClick = onClick

    def Draw(self):
        self.buttonRect = pygame.draw.rect(self.gameWindow.display, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            self.gameWindow.display.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_width() / 2)))

    def HandleInput(self, pos, event):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.hover = True
                self.onHover()

                if(event.type == pygame.MOUSEBUTTONDOWN):
                    self.onClick()
            else:
                self.hover = False
                self.onExit()
        else:
            self.hover = False
            self.onExit()

    def onHover(self):
        self.color = self.hoveredColor

    def onExit(self):
        self.color = self.normalColor
        