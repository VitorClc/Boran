import pygame, math, time

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from os import listdir
from os.path import isfile, join

baseDir = "SPRITES/Player/"

##ANIMATIONS
runFront = [f for f in listdir(baseDir + "Running5/") if isfile(join(baseDir + "Running5/", f))]
runBack = [f for f in listdir(baseDir + "Running1/") if isfile(join(baseDir + "Running1/", f))]
runLeft = [f for f in listdir(baseDir + "Running7/") if isfile(join(baseDir + "Running7/", f))]
runRight = [f for f in listdir(baseDir + "Running3/") if isfile(join(baseDir + "Running3/", f))]

runLeftBack = [f for f in listdir(baseDir + "Running8/") if isfile(join(baseDir + "Running8/", f))]
runLeftUp = [f for f in listdir(baseDir + "Running6/") if isfile(join(baseDir + "Running6/", f))]
runRightBack = [f for f in listdir(baseDir + "Running2/") if isfile(join(baseDir + "Running2/", f))]
runRightUp = [f for f in listdir(baseDir + "Running4/") if isfile(join(baseDir + "Running4/", f))]

# 0 = Front; 1 = Back; 2 = Left; 3 = Right; 4 = Left-Back; 5 = Left-Up; 6 = Right-Back; 7 = Right-Up
stopSprites = ["Idle/5.png", "Idle/1.png", "Idle/7.png", "Idle/3.png", "Idle/8.png", "Idle/6.png", "Idle/2.png", "Idle/4.png"]

class Player(pygame.sprite.Sprite):
    def __init__(self, group, startPosition, tilemap):
        self.sprite = "Idle/5.png"
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

    def getAnimation(self):
        ## UP
        if(self.dY == -1 and self.dX == 0):
            if(self.walkCount < len(runFront)):
                self.image = pygame.image.load(baseDir + "Running5/" + runFront[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 0
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2

        ## DOWN
        elif(self.dY == 1 and self.dX == 0):
            if(self.walkCount < len(runBack)):
                self.image = pygame.image.load(baseDir + "Running1/" + runBack[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 1
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2

        ## LEFT
        elif(self.dX == -1 and self.dY == 0):
            if(self.walkCount < len(runLeft)):
                self.image = pygame.image.load(baseDir + "Running7/" + runLeft[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 2
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2

        ## RIGHT
        elif(self.dX == 1 and self.dY == 0):
            if(self.walkCount < len(runRight)):
                self.image = pygame.image.load(baseDir + "Running3/" + runRight[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 3
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2

        ## RIGHT-DOWN
        elif(self.dX == 1 and self.dY == 1):
            if(self.walkCount < len(runRightBack)):
                self.image = pygame.image.load(baseDir + "Running2/" + runRightBack[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 6
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0
                
        ## RIGHT-UP
        elif(self.dX == 1 and self.dY == -1):
            if(self.walkCount < len(runRightUp)):
                self.image = pygame.image.load(baseDir + "Running4/" + runRightUp[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 7
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## LEFT-DOWN
        elif(self.dX == -1 and self.dY == 1):
            if(self.walkCount < len(runLeftBack)):
                self.image = pygame.image.load(baseDir + "Running8/" + runLeftBack[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 4
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2
                
        ## LEFT-UP
        elif(self.dX == -1 and self.dY == -1):
            if(self.walkCount < len(runLeftUp)):
                self.image = pygame.image.load(baseDir + "Running6/" + runLeftUp[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 5
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 2

        elif(self.dY == 0 and self.dX == 0):
            self.image = pygame.image.load(baseDir + stopSprites[self.lastDir])

    def checkPosition(self):
        if(self.moving == True):
            if(self.isoReal.x == self.destination.x and -self.isoReal.y == self.destination.y):
                self.dX = 0
                self.dY = 0
                self.actualPath += 1
                self.moving = False
                self.goToPosition()

            elif(self.isoReal.x == self.destination.x):
                self.dX = 0

            elif(-self.isoReal.y == self.destination.y):
                self.dY = 0

    def goToPosition(self):
        if(self.actualPath < len(self.path)):
            if(self.moving == False):
                self.destination = pygame.math.Vector2(self.path[self.actualPath][0], -self.path[self.actualPath][1])
                ## CHECK X
                if(self.isoReal.x > self.destination.x):
                    self.dX = -1
                elif(self.isoReal.x < self.destination.x):
                    self.dX = 1
                else:
                    self.dX = 0

                ## CHECK Y
                if(-self.isoReal.y > self.destination.y):
                    self.dY = -1
                elif(-self.isoReal.y < self.destination.y):
                    self.dY = 1
                else:
                    self.dY = 0

                self.moving = True
        else:
            self.path = 0
            self.actualPath = 0

    def ProcessInputs(self, isoClickPos):
        if(self.canInteract == True):
            mouseClick = pygame.mouse.get_pressed()         
            if mouseClick[0] == 1:
                start = self.grid.node(int(self.isoReal.x), int(self.isoReal.y))
                end = self.grid.node(int(isoClickPos.x), int(isoClickPos.y))
                self.path = self.finder.find_path(start, end, self.grid)[0]
                #print(self.grid.grid_str(path=self.path, start=start, end=end))
                self.goToPosition()
                self.grid.cleanup()

    def Update(self, camera, surface):
        self.checkPosition()

        self.cartesianPos.x += self.dX * 4
        self.cartesianPos.y += self.dY * 4

        self.cartesianToIsometric(self.cartesianPos) 

        self.getAnimation()
        self.rect.center = pygame.Vector2(self.isoMov.x, self.isoMov.y)