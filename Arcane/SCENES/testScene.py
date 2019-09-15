import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import PlayerFollow
from Core.Text import Text

from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", 4, pygame.math.Vector2(0,-1))
        self.tilemap.Render()

        self.player = Player(self.window.display, self.tilemap.isometricToCartesian(pygame.Vector2(0,0)), self.tilemap.map)
        self.camera = PlayerFollow(self.player.cartesianPos)
        
        self.mousePosIsoText = Text("Mouse ISO", 25, pygame.Vector2(0, 0))
        self.playerPosText = Text("Player position", 25, pygame.Vector2(0, 26))

    def Update(self):
        isoClickPos = self.tilemap.cartesianToIsometric(pygame.math.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - (self.tilemap.yOffset * self.tilemap.tileSize.y) + 64), self.camera)
        self.mousePosIsoText.setText("Mouse ISOMETRIC: " + str(isoClickPos))

        self.player.ProcessInputs(isoClickPos)
        self.camera.getPlayerPosition(self.player.isoMov)

        self.playerPosText.setText(self.player.isoReal)

        self.tilemap.DrawSprite(self.camera.x, self.camera.y)
        self.player.Render(self.camera)

        self.mousePosIsoText.Render(self.window.display)
        self.playerPosText.Render(self.window.display)

        pygame.display.update(self.tilemap.tilemapSprite)
        pygame.display.update(self.player.playerSprite)