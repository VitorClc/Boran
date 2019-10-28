import pygame, math
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import PlayerFollow
from Core.Text import Text

from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.ground = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", 4, pygame.math.Vector2(0, -1), self.ground, self.wall)
        self.player = Player(self.window.display, self.tilemap.isometricToCartesian(pygame.Vector2(0,0)), self.tilemap)       
        self.camera = PlayerFollow(self.player.cartesianPos)
        
        self.mousePosIsoText = Text("Mouse ISO", 25, pygame.Vector2(0, 0), self.window.display, (255,0,0))

    def Update(self):
        isoClickPos = self.tilemap.cartesianToIsometric(pygame.math.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - (self.tilemap.yOffset * self.tilemap.tileSize.y) + 64), self.camera)
        self.mousePosIsoText.setText("Mouse ISOMETRIC: " + str(isoClickPos))

        self.player.ProcessInputs(isoClickPos)
        
        self.camera.getPlayerPosition(self.player.isoMov)
        
        self.ground.update()
        self.wall.update()

    def Render(self):
        self.ground.draw(self.tilemap.tileSurface)
        self.wall.draw(self.tilemap.tileSurface)

        self.tilemap.drawTilemap(self.camera)

        self.player.Render(self.camera)
        pygame.display.update(self.tilemap.tileSprite)
        pygame.display.update(self.player.playerSprite)
