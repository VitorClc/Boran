import pygame, math, time

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from os import listdir
from os.path import isfile, join

baseDir = "SPRITES/Kamon/"

# 0 = Front; 1 = Back; 2 = Left; 3 = Right; 4 = Left-Back; 5 = Left-Up; 6 = Right-Back; 7 = Right-Up
stopSprite = "Stand.png"
deadSprite = "Dead.png"

class Kamon(pygame.sprite.Sprite):
    def __init__(self, group, startPosition, tilemap, startSprite):
        if(startSprite == 0):
            self.sprite = stopSprite
        elif(startSprite == 1):
            self.sprite = deadSprite

        self.image = pygame.image.load(baseDir + self.sprite)
        self.rect = self.image.get_rect(center=-startPosition)

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoMov = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoReal = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.destination = pygame.math.Vector2(startPosition.x, startPosition.y)

        self.canInteract = True

        self.mapData = tilemap.map
        self.grid = Grid(matrix=tilemap.map)

        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        self.path = 0
        self.actualPath = 0
        self.moving = False
        
        self.dX = 0
        self.dY = 0

        ## ANIMATION
        self.lastDir = 0
        self.walkCount = 0 
        self.animationSpeed = 35
        self.lastUpdate = 0

        self.tilemap = tilemap
        
        pygame.sprite.Sprite.__init__(self, group)

    def cartesianToIsometric(self, cartesian):
        self.isoMov = pygame.math.Vector2((cartesian.x - cartesian.y) + self.tilemap.tileSize.x / 2 + 12, (cartesian.x + cartesian.y) / 2 + self.tilemap.tileSize.y * 4 + 200)
        self.isoReal = pygame.math.Vector2(cartesian.x / 128, -cartesian.y / 128)

    def Update(self, surface):

        self.cartesianPos.x += self.dX
        self.cartesianPos.y += self.dY

        self.cartesianToIsometric(self.cartesianPos) 

        self.rect.center = pygame.Vector2(self.isoMov.x, self.isoMov.y)