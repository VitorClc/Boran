import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import MouseControl
from Core.Text import Text

from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", 4)
        self.tilemap.Render()

        self.camera = MouseControl([1000, -0], [500, -700], [800,0], 10)

        self.player = Player(self.window.display, self.tilemap.isometricToCartesian(pygame.Vector2(0,0)))

        self.mousePosCartText = Text("Mouse Cart", 25, pygame.Vector2(0, 2))
        self.mousePosIsoText = Text("Mouse ISO", 25, pygame.Vector2(0, self.mousePosCartText.size + 5))

    def Update(self):
        self.camera.getMovements(self.window.display)
        
        self.mousePosCartText.setText("Mouse CARTESIAN: " + str(pygame.math.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - (self.tilemap.yOffset * self.tilemap.tileSize.y) + 64)))
        self.mousePosIsoText.setText("Mouse ISOMETRIC: " + str(self.tilemap.cartesianToIsometric(pygame.math.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - (self.tilemap.yOffset * self.tilemap.tileSize.y) + 64), self.camera)))

        self.player.ProcessInputs()
        self.tilemap.DrawSprite(self.camera.x, self.camera.y)
        self.player.Render(self.camera.x, self.camera.y)

        self.mousePosCartText.Render(self.window.display)
        self.mousePosIsoText.Render(self.window.display)

        pygame.display.update(self.tilemap.tilemapSprite)
        pygame.display.update(self.player.playerSprite)
