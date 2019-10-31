import pygame, math
from pytmx.util_pygame import load_pygame

tileDir = "TILESETS/"

class Loader():
    def __init__(self, _filename, groundGroup, wallGroup):
        filename = _filename
        
        self.groundGroup = groundGroup
        self.wallGroup = wallGroup
        
        self.tilemapData = load_pygame(filename, pixelalpha=True)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)

        self.layers = self.tilemapData.layers

        self.wall = pygame.image.load(tileDir + 'block.png').convert_alpha()
        self.ground = pygame.image.load(tileDir + 'floor.png').convert_alpha()

    def Generate(self, window, zeroPoint):
        self.window = window
        self.zeroPoint = zeroPoint

        centered_x = self.window.get_rect().centerx
       
        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_properties(x,y,0)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    Tile(self.groundGroup, self.ground, (xPos + centered_x, yPos + 64))
        
        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_properties(x,y,1)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    Tile(self.wallGroup, self.wall, pygame.Vector2(xPos + centered_x, yPos + 64))

    def cartesianToIsometric(self, cartesian, camera):
        isometricX= math.floor((cartesian.y / self.tileSize.y) + (cartesian.x / self.tileSize.x))
        isometricY=math.floor((-cartesian.x / self.tileSize.x) + (cartesian.y / self.tileSize.y))
        return pygame.math.Vector2(isometricX + self.zeroPoint.x, (isometricY * -1) + (self.zeroPoint.y))

class Tile(pygame.sprite.Sprite):
    def __init__(self, group, image, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        pygame.sprite.Sprite.__init__(self, group)