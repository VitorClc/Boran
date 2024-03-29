import pygame, math, time

from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Dialogue import Dialogue

from OBJECTS.Player import Player
from OBJECTS.Kamon import Kamon
from OBJECTS.NPC import NPC

class PlayerFollow(object):
    def __init__(self, startPosition):
        self.x = startPosition[0]
        self.y = startPosition[1]

    def getPlayerPosition(self, playerPos):
        self.x = -playerPos.x + 1000
        self.y = -playerPos.y + 400

class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.rect.centery

    def draw(self, surface, player):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            if(hasattr(spr, "sprite") == False & player.useDepth == True):
                if(spr.isoPos.y < player.isoReal.y and spr.isoPos.y == player.isoReal.y - 1):
                    if(spr.isoPos.x - player.isoReal.x < 2 and spr.isoPos.x - player.isoReal.x >= 0):
                        spr.image.set_alpha(70)
                    elif(spr.isoPos.x - player.isoReal.x > -2 and spr.isoPos.x - player.isoReal.x <= 0):
                        spr.image.set_alpha(70)
                    else:
                        spr.image.set_alpha(255)
                else:
                    spr.image.set_alpha(255)

            self.spritedict[spr] = surface_blit(spr.image, spr.rect)

        self.lostsprites = []

class City(SceneModel):
    def Start(self, _gameWindow, sceneManager, startPos):
        self.window = _gameWindow
        self.sceneManager = sceneManager

        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/vilarejo_001.tmx", self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)), pygame.HWSURFACE)
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        if(startPos != None) :
            self.player = Player(self.wall, pygame.Vector2(startPos.x * 128, -startPos.y * 128), self.tilemap, 1)
        else:
            self.player = Player(self.wall, pygame.Vector2(1152,-384), self.tilemap, 1)

        self.enemy = NPC(self.wall, pygame.Vector2(512, -1024), self.tilemap, 1)
        self.enemy2 = NPC(self.wall, pygame.Vector2(1024, -384), self.tilemap, 1)
        
        self.enemyPatrol = 0
        self.enemy2Patrol = 0

        self.player.canInteract = True
        self.player.useDepth = True
        
        self.camera = PlayerFollow(self.player.cartesianPos)
        pygame.display.flip()
        
    def ProcessInput(self, event, pressed_keys):
        self.isoPos = self.tilemap.cartesianToIsometric(pygame.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - 128))
        self.player.ProcessInputs(self.isoPos)

        if event.type  == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                playerPos = "3"
                playerPos += str(int(self.player.isoReal.x))
                playerPos += str(int(self.player.isoReal.y))

                f = open("save.txt", "w")
                f.write(playerPos)
                f.close()

    def Update(self):
        self.surface.fill((0,0,0))
        self.tilemap.DrawGround(self.surface, self.camera)
        pygame.display.update(self.tilemap.groundSprite)

        self.enemy.Update(self.surface)
        self.enemy2.Update(self.surface)

        if(self.enemyPatrol == 0):
            self.enemy.goToPosition(pygame.Vector2(512, -1024))
        elif(self.enemyPatrol == 1):
            self.enemy.goToPosition(pygame.Vector2(512, 0))

        if(self.enemy.moving == False and int(self.enemy.isoReal.y) == -1024):       
            self.enemyPatrol = 1
        elif(self.enemy.moving == False and int(self.enemy.isoReal.y) == 0):
            self.enemyPatrol = 0

        if(self.enemy2Patrol == 0):
            self.enemy2.goToPosition(pygame.Vector2(1024, -384))
        elif(self.enemy2Patrol == 1):
            self.enemy2.goToPosition(pygame.Vector2(0, -384))

        if(self.enemy2.moving == False and int(self.enemy2.isoReal.x) == 1024):       
            self.enemy2Patrol = 1
        elif(self.enemy2.moving == False and int(self.enemy2.isoReal.x) == 0):
            self.enemy2Patrol = 0

        self.camera.getPlayerPosition(self.player.isoMov)

        self.player.Update(self.camera, self.surface)

        self.wall.draw(self.surface, self.player)

        if((self.player.isoReal.x == 4 or self.player.isoReal.x == 5) and self.player.isoReal.y == 9):
            self.SwitchToScene(self.sceneManager.scenesArray[4], pygame.Vector2(4, 1))
            self.Destroy()
            pygame.display.flip()         

    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        pygame.display.update(self.window.display.get_rect())
        
    def Destroy(self):
        self.surface.fill((0,0,0,0))