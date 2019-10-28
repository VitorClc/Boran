import pygame
import math
from pytmx.util_pygame import load_pygame

class Loader(object):
    def __init__(self, display, _filename, yOffset, startPoint, group):
        self.filename = _filename
        self.tilemapData = load_pygame(self.filename, pixelalpha=True)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)

        self.display = display

        self.spriteGroup = group

        #### MAP INFO
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)
        self.layers = self.tilemapData.layers

        groundMap = self.tilemapData.layers[0].data

        ### INVERT MAP MATRIX
        self.map = [[0 for x in range(len(groundMap))] for y in range(len(groundMap[0]))] 

        for w in range(0, len(groundMap)):
            for h in range(0, len(groundMap[w])):
                self.map[w][h] = groundMap[w][h]
            
        self.map = self.map[::-1]

        ## HEIGHT OFFSET
        self.yOffset = yOffset

        self.startPoint = startPoint

        self.Create()

    def Create(self):
        for layer in range(len(self.layers)):
            for x in range(0, int(self.mapSize.x)):
                for y in range(0, int(self.mapSize.y)):
                    tile = self.tilemapData.get_tile_image(x,y,layer)
                    if(tile != None):
                        xPos = (x - y) * self.tileSize.x / 2
                        yPos = (y + x) * self.tileSize.y / 2

                        if(layer == 0):
                            Tile(self.spriteGroup, tile, 0, (xPos + self.display.get_rect().centerx, yPos))
                        if(layer == 1):
                            Tile(self.spriteGroup, tile, 1, (xPos + self.display.get_rect().centerx, yPos))
    

class Tile(pygame.sprite.Sprite):
    def __init__(self, group, image, layer, pos):
        self.image = image
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, group)

                        