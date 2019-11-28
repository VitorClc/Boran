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
        self.followPlayer = True

    def getPlayerPosition(self, playerPos):
        if(self.followPlayer == True):
            self.x = -playerPos.x + 1000
            self.y = -playerPos.y + 400
    
    def goToPosition(self, position, debug):
        if(self.followPlayer == False):
            if(position.x < self.x):
                dX = -10
            elif(position.x > self.x):
                dX = 10
            elif(position.x == self.x):
                dX = 0
            
            self.x += dX

            if(debug == True):
                print(self.x)

    def getPositionX(self):
        return self.x

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

            if(hasattr(spr, "visible") == False):
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)

        self.lostsprites = []

class Ruins(SceneModel):
    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow
        self.sceneManager = sceneManager

        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/academia_001.tmx", self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)), pygame.HWSURFACE)
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        self.player = Player(self.wall, pygame.Vector2(512,-768), self.tilemap, 1)
        self.player.canInteract = False
        self.player.useDepth = False
        self.player.standUp = True
        
        self.dialogue = Dialogue()
        #self.fade(1920, 1080)

        ##CUTSCENES
        self.firstDialogue = False
        self.secondDialogue = False
        self.thirdDialogue = False
        self.fourthDialogue = False
        self.fifthDialogue = False
        self.sixthDialogue = False
        self.seventhDialogue = False
        self.cameraDragToEnemies = False
        self.createdEnemies = False
        self.finishedEnemyDialog = False
        self.finishedEnemyDialog2 = False

        self.kamon = Kamon(self.wall, pygame.Vector2(512, -640), self.tilemap, 1)

        self.camera = PlayerFollow(self.player.cartesianPos)
        self.camera.followPlayer = True
        
    def explosion(self, width, height): 
        surface = pygame.Surface((width, height))
        surface.fill((0,0,0))
        for i in range(0, 3):
            pygame.time.delay(300)
            surface.fill((0,0,0))
            pygame.display.update()
            self.window.display.blit(surface, (0,0))
            pygame.display.update()
            surface.fill((255,255,255))
            pygame.time.delay(300)
            pygame.display.update()
            self.window.display.blit(surface, (0,0))
            pygame.display.update()

    def ProcessInput(self, event, pressed_keys):
        self.isoPos = self.tilemap.cartesianToIsometric(pygame.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - 128))
        self.player.ProcessInputs(self.isoPos)

        if(self.firstDialogue == True & (len(self.dialogue.text) < len(self.dialogue.completeText))):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dialogue.text = self.dialogue.completeText
        elif(len(self.dialogue.text) == len(self.dialogue.completeText)):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(self.secondDialogue == False):
                    self.dialogue.setCharName("Kamon")
                    self.dialogue.setText("Ahh!...")
                    self.secondDialogue = True
                elif(self.thirdDialogue == False):
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Irmão, não me deixe! Eu preciso de você, a vila precisa de você...")
                    self.thirdDialogue = True
                elif(self.fourthDialogue == False):
                    self.dialogue.setCharName("Kamon")
                    self.dialogue.setText("Boran, meu fim está próximo mas o seu está longe...\n Preciso que você vá para a Floresta dos Ventos e\n procure por Sunan...")
                    self.fourthDialogue = True
                elif(self.fifthDialogue == False):
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Sunan?")
                    self.fifthDialogue = True
                elif(self.sixthDialogue == False):
                    self.dialogue.setCharName("Kamon")
                    self.dialogue.setText("... E nunca lute com nenhum deles, ainda não estamos preparados...")
                    self.sixthDialogue = True
                elif(self.seventhDialogue == False):
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Irmão??")
                    self.seventhDialogue = True  
                else:
                    self.cameraDragToEnemies = True
                    #self.SwitchToScene(self.sceneManager.scenesArray[2])
                    self.dialogue.visible = False
                    #self.explosion(1920, 1080)
                    #self.player.canInteract = True   
                    #self.player.useDepth = True 

    def Update(self):
        self.surface.fill((0,0,0))
        self.tilemap.DrawGround(self.surface, self.camera)
        pygame.display.update(self.tilemap.groundSprite)

        self.camera.getPlayerPosition(self.player.isoMov)

        self.player.Update(self.camera, self.surface)
        self.kamon.Update(self.surface)

        self.wall.draw(self.surface, self.player)
        
        if(self.firstDialogue == False):
            self.dialogue.setCharName("Boran")
            self.dialogue.setText("Irmão!?")
            self.firstDialogue = True

        if(len(self.dialogue.text) < len(self.dialogue.completeText)):
            self.dialogue.updateText()
        
        if(self.seventhDialogue == True & self.cameraDragToEnemies == True):
            self.camera.followPlayer = False
            self.camera.goToPosition(pygame.Vector2(-1200, 0), False)

            if(self.camera.getPositionX() == -1200):
                if( self.createdEnemies == False):
                    self.enemy2 = NPC(self.wall, pygame.Vector2(896, -1152), self.tilemap, 1)
                    self.enemy = NPC(self.wall, pygame.Vector2(1024, -1152), self.tilemap, 1)
                    self.enemy3 = NPC(self.wall, pygame.Vector2(1152, -1152), self.tilemap, 1)

                    self.createdEnemies = True


        if(self.createdEnemies == True):
            self.enemy.Update(self.surface)
            self.enemy2.Update(self.surface)
            self.enemy3.Update(self.surface)

            if(self.finishedEnemyDialog == False):
                self.enemy.Movement(pygame.Vector2(8, 9), pygame.Vector2(8, 8))
                self.finishedEnemyDialog = True
            

        #if(self.player.isoReal.x == 3 and self.player.isoReal.y == 7):
        #    self.SwitchToScene(self.sceneManager.scenesArray[2])
        #    self.Destroy()
        #    pygame.display.flip()         

    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        self.dialogue.Draw(self.window.display)
        pygame.display.update(self.window.display.get_rect())
        
    def Destroy(self):
        self.surface.fill((0,0,0,0))