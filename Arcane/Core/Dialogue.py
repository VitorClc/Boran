import pygame
import Core.ptext as ptext

class Dialogue():
    def __init__(self):
        self.text = ""
        self.completeText = self.text
        self.visible = True

    def setCharName(self, _charName):
        self.charName = _charName
        self.lastUpdate = 0
        self.animationSpeed = 55

    def setText(self, _text):
        self.completeText = _text
        self.text_iterator = iter(_text)
        self.text = ""

    def updateText(self):
        if(pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed):
            self.text += next(self.text_iterator)
            self.lastUpdate = pygame.time.get_ticks()

    def Draw(self, _gameWindow):
        if self.visible == True:
            self.nameRect = pygame.draw.rect(_gameWindow,(26, 35, 126),(360,830,600,50))
            self.dialogueRect = pygame.draw.rect(_gameWindow,(48, 63, 159),(360,880,1200,200))

            font = pygame.font.Font('freesansbold.ttf', 32) 

            charRender = font.render(self.charName, True, (255,255,255)) 

            charRect = charRender.get_rect()  

            charRect.bottomleft = (400, 874) 

            _gameWindow.blit(charRender, charRect) 
            ptext.draw(self.text, topleft=(400, 930), fontsize=50) 
