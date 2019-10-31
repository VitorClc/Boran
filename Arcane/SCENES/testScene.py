import pygame, math

from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Text import Text

from OBJECTS.Player import Player

spritesDir = "SPRITES/Human/"
idle = pygame.image.load(spritesDir + 'Human_0_Idle0.png')

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
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.ground = pygame.sprite.LayeredUpdates()
        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/testScene.tmx", self.ground, self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)))
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        self.player = Player(self.wall, idle.convert_alpha(), self.tilemap.isometricToCartesian(pygame.Vector2(-6,7)), self.tilemap)
        self.camera = PlayerFollow(self.player.position)

        self.mousePosIsoText = Text("Mouse ISO", 25, pygame.Vector2(0, 0), self.window.display, (255,0,0))
        
    def ProcessInput(self, event, pressed_keys):
        self.isoPos = self.tilemap.cartesianToIsometric(pygame.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] + 64))
        self.mousePosIsoText.setText("Mouse ISOMETRIC: " + str(self.isoPos))

    def Update(self):
        self.surface.fill((0,0,0))

        self.camera.getPlayerPosition(pygame.Vector2(self.player.rect.centerx, self.player.rect.centery))

        self.ground.draw(self.surface)
        self.wall.draw(self.surface)

    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        self.mousePosIsoText.drawText()
        pygame.display.update(self.mousePosIsoText.textSprite)

        pygame.display.update(self.window.display.get_rect())
