import pygame, math
from pytmx.util_pygame import load_pygame

tileDir = "TILESETS/"

class Loader():
    def __init__(self, _filename, wallGroup):
        filename = _filename
        
        self.wallGroup = wallGroup
        
        self.tilemapData = load_pygame(filename, smart_convert=True, pixelalpha=True)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)

        self.layers = self.tilemapData.layers

        self.groundSurface = pygame.Surface(((self.mapSize.x * self.tileSize.x) + 32, self.mapSize.y * self.tileSize.y + (self.tileSize.y * 2)))
        self.groundRect = self.groundSurface.get_rect()

        groundMap = self.tilemapData.layers[0].data
        ### INVERT MAP MATRIX
        self.map = [[0 for x in range(len(groundMap))] for y in range(len(groundMap[0]))] 

        for w in range(0, len(groundMap)):
            for h in range(0, len(groundMap[w])):
                self.map[w][h] = groundMap[w][h]
            
        self.map = self.map[::-1]

    def DrawGround(self, display, camera):
        self.groundSprite = display.blit(self.groundSurface, (0, 256))

    def Generate(self, window, zeroPoint):
        self.window = window
        self.zeroPoint = zeroPoint

        centered_x = self.window.get_rect().centerx
       
        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_image(x,y,0)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    #Tile(self.groundGroup, tile, (xPos + centered_x, yPos + 64))
                    self.groundSurface.blit(tile, (xPos + self.groundRect.centerx - self.tileSize.x / 2, yPos - self.groundRect.centery + self.tileSize.y / 2  + self.tileSize.y))

        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_image(x,y,1)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    Tile(self.wallGroup, tile, pygame.Vector2(xPos + centered_x, yPos + 64))

    def cartesianToIsometric(self, cartesian):
        isometricX= math.floor((cartesian.y / self.tileSize.y) + (cartesian.x / self.tileSize.x))
        isometricY=math.floor((-cartesian.x / self.tileSize.x) + (cartesian.y / self.tileSize.y))
        return pygame.math.Vector2(isometricX + self.zeroPoint.x, (isometricY * -1) + (self.zeroPoint.y))

    def isometricToCartesian(self, isometric):
        cartesianX=(2*isometric.y+isometric.x)/2 * 128
        cartesianY=(2*isometric.y-isometric.x)/2 * 64
        return pygame.math.Vector2(cartesianX, cartesianY)

class Tile(pygame.sprite.Sprite):
    def __init__(self, group, image, pos):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        pygame.sprite.Sprite.__init__(self, group)