import pygame
from pytmx.util_pygame import load_pygame

class Loader(object):
    def __init__(self, _filename):
        self.filename = _filename
        self.tilemapData = load_pygame(self.filename)
        #self.tileWidth = self.tilemapData.tilewidth    
        #self.tileHeight = self.tilemapData.tileheight

        #### MAP INFO
        self.width = self.tilemapData.width
        self.height = self.tilemapData.height
        self.layers = self.tilemapData.layers

    def Render(self, display):
        for layer in range(len(self.layers)):
            for x in range(0, self.width):
                for y in range(0,self.height):
                    tile = self.tilemapData.get_tile_image(x,y,layer)
                    if(tile != None):
                        xPos = (x * 256 / 2) - (y * 256 / 2)
                        yPos = (y * 128 / 2) + (x * 128 / 2)
                        centeredX = xPos + display.get_rect().centerx
                        centeredY = yPos - display.get_rect().centery
                        display.blit(tile, (centeredX, centeredY))

