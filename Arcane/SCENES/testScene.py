import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import MouseControl
from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.camera = MouseControl([500, -700], [500, -700], [-200,-50], 10)

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx")
        self.tilemap.Render()

        self.player = Player(self.window.display, self.tilemap.isometricToCartesian(pygame.Vector2(0,0)))

    def Update(self):
        self.camera.getMovements(self.window.display)
        
        self.tilemap.DrawSprite(self.camera.x, self.camera.y)

        self.player.ProcessInputs()
        self.player.Render(self.camera.x, self.camera.y)

        pygame.display.update(self.tilemap.tilemapSprite)
        pygame.display.update(self.player.playerSprite)

