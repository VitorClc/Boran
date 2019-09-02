import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.tilemap = Loader("MAPS/testScene.tmx")
        #self.player = Player(0,0)
        self.x = 0
        self.y = 0

    def Update(self):
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            self.x += 5
        if keys[pygame.K_RIGHT]:
            self.x -= 5

        self.tilemap.Render(self.window.display, self.x, self.y)
        #self.player.Render(self.window.display)