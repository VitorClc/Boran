import pygame
from Scenes import SceneModel
from Tilemap import Loader

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow
        self.tilemap = Loader("MAPS/testScene.tmx")

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def Update(self):
        self.tilemap.render(self.window.display)