import pygame, math

from Core.Scenes import SceneModel
from Core.Tilemap import Loader

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.ground = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()

        self.tilemap = Loader("MAPS/testScene.tmx", self.ground, self.wall)
        
        self.surface = pygame.Surface([self.tilemap.tileSize.x * self.tilemap.mapSize.x + 32, self.tilemap.tileSize.y * self.tilemap.mapSize.y + 256])
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, 0)

        self.camera = pygame.Vector2(0,0)
        
    def ProcessInput(self, event, pressed_keys):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.camera.y += 16
        if keys[pygame.K_a]:
            self.camera.x += 16
        if keys[pygame.K_s]:
            self.camera.y -= 15
        if keys[pygame.K_d]:
            self.camera.x -= 15

    def Update(self):
        self.ground.draw(self.surface)
        self.wall.draw(self.surface)

    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        pygame.display.update(self.window.display.get_rect())
