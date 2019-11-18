import pygame

class Dialogue():
    def Draw(self, _gameWindow):
        self.nameRect = pygame.draw.rect(_gameWindow,(26, 35, 126),(360,830,600,50))
        self.dialogueRect = pygame.draw.rect(_gameWindow,(48, 63, 159),(360,880,1200,200))
        
        font = pygame.font.Font('freesansbold.ttf', 32) 

        char = font.render('GeeksForGeeks', True, (255,255,255)) 
        text = font.render('GeeksForGeeks', True, (255,255,255)) 

        charRect = char.get_rect()  
        textRect = text.get_rect()  
        
        charRect.center = (500, 857) 
        textRect.center = (500, 950) 

        _gameWindow.blit(char, charRect) 
        _gameWindow.blit(text, textRect) 
