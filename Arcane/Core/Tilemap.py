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
                if(tile != None):
                    resizedTile = pygame.transform.scale(tile, (64,64))
                    display.blit(resizedTile, (x * 64, y * 64))


