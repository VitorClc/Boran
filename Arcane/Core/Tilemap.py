import pygame
from pytmx.util_pygame import load_pygame

class Loader(object):
    def __init__(self, display, _filename):
        self.filename = _filename
        self.tilemapData = load_pygame(self.filename)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)

        self.display = display

        #### MAP INFO
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)
        self.layers = self.tilemapData.layers

        self.tileSurface = pygame.Surface((self.mapSize.x * self.tileSize.x, self.mapSize.y * self.tileSize.y))

    def DrawSprite(self, cameraX, cameraY):
        self.tilemapSprite = self.display.blit(self.tileSurface, (cameraX,cameraY))

    def isometricToCartesian(self, isometric):
        cartesianX=(2*isometric.y+isometric.x)/2 * 128;
        cartesianY=(2*isometric.y-isometric.x)/2 * 64;
        return pygame.math.Vector2(cartesianX, cartesianY)

    def Render(self):
        self.tileSurface.fill((0,0,255))
        for layer in range(len(self.layers)):
            for x in range(0, int(self.mapSize.x)):
                for y in range(0, int(self.mapSize.y)):
                    tile = self.tilemapData.get_tile_image(x,y,layer)
                    if(tile != None):
                        xPos = (x - y) * self.tileSize.x / 2
                        yPos = (y + x) * self.tileSize.y / 2

                        self.tileSurface.blit(tile, (xPos, yPos))

