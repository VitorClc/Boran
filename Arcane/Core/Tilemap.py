import pygame
import math
from pytmx.util_pygame import load_pygame

class Loader(object):
    def __init__(self, display, _filename, yOffset):
        self.filename = _filename
        self.tilemapData = load_pygame(self.filename)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)

        self.display = display

        #### MAP INFO
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)
        self.layers = self.tilemapData.layers

        self.tileSurface = pygame.Surface((self.mapSize.x * self.tileSize.x, self.mapSize.y * self.tileSize.y + self.tileSize.y))
        self.rect = self.tileSurface.get_rect()

        self.groundMap = self.tilemapData.layers[0].data

        ## HEIGHT OFFSET
        self.yOffset = yOffset

    def DrawSprite(self, cameraX, cameraY):
        self.tilemapSprite = self.display.blit(self.tileSurface, (cameraX,
                                                                  cameraY + self.tileSize.y / 2 - (self.yOffset * self.tileSize.y / 2)))

    def isometricToCartesian(self, isometric):
        cartesianX=(2*isometric.y+isometric.x)/2 * 128;
        cartesianY=(2*isometric.y-isometric.x)/2 * 64;
        return pygame.math.Vector2(cartesianX, cartesianY)
    
    def cartesianToIsometric(self, cartesian, camera):
        isometricX=math.floor((cartesian.y / self.tileSize.y) + (cartesian.x / self.tileSize.x))
        isometricY=math.floor((-cartesian.x / self.tileSize.x) + (cartesian.y / self.tileSize.y))
        print(isometricY - math.floor(self.yOffset/self.tileSize.y))
        return pygame.math.Vector2(isometricX, isometricY)

    def Render(self):
        for layer in range(len(self.layers)):
            for x in range(0, int(self.mapSize.x)):
                for y in range(0, int(self.mapSize.y)):
                    tile = self.tilemapData.get_tile_image(x,y,layer)
                    if(tile != None):
                        xPos = (x - y) * self.tileSize.x / 2
                        yPos = (y + x) * self.tileSize.y / 2

                        self.tileSurface.blit(tile, (xPos + self.rect.centerx - self.tileSize.x / 2, yPos - self.rect.centery + self.tileSize.y / 2 + (self.yOffset * self.tileSize.y / 2)))