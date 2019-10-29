import pygame, math

from Core.Scenes import SceneModel
from Core.Tilemap import Loader

class testScene(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow

        self.sceneManager = sceneManager

        self.ground = pygame.sprite.LayeredUpdates()
        self.wall = pygame.sprite.LayeredUpdates()

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", self.ground, self.wall)
        self.camera = pygame.Vector2(0,0)
        
    def ProcessInput(self, event, pressed_keys):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.camera.y += 5
        if keys[pygame.K_a]:
            self.camera.x += 5
        if keys[pygame.K_s]:
            self.camera.y -= 5
        if keys[pygame.K_d]:
            self.camera.x -= 5

    def Update(self):
        #self.tilemap.Update(self.camera)
        pass
        
    def Render(self):
        self.ground.draw(self.window.display)
        self.wall.draw(self.window.display)
