import pygame
from pytmx.util_pygame import load_pygame

class Loader(object):
    def __init__(self, display, _filename, xCam, yCam):
        self.filename = _filename
        self.tilemapData = load_pygame(self.filename)
        #self.tileWidth = self.tilemapData.tilewidth    
        #self.tileHeight = self.tilemapData.tileheight

        self.display = display

        #### MAP INFO
        self.width = self.tilemapData.width
        self.height = self.tilemapData.height
        self.layers = self.tilemapData.layers

        self.offsetX = xCam
        self.offsetY = yCam

        self.tileSurface = pygame.Surface((self.width * 256 + 200, self.height * 128 + 200))
        self.tileSurface.get_rect().centerx = (self.width * 256) / 2
        self.tileSurface.get_rect().centery = (self.height * 128) / 2

    def DrawSprite(self, cameraX, cameraY):
        self.tilemapSprite = self.display.blit(self.tileSurface, (cameraX,cameraY))

    def Render(self):
        for layer in range(len(self.layers)):
            for x in range(0, self.width):
                for y in range(0,self.height):
                    tile = self.tilemapData.get_tile_image(x,y,layer)
                    if(tile != None):
                        xPos = (x - y) * 256 / 2
                        yPos = (y + x) * 128 / 2

                        centeredX = xPos + self.tileSurface.get_rect().centerx
                        centeredY = yPos - self.tileSurface.get_rect().centery / 2
                        self.tileSurface.blit(tile, (centeredX - self.offsetX, centeredY - self.offsetY))

