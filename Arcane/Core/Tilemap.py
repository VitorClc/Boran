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

    def Render(self, display):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tilemapData.get_tile_image(x,y,0)
                xPos = (x * 256 / 2) + (y * 256 / 2)
                yPos = (y * 128 / 2) - (x * 128 / 2)
                resizedTile = pygame.transform.scale(tile, (128, 256))
                if(tile != None):
                    display.blit(resizedTile, (xPos / 2, yPos / 2))


