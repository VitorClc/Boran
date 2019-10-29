import pygame
from pytmx.util_pygame import load_pygame

tileDir = "TILESETS/"

wall = pygame.image.load(tileDir + 'block.png')
ground = pygame.image.load(tileDir + 'floor.png')

class Loader():
    def __init__(self, gameWindow, _filename, groundGroup, wallGroup):
        filename = _filename

        self.window = gameWindow
        
        self.groundGroup = groundGroup
        self.wallGroup = wallGroup
        
        self.tilemapData = load_pygame(filename, pixelalpha=True)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)

        self.layers = self.tilemapData.layers

        self.Generate()

    def Generate(self):
        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_properties(x,y,0)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    centered_x = self.window.get_rect().centerx
                    centered_y = self.window.get_rect().centery/2

                    Tile(self.groundGroup, ground.convert_alpha(), 0, (xPos + centered_x, yPos - centered_y))
        
        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_properties(x,y,1)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    centered_x = self.window.get_rect().centerx
                    centered_y = self.window.get_rect().centery/2

                    Tile(self.wallGroup, wall.convert_alpha(), 1, (xPos + centered_x, yPos - centered_y))


    def Update(self, camera):
        #for i in len(self.groundGroup.sprites):
        #    print(i)

        #self.wallGroup.update()
        pass

class Tile(pygame.sprite.Sprite):
    def __init__(self, group, image, layer, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, group)