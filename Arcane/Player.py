import pygame, math, time
from Core.GameObject import GameObjectBase

#Pathfinding lib
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

baseDir = "SPRITES/Human/"

class Player(GameObjectBase):
    def __init__(self, gameWindow, startPosition, mapData):
        self.gameWindow = gameWindow

        self.cartesianPos = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoMov = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.isoReal = pygame.math.Vector2(startPosition.x, startPosition.y)
        self.destination = pygame.math.Vector2(startPosition.x, startPosition.y)

        self.mapData = mapData
        self.grid = Grid(matrix=mapData)

        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path = 0
        self.actualPath = 0
        self.moving = False
        
        self.dX = 0
        self.dY = 0

        self.actualSprite = "Human_0_Idle0.png"
        self.sprite = pygame.image.load(baseDir + self.actualSprite)
        self.walkCount = 0 
        self.animationSpeed = 40
        self.lastUpdate = 0

        ##ANIMATIONS
        self.runFront = ["Human_0_Run0.png", "Human_0_Run1.png", "Human_0_Run2.png", "Human_0_Run3.png", "Human_0_Run4.png" ,"Human_0_Run5.png" ,"Human_0_Run6.png", "Human_0_Run7.png", "Human_0_Run8.png"]
        self.runBack = ["Human_4_Run0.png", "Human_4_Run1.png", "Human_4_Run2.png", "Human_4_Run3.png", "Human_4_Run4.png" ,"Human_4_Run5.png" ,"Human_4_Run6.png", "Human_4_Run7.png", "Human_4_Run8.png"]
        self.runLeft = ["Human_6_Run0.png", "Human_6_Run1.png", "Human_6_Run2.png", "Human_6_Run3.png", "Human_6_Run4.png" ,"Human_6_Run5.png" ,"Human_6_Run6.png", "Human_6_Run7.png", "Human_6_Run8.png"]
        self.runRight = ["Human_2_Run0.png", "Human_2_Run1.png", "Human_2_Run2.png", "Human_2_Run3.png", "Human_2_Run4.png" ,"Human_2_Run5.png" ,"Human_2_Run6.png", "Human_2_Run7.png", "Human_2_Run8.png"]

    def cartesianToIsometric(self, cartesian):
        self.isoMov = pygame.math.Vector2((cartesian.x - cartesian.y), (cartesian.x + cartesian.y) / 2)
        self.isoReal = pygame.math.Vector2(cartesian.x / 128, -cartesian.y / 128)

    def getAnimation(self):
        ## UP
        if(self.dY == -1):
            if(self.walkCount < len(self.runFront)):
                self.sprite = pygame.image.load(baseDir + self.runFront[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## DOWN
        elif(self.dY == 1):
            if(self.walkCount < len(self.runFront)):
                self.sprite = pygame.image.load(baseDir + self.runBack[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## LEFT
        elif(self.dX == -1):
            if(self.walkCount < len(self.runFront)):
                self.sprite = pygame.image.load(baseDir + self.runLeft[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        ## RIGHT
        elif(self.dX == 1):
            if(self.walkCount < len(self.runFront)):
                self.sprite = pygame.image.load(baseDir + self.runRight[self.walkCount])
                if pygame.time.get_ticks() - self.lastUpdate > self.animationSpeed:
                    self.walkCount += 1
                    self.lastUpdate = pygame.time.get_ticks()
            else:
                self.elapsed = 0
                self.walkCount = 0

        if(self.dY == 0 and self.dX == 0):
            self.sprite = pygame.image.load(baseDir + "Human_0_Idle0.png")


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

    def ProcessInputs(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.cartesianPos.x -= 128
                if event.key == pygame.K_RIGHT:
                    self.cartesianPos.x += 128
                if event.key == pygame.K_UP:
                    self.cartesianPos.y -= 128
                if event.key == pygame.K_DOWN:
                    self.cartesianPos.y += 128

    def Render(self, cameraX, cameraY):
        self.checkPosition()

        self.cartesianPos.x += self.dX * 4
        self.cartesianPos.y += self.dY * 4

        self.cartesianToIsometric(self.cartesianPos) 

        self.getAnimation()
        self.playerSprite = self.gameWindow.blit(self.sprite, (self.isoMov.x + cameraX, self.isoMov.y + cameraY))