import pygame, math, time

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from os import listdir
from os.path import isfile, join

baseDir = "SPRITES/Sunan/"

##ANIMATIONS
runLeft = [f for f in listdir(baseDir + "Running/") if isfile(join(baseDir + "Running/", f))]
runUp = [f for f in listdir(baseDir + "Running2/") if isfile(join(baseDir + "Running2/", f))]

voadora = [f for f in listdir(baseDir + "Voadora/") if isfile(join(baseDir + "Voadora/", f))]
kick = [f for f in listdir(baseDir + "Kick/") if isfile(join(baseDir + "Kick/", f))]

# 0 = Front; 1 = Back; 2 = Left; 3 = Right; 4 = Left-Back; 5 = Left-Up; 6 = Right-Back; 7 = Right-Up
stopSprites = ["Idle/5.png", "Idle/1.png", "Idle/7.png", "Idle/3.png", "Idle/8.png", "Idle/6.png", "Idle/2.png", "Idle/4.png"]

class Sunan(pygame.sprite.Sprite):
    def __init__(self, group, startPosition, tilemap, startDirection):
        self.sprite = "Idle/5.png"
        self.image = pygame.image.load(baseDir + self.sprite)
        self.rect = self.image.get_rect(center=-startPosition)

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoMov = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoReal = pygame.math.Vector2(startPosition.x, startPosition.y)

        self.canInteract = True

        self.mapData = tilemap.map

        self.dX = 0
        self.dY = 0

        ## ANIMATION
        self.lastDir = startDirection
        self.walkCount = 0 
        self.animationSpeed = 28
        self.lastUpdate = 0

        self.tilemap = tilemap
        
        self.moving = False
        self.voadoraAct = False
        self.kickAct = False
        self.finishedKick = False

        self.finishedVoadora = False

        pygame.sprite.Sprite.__init__(self, group)

    def cartesianToIsometric(self, cartesian):
        if(self.voadoraAct == False and self.kickAct == False):
            self.isoMov = pygame.math.Vector2((cartesian.x - cartesian.y) + self.tilemap.tileSize.x / 2 + 12, (cartesian.x + cartesian.y) / 2 + self.tilemap.tileSize.y * 4 + 300)

        self.isoReal = pygame.math.Vector2(cartesian.x, cartesian.y)

    def getAnimation(self):

        if(self.dX == 0 and self.dY == -1):
            if(self.walkCount < len(runUp)):
                self.image = pygame.image.load(baseDir + "Running2/" + runUp[self.walkCount])
                self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.8), (int(self.image.get_size()[1]*0.8))))
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 0
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2
        ## LEFT
        if(self.dX == -1 and self.dY == 0):
            if(self.walkCount < len(runLeft)):
                self.image = pygame.image.load(baseDir + "Running/" + runLeft[self.walkCount])
                self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.8), (int(self.image.get_size()[1]*0.8))))
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 2
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2

        elif(self.voadoraAct == True):
            if(self.walkCount < 45):
                self.image = pygame.image.load(baseDir + "Voadora/" + voadora[self.walkCount])
                self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.8), (int(self.image.get_size()[1]*0.8))))
                
                #self.lastDir = 5
                self.walkCount += 1
                self.lastUpdate = pygame.time.get_ticks()
            else:
                self.voadoraAct = False
                self.finishedVoadora = True

        elif(self.kickAct == True):
            if(self.walkCount < len(kick)):
                self.image = pygame.image.load(baseDir + "Kick/" + kick[self.walkCount])
                self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.8), (int(self.image.get_size()[1]*0.8))))
                
                self.walkCount += 1
                self.lastUpdate = pygame.time.get_ticks()
            else:
                self.walkCount = 0
                self.kickAct = False
                self.finishedKick = True

        elif(self.dY == 0 and self.dX == 0):
            self.image = pygame.image.load(baseDir + stopSprites[self.lastDir])
            self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.8), (int(self.image.get_size()[1]*0.8))))

    def goToPosition(self, position):
            ## CHECK X
            if(int(self.isoReal.x) > position.x + 5):
                self.dX = -1
            elif(int(self.isoReal.x) < position.x - 5):
                self.dX = 1
            elif(int(self.isoReal.x) == position.x + 1 or int(self.isoReal.x) == position.x - 1 or int(self.isoReal.x) == position.x):
                self.dX = 0

            ## CHECK Y
            if(int(self.isoReal.y) > position.y + 5):
                self.dY = -1
            elif(int(self.isoReal.y) < position.y - 5):
                self.dY = 1
            elif(int(self.isoReal.y) == position.y):
                self.dY = 0
            
            if(self.dY == 0 and self.dX == 0):
                self.moving = False
            else:
                self.moving = True

    def Update(self, surface):

        self.getAnimation()

        self.cartesianPos.x += self.dX * 4.5
        self.cartesianPos.y += self.dY * 4.5

        self.cartesianToIsometric(self.cartesianPos) 

        self.rect.center = pygame.Vector2(self.isoMov.x, self.isoMov.y)