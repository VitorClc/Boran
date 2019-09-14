import pygame
from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Camera import MouseControl
from Core.Text import Text

from Player import Player

class testScene(SceneModel):
    def Start(self, _gameWindow):
        self.window = _gameWindow

        self.tilemap = Loader(self.window.display, "MAPS/testScene.tmx", 4, pygame.math.Vector2(0,-1))
        self.tilemap.Render()

        self.camera = MouseControl([1000, -0], [500, -700], [800,0], 10)

        self.player = Player(self.window.display, self.tilemap.isometricToCartesian(pygame.Vector2(0,0)), self.tilemap.map)

        self.mousePosIsoText = Text("Mouse ISO", 25, pygame.Vector2(0, 0))
        self.playerPosText = Text("Player position", 25, pygame.Vector2(0, 26))

    def Update(self):
        self.camera.getMovements(self.window.display)
        isoClickPos = self.tilemap.cartesianToIsometric(pygame.math.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - (self.tilemap.yOffset * self.tilemap.tileSize.y) + 64), self.camera)
        self.mousePosIsoText.setText("Mouse ISOMETRIC: " + str(isoClickPos))
        self.player.ProcessInputs()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.grid.cleanup()
                    start = self.player.grid.node(int(self.player.position.x), int(self.player.position.y))
                    end = self.player.grid.node(int(isoClickPos.x), int(isoClickPos.y))
                    path, runs = self.player.finder.find_path(start, end, self.player.grid)
                    print('operations:', runs, 'path length:', len(path))
                    print(self.player.grid.grid_str(path=path, start=start, end=end))

        self.playerPosText.setText(self.player.isoReal)

        self.tilemap.DrawSprite(self.camera.x, self.camera.y)
        self.player.Render(self.camera.x, self.camera.y)

        self.mousePosIsoText.Render(self.window.display)
        self.playerPosText.Render(self.window.display)

        pygame.display.update(self.tilemap.tilemapSprite)
        pygame.display.update(self.player.playerSprite)