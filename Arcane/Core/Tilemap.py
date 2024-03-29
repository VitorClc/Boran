import pygame, math
from pytmx.util_pygame import load_pygame

tileDir = "TILESETS/"

class Loader():
    def __init__(self, _filename, wallGroup):
        filename = _filename
        
        self.wallGroup = wallGroup
        
        self.tilemapData = load_pygame(filename)

        self.tileSize = pygame.Vector2(self.tilemapData.tilewidth, self.tilemapData.tileheight)
        self.mapSize = pygame.Vector2(self.tilemapData.width, self.tilemapData.height)

        self.layers = self.tilemapData.layers

        self.groundSurface = pygame.Surface(((self.mapSize.x * self.tileSize.x) + 32, (self.mapSize.y * self.tileSize.y) + 40))
        self.groundRect = self.groundSurface.get_rect()

        groundMap = self.tilemapData.layers[1].data
        ### INVERT MAP MATRIX
        self.map = [[0 for x in range(len(groundMap))] for y in range(len(groundMap[0]))] 

        for w in range(0, len(groundMap)):
            for h in range(0, len(groundMap[w])):
                if(groundMap[w][h] != 0):
                    self.map[w][h] = 0
                else:
                    self.map[w][h] = 1
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
                    self.groundSurface.blit(tile.convert_alpha(), (xPos + self.groundRect.centerx - self.tileSize.x / 2, yPos - self.groundRect.centery + self.tileSize.y + 16 + 130))

        for x in range(0, int(self.mapSize.x)):
            for y in range(0, int(self.mapSize.y)):
                tile = self.tilemapData.get_tile_image(x,y,1)
                if(tile != None):
                    xPos = (x - y) * self.tileSize.x / 2
                    yPos = (y + x) * self.tileSize.y / 2

                    isoPos = self.cartesianToIsometric(pygame.Vector2(xPos, yPos))
                    isoPos.x -= zeroPoint.x

                    isoPos.y = y - self.mapSize.y + 1
                    isoPos.y *= -1

                    Tile(self.wallGroup, tile.convert(), pygame.Vector2(xPos + centered_x, yPos + 130), isoPos)

    def cartesianToIsometric(self, cartesian):
        isometricX= math.floor((cartesian.y / self.tileSize.y) + (cartesian.x / self.tileSize.x))
        isometricY=math.floor((-cartesian.x / self.tileSize.x) + (cartesian.y / self.tileSize.y))
        return pygame.math.Vector2(isometricX + self.zeroPoint.x, (isometricY * -1) + (self.zeroPoint.y))

class Tile(pygame.sprite.Sprite):
    def __init__(self, group, image, pos, isoPos):
        self.image = image
        self.image.set_colorkey((255,0,255))

        self.isoPos = isoPos
        
        #pygame.font.init() 
        #myfont = pygame.font.SysFont('Comic Sans MS', 30)
        #textsurface = myfont.render(str(isoPos), False, (255, 0, 0))
        #self.image.blit(textsurface, (64,256))

        self.rect = self.image.get_rect(center=pos)
        pygame.sprite.Sprite.__init__(self, group)