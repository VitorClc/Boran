import pygame, math, time

from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Dialogue import Dialogue

from OBJECTS.Player import Player
from OBJECTS.Kamon import Kamon
from OBJECTS.NPC import NPC
from OBJECTS.Sunan import Sunan

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

class Field(SceneModel):
    def Start(self, _gameWindow, sceneManager, startPos):
        self.window = _gameWindow
        self.sceneManager = sceneManager

        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/campo_000.tmx", self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)), pygame.HWSURFACE)
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        if(startPos != None) :
            self.player = Player(self.wall, pygame.Vector2(startPos.x * 128, -startPos.y * 128), self.tilemap, 1)
        else:
            self.player = Player(self.wall, pygame.Vector2(1152,-384), self.tilemap, 1)

        self.enemyCreated = False
        
        self.enemyPatrol = 0
        self.enemy2Patrol = 0

        self.player.canInteract = True
        self.player.useDepth = True
        
        self.camera = PlayerFollow(self.player.cartesianPos)
        self.dialogue = Dialogue()

        self.firstDialogue = False
        self.secondDialogue = False
        self.thirdDialogue = False

        self.createdSunan = False
        self.sunanCutscene = 0

    def ProcessInput(self, event, pressed_keys):
        self.isoPos = self.tilemap.cartesianToIsometric(pygame.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - 128))
        self.player.ProcessInputs(self.isoPos)

        if(self.firstDialogue == True & (len(self.dialogue.text) < len(self.dialogue.completeText))):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dialogue.text = self.dialogue.completeText
        elif(len(self.dialogue.text) == len(self.dialogue.completeText)):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(self.secondDialogue == False):
                    self.dialogue.setCharName("Soldados")
                    self.dialogue.setText("Parado !!")
                    self.secondDialogue = True

                if(self.sunanCutscene == 3):
                    self.dialogue.visible = False
                    self.player.canInteract = True

    def Update(self):
        self.surface.fill((0,0,0))
        self.tilemap.DrawGround(self.surface, self.camera)
        pygame.display.update(self.tilemap.groundSprite)

        if(self.enemyCreated == True):
            self.enemy.Update(self.surface)
            self.enemy2.Update(self.surface)

        self.camera.getPlayerPosition(self.player.isoMov)

        self.player.Update(self.camera, self.surface)

        self.wall.draw(self.surface, self.player)

        if(self.player.isoReal.x == 3 and (self.player.isoReal.y == 7 or self.player.isoReal.y == 8)):
            self.player.canInteract = False

            if(self.enemyCreated == False):
                self.enemy = NPC(self.wall, pygame.Vector2(0, -896), self.tilemap, 1)
                self.enemy2 = NPC(self.wall, pygame.Vector2(0, -1024), self.tilemap, 1)
                self.enemyCreated = True

        if(self.enemyCreated == True):
            if(self.enemyPatrol == 0):
                self.enemy.goToPosition(pygame.Vector2(128, -896))

            if(self.enemy.moving == False and int(self.enemy.isoReal.x) >= 126):       
                self.enemyPatrol = 1

            if(self.enemy2Patrol == 0):
                self.enemy2.goToPosition(pygame.Vector2(128, -1024))

            if(self.enemy2.moving == False and int(self.enemy2.isoReal.x) >= 126):       
                self.enemy2Patrol = 1

            if(self.enemyPatrol == 1 and self.enemy2Patrol == 1):
                if(self.firstDialogue == False):
                    self.dialogue.setCharName("Soldados")
                    self.dialogue.setText("Encontramos você !!")
                    self.dialogue.visible = True
                    self.firstDialogue = True
        
                if(len(self.dialogue.text) < len(self.dialogue.completeText)):
                    self.dialogue.updateText()
            
            if(self.secondDialogue == True and self.thirdDialogue == False and self.createdSunan == False):
                self.Sunan = Sunan(self.wall, pygame.Vector2(1152, -1024), self.tilemap, 1)
                self.createdSunan = True
                    

            if(self.createdSunan == True):
                self.Sunan.Update(self.surface)

                if(self.sunanCutscene == 0):
                    self.Sunan.goToPosition(pygame.Vector2(256, -1024))
                elif(self.sunanCutscene == 1):
                    self.Sunan.voadoraAct = True
                    self.enemy2.die = True
                    if(self.Sunan.finishedVoadora == True):
                        self.sunanCutscene = 2
                elif(self.sunanCutscene == 2):
                    self.Sunan.kickAct = True

                    if(self.Sunan.finishedKick == True):
                        self.sunanCutscene = 3
                        self.dialogue.setCharName("???")
                        self.dialogue.setText("Corre")
                        self.dialogue.visible = True
            
                if(self.sunanCutscene == 2 or self.sunanCutscene == 3):
                    if(self.enemy2.die == False):
                        self.enemy.die = True

                if(self.Sunan.moving == False and int(self.Sunan.isoReal.x) <= 300 and self.sunanCutscene == 0):
                    self.sunanCutscene = 1  

        if(self.player.isoReal.x == 4 and self.player.isoReal.y == 9):
            self.SwitchToScene(self.sceneManager.scenesArray[5], pygame.Vector2(4,0))
            self.Destroy()
            pygame.display.flip()     

    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        if(self.enemyPatrol == 1 and self.enemy2Patrol == 1):
            self.dialogue.Draw(self.window.display)
        pygame.display.update(self.window.display.get_rect())
        
    def Destroy(self):
        self.surface.fill((0,0,0,0))