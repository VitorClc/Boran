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

class Field2(SceneModel):
    def Start(self, _gameWindow, sceneManager, startPos):
        self.window = _gameWindow
        self.sceneManager = sceneManager

        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/campo2.tmx", self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)), pygame.HWSURFACE)
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        if(startPos != None):
            self.player = Player(self.wall, pygame.Vector2(startPos.x * 128, -startPos.y * 128), self.tilemap, 1)
        else:
            self.player = Player(self.wall, pygame.Vector2(512,-768), self.tilemap, 1)

        self.player.canInteract = True
        self.player.useDepth = True
        
        self.camera = PlayerFollow(self.player.cartesianPos)
        self.dialogue = Dialogue()

        self.firstDialogue = False
        self.secondDialogue = False
        self.thirdDialogue = False
        self.fourthDialogue = False

        self.createdSunan = False
        self.startDialog = False
        pygame.display.flip()

    def ProcessInput(self, event, pressed_keys):
        self.isoPos = self.tilemap.cartesianToIsometric(pygame.Vector2(pygame.mouse.get_pos()[0] - self.camera.x, - self.camera.y + pygame.mouse.get_pos()[1] - 128))
        self.player.ProcessInputs(self.isoPos)

        if(self.firstDialogue == True & (len(self.dialogue.text) < len(self.dialogue.completeText))):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dialogue.text = self.dialogue.completeText
        elif(len(self.dialogue.text) == len(self.dialogue.completeText)):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(self.secondDialogue == False):
                    self.dialogue.setCharName("Sunan")
                    self.dialogue.setText("Me chamo Sunan...")
                    self.secondDialogue = True

                elif(self.thirdDialogue == False):
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Sunan!? Meu irmão pediu para te procurar. Antes de morrer...\n Ele disse que você pode trazer paz para o nosso povo")
                    self.thirdDialogue = True
                elif(self.fourthDialogue == False):
                    self.dialogue.setCharName("Sunan")
                    self.dialogue.setText("Voltei para treinar uma elite de guerreiros, pessoas que tem coragem\nsuficiente para expulsar os invasores")
                    self.thirdDialogue = True
            
    def Update(self):
        self.surface.fill((0,0,0))
        self.tilemap.DrawGround(self.surface, self.camera)
        pygame.display.update(self.tilemap.groundSprite)

        self.camera.getPlayerPosition(self.player.isoMov)

        self.player.Update(self.camera, self.surface)

        self.wall.draw(self.surface, self.player)


        if(len(self.dialogue.text) < len(self.dialogue.completeText)):
            self.dialogue.updateText()

        if(self.createdSunan == True):
            self.Sunan.Update(self.surface)

        if(self.player.isoReal.x == 4 and self.player.isoReal.y == 3):
            self.player.canInteract = False

            if(self.createdSunan == False):
                self.Sunan = Sunan(self.wall, pygame.Vector2(512, 0), self.tilemap, 1)
                self.createdSunan = True
            
            if(self.startDialog == False and self.createdSunan == True):
                self.Sunan.goToPosition(pygame.Vector2(512, -256))

            if(self.Sunan.moving == False and int(self.Sunan.isoReal.y) > -258):
                self.player.lastDir = 1
                self.startDialog = True
                
            if(self.startDialog == True and self.firstDialogue == False):
                self.dialogue.setCharName("???")
                self.dialogue.setText("Agora nós estamos seguros")
                self.firstDialogue = True

    def Render(self):
        self.window.display.blit(self.surface,(self.camera.x, self.camera.y))
        if(self.startDialog == True):
            self.dialogue.Draw(self.window.display)
        pygame.display.update(self.window.display.get_rect())
        
    def Destroy(self):
        self.surface.fill((0,0,0,0))