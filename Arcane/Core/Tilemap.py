import pygame
import math
from pytmx.util_pygame import load_pygame

class Loader(object):
    def __init__(self, display, _filename, yOffset, startPoint):
        self.filename = _filename
        self.tilemapData = load_pygame(self.filename)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)

        self.display = display

        #### MAP INFO
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)
        self.layers = self.tilemapData.layers

        #### SURFACES
        self.groundSurface = pygame.Surface(((self.mapSize.x * self.tileSize.x) + 32, self.mapSize.y * self.tileSize.y + (self.tileSize.y * 2)))
        self.groundRect = self.groundSurface.get_rect()

        self.wallSurface = pygame.Surface(((self.mapSize.x * self.tileSize.x) + 32, self.mapSize.y * self.tileSize.y + (self.tileSize.y * 2)), pygame.SRCALPHA)
        self.wallRect = self.wallSurface.get_rect()

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

    def DrawGround(self, camera):
        self.groundSprite = self.display.blit(self.groundSurface, (camera.x - 16,
                                                                  camera.y + self.tileSize.y / 2 - (self.yOffset * self.tileSize.y / 2) - self.tileSize.y / 2))

    def DrawWalls(self, camera):
        self.wallSprite = self.display.blit(self.wallSurface, (camera.x - 16,
                                                                  camera.y + self.tileSize.y / 2 - (self.yOffset * self.tileSize.y / 2) - self.tileSize.y / 2))

    def isometricToCartesian(self, isometric):
        cartesianX=(2*isometric.y+isometric.x)/2 * 128;
        cartesianY=(2*isometric.y-isometric.x)/2 * 64;
        return pygame.math.Vector2(cartesianX, cartesianY)
    
    def cartesianToIsometric(self, cartesian, camera):
        isometricX=math.floor((cartesian.y / self.tileSize.y) + (cartesian.x / self.tileSize.x))
        isometricY=math.floor((-cartesian.x / self.tileSize.x) + (cartesian.y / self.tileSize.y))
        return pygame.math.Vector2(isometricX + self.startPoint.x, (isometricY * -1) + (self.startPoint.y))

    def Create(self):
        for layer in range(len(self.layers)):
            for x in range(0, int(self.mapSize.x)):
                for y in range(0, int(self.mapSize.y)):
                    tile = self.tilemapData.get_tile_image(x,y,layer)
                    if(tile != None):
                        xPos = (x - y) * self.tileSize.x / 2
                        yPos = (y + x) * self.tileSize.y / 2

                        if(layer == 0):
                            self.groundSurface.blit(tile, (xPos + self.groundRect.centerx - self.tileSize.x / 2, yPos - self.groundRect.centery + self.tileSize.y / 2 + (self.yOffset * self.tileSize.y / 2) + self.tileSize.y))
                        elif(layer == 1):
                            self.wallSurface.blit(tile, (xPos + self.wallRect.centerx - self.tileSize.x / 2, yPos - self.wallRect.centery + self.tileSize.y / 2 + (self.yOffset * self.tileSize.y / 2) + self.tileSize.y))
                        