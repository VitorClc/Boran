import pygame, math, time

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

baseDir = "SPRITES/Human/"

##ANIMATIONS
runFront = ["Human_0_Run0.png", "Human_0_Run1.png", "Human_0_Run2.png", "Human_0_Run3.png", "Human_0_Run4.png" ,"Human_0_Run5.png" ,"Human_0_Run6.png", "Human_0_Run7.png", "Human_0_Run8.png"]
runBack = ["Human_4_Run0.png", "Human_4_Run1.png", "Human_4_Run2.png", "Human_4_Run3.png", "Human_4_Run4.png" ,"Human_4_Run5.png" ,"Human_4_Run6.png", "Human_4_Run7.png", "Human_4_Run8.png"]
runLeft = ["Human_6_Run0.png", "Human_6_Run1.png", "Human_6_Run2.png", "Human_6_Run3.png", "Human_6_Run4.png" ,"Human_6_Run5.png" ,"Human_6_Run6.png", "Human_6_Run7.png", "Human_6_Run8.png"]
runRight = ["Human_2_Run0.png", "Human_2_Run1.png", "Human_2_Run2.png", "Human_2_Run3.png", "Human_2_Run4.png" ,"Human_2_Run5.png" ,"Human_2_Run6.png", "Human_2_Run7.png", "Human_2_Run8.png"]

runLeftBack = ["Human_5_Run0.png", "Human_5_Run1.png", "Human_5_Run2.png", "Human_5_Run3.png", "Human_5_Run4.png" ,"Human_5_Run5.png" ,"Human_5_Run6.png", "Human_5_Run7.png", "Human_5_Run8.png"]
runLeftUp = ["Human_7_Run0.png", "Human_7_Run1.png", "Human_7_Run2.png", "Human_7_Run3.png", "Human_7_Run4.png" ,"Human_7_Run5.png" ,"Human_7_Run6.png", "Human_7_Run7.png", "Human_7_Run8.png"]
runRightBack = ["Human_3_Run0.png", "Human_3_Run1.png", "Human_3_Run2.png", "Human_3_Run3.png", "Human_3_Run4.png" ,"Human_3_Run5.png" ,"Human_3_Run6.png", "Human_3_Run7.png", "Human_3_Run8.png"]
runRightUp = ["Human_1_Run0.png", "Human_1_Run1.png", "Human_1_Run2.png", "Human_1_Run3.png", "Human_1_Run4.png" ,"Human_1_Run5.png" ,"Human_1_Run6.png", "Human_1_Run7.png", "Human_1_Run8.png"]

# 0 = Front; 1 = Back; 2 = Left; 3 = Right; 4 = Left-Back; 5 = Left-Up; 6 = Right-Back; 7 = Right-Up
stopSprites = ["Human_0_Idle0.png", "Human_4_Idle0.png", "Human_6_Idle0.png", "Human_2_Idle0.png", "Human_5_Idle0.png" ,"Human_7_Idle0.png" ,"Human_3_Idle0.png", "Human_1_Idle0.png"]

class Player(pygame.sprite.Sprite):
    def __init__(self, group, startPosition, tilemap):
        self.sprite = "Human_0_Idle0.png"
        self.image = pygame.image.load(baseDir + self.sprite)
        self.rect = self.image.get_rect(center=-startPosition)

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoMov = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoReal = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.destination = pygame.math.Vector2(startPosition.x, startPosition.y)

        self.mapData = tilemap.map
        self.grid = Grid(matrix=tilemap.map)

        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        self.path = 0
        self.actualPath = 0
        self.moving = False
        
        self.dX = 0
        self.dY = 0

        ## ANIMATION
        self.lastDir = 0
        self.walkCount = 0 
        self.animationSpeed = 40
        self.lastUpdate = 0

        self.tilemap = tilemap
        
        pygame.sprite.Sprite.__init__(self, group)

    def cartesianToIsometric(self, cartesian):
        self.isoMov = pygame.math.Vector2((cartesian.x - cartesian.y) - (self.tilemap.zeroPoint.x * 24), (cartesian.x + cartesian.y) / 2 + (self.tilemap.zeroPoint.y * 102 ))
        self.isoReal = pygame.math.Vector2(cartesian.x / 128, -cartesian.y / 128)

    def getAnimation(self):
        ## UP
        if(self.dY == -1 and self.dX == 0):
            if(self.walkCount < len(runFront)):
                self.sprite = pygame.image.load(baseDir + runFront[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 0
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## DOWN
        elif(self.dY == 1 and self.dX == 0):
            if(self.walkCount < len(runBack)):
                self.sprite = pygame.image.load(baseDir + runBack[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 1
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## LEFT
        elif(self.dX == -1 and self.dY == 0):
            if(self.walkCount < len(runLeft)):
                self.sprite = pygame.image.load(baseDir + runLeft[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 2
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## RIGHT
        elif(self.dX == 1 and self.dY == 0):
            if(self.walkCount < len(runRight)):
                self.sprite = pygame.image.load(baseDir + runRight[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 3
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## RIGHT-DOWN
        elif(self.dX == 1 and self.dY == 1):
            if(self.walkCount < len(runRightBack)):
                self.sprite = pygame.image.load(baseDir + runRightBack[self.walkCount])
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
                self.sprite = pygame.image.load(baseDir + runRightUp[self.walkCount])
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
                self.sprite = pygame.image.load(baseDir + runLeftBack[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 4
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0
                
        ## LEFT-UP
        elif(self.dX == -1 and self.dY == -1):
            if(self.walkCount < len(runLeftUp)):
                self.sprite = pygame.image.load(baseDir + runLeftUp[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.lastDir = 5
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        elif(self.dY == 0 and self.dX == 0):
            self.sprite = pygame.image.load(baseDir + stopSprites[self.lastDir])

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
        mouseClick = pygame.mouse.get_pressed()         
        if mouseClick[0] == 1:
            start = self.grid.node(int(self.isoReal.x), int(self.isoReal.y))
            end = self.grid.node(int(isoClickPos.x), int(isoClickPos.y))
            self.path = self.finder.find_path(start, end, self.grid)[0]
            print(self.grid.grid_str(path=self.path, start=start, end=end))
            self.goToPosition()
            self.grid.cleanup()

    def Update(self, camera, surface):
        self.checkPosition()

        self.cartesianPos.x += self.dX * 4
        self.cartesianPos.y += self.dY * 4

        self.cartesianToIsometric(self.cartesianPos) 

        self.getAnimation()
        self.rect.center = pygame.Vector2(self.isoMov.x, self.isoMov.y)