import pygame, math, time

from Core.Scenes import SceneModel
from Core.Tilemap import Loader

from OBJECTS.Player import Player

class PlayerFollow(object):
    def __init__(self, startPosition):
        self.x = startPosition[0]
        self.y = startPosition[1]

    def getPlayerPosition(self, playerPos):
        self.x = -playerPos.x + 1000
        self.y = -playerPos.y + 400


class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.rect.centery

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            #if(hasattr(spr, 'sprite')):
            #    print("a")
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)

        self.lostsprites = []

class scene2(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow
        self.sceneManager = sceneManager

        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/test2.tmx", self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)))
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        self.player = Player(self.wall, self.tilemap.isometricToCartesian(pygame.Vector2(0,1)), self.tilemap)
        self.camera = PlayerFollow(self.player.cartesianPos)

    def ProcessInput(self, event, pressed_keys):
        self.isoPos = self.tilemap.cartesianToIsometric(pygame.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] + 64))
        self.player.ProcessInputs(self.isoPos)

    def Update(self):
        self.tilemap.DrawGround(self.surface, self.camera)
        pygame.display.update(self.tilemap.groundSprite)

        self.camera.getPlayerPosition(self.player.isoMov)

        self.player.Update(self.camera, self.surface)
        self.wall.draw(self.surface)

        if(self.player.isoReal.x == 0 and self.player.isoReal.y == 1):
            self.SwitchToScene(self.sceneManager.scenesArray[2])
            pygame.display.flip()     
            
    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))

        pygame.display.update(self.window.display.get_rect())