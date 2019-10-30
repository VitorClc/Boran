import pygame, math

from Core.Scenes import SceneModel
from Core.Tilemap import Loader

spritesDir = "SPRITES/Human/"
idle = pygame.image.load(spritesDir + 'Human_0_Idle0.png')

class Player(pygame.sprite.Sprite):
    def __init__(self, group, image, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        pygame.sprite.Sprite.__init__(self, group)

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
        
        self.surface = pygame.Surface([self.tilemap.tileSize.x * self.tilemap.mapSize.x + 32, self.tilemap.tileSize.y * self.tilemap.mapSize.y + 256])
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, 0)

        self.camera = pygame.Vector2(0,0)
        self.player = Player(self.wall, idle.convert_alpha(), pygame.Vector2(800,400))
        
    def ProcessInput(self, event, pressed_keys):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.player.rect.centery -= 15
        if keys[pygame.K_a]:
            self.player.rect.centerx -= 15
        if keys[pygame.K_s]:
            self.player.rect.centery += 15
        if keys[pygame.K_d]:
            self.player.rect.centerx += 15

    def Update(self):
        self.surface.fill((0,0,100))
        self.ground.draw(self.surface)
        self.wall.draw(self.surface)
        
    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        pygame.display.update(self.window.display.get_rect())
