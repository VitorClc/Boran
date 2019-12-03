import pygame, math, time

from Core.Scenes import SceneModel
from Core.Tilemap import Loader
from Core.Dialogue import Dialogue

from OBJECTS.Player import Player
from OBJECTS.Kamon import Kamon

soundsDir = "SOUNDS/"
pygame.mixer.init()
explosion = pygame.mixer.Sound(soundsDir + "explosion.ogg")
explosion.set_volume(0.5)

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

class Academy(SceneModel):
    def Start(self, _gameWindow, sceneManager, startPos):
        self.window = _gameWindow
        self.sceneManager = sceneManager

        self.wall = YAwareGroup()

        self.tilemap = Loader("MAPS/academia_000.tmx", self.wall)
        
        self.surface = pygame.Surface(((self.tilemap.mapSize.x * self.tilemap.tileSize.x) + 32, self.tilemap.mapSize.y * self.tilemap.tileSize.y + (self.tilemap.tileSize.y * 2)), pygame.HWSURFACE)
        self.surface.get_rect().centerx = (self.tilemap.tileSize.x * self.tilemap.mapSize.x) / 2
        self.surface.get_rect().centery = (self.tilemap.tileSize.y * self.tilemap.mapSize.y) / 2

        self.tilemap.Generate(self.surface, pygame.Vector2(-6,5))

        if(startPos != None):
            self.player = Player(self.wall, pygame.Vector2(startPos.x * 128, -startPos.y * 128), self.tilemap, 1)
        else:
            self.player = Player(self.wall, pygame.Vector2(512,-768), self.tilemap, 1)

        self.player.canInteract = False
        self.player.useDepth = False
        
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

        self.kamon = Kamon(self.wall, pygame.Vector2(512, -640), self.tilemap, 0)

        self.camera = PlayerFollow(self.player.cartesianPos)
    
    def explosion(self, width, height): 
        surface = pygame.Surface((width, height))
        explosion.play()
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
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Espero me tornar um grande guerreiro igual você! Quando os \nmonges te levarão para receber o treinamento para ser um mestre?")
                    self.secondDialogue = True
                elif(self.thirdDialogue == False):
                    self.dialogue.setCharName("Kamon")
                    self.dialogue.setText("Quando eu estiver preparado... Os monges estão se isolando na \nfloresta dos Ventos... Acredito que isso tem alguma ligação com as \nnotícias recentes...")
                    self.thirdDialogue = True
                elif(self.fourthDialogue == False):
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Notícias?")
                    self.fourthDialogue = True
                elif(self.fifthDialogue == False):
                    self.dialogue.setCharName("Kamon")
                    self.dialogue.setText("Sim, sobre o terrível Harrison \"The Hunter\" e seu império Apolda. \nDiversos povos já foram escravizados ou dizimados.")
                    self.fifthDialogue = True
                elif(self.sixthDialogue == False):
                    self.dialogue.setCharName("Boran")
                    self.dialogue.setText("Temos fortes guerreiros, todos nós somos muito bem treinados!")
                    self.sixthDialogue = True
                elif(self.seventhDialogue == False):
                    self.dialogue.setCharName("Kamon")
                    self.dialogue.setText("Meu jovem irmão, pelos boatos que ouvi, um dos maiores mestres \nde Muay Thai caiu diante de um jovem mago Apolda... Os nossos \nmelhores guerreiros são ineficazes sem o equilíbrio da natureza...")
                    self.seventhDialogue = True  
                else:
                    self.SwitchToScene(self.sceneManager.scenesArray[2], None)
                    self.dialogue.visible = False
                    self.explosion(1920, 1080)
                    #self.player.canInteract = True                                  

    def Update(self):
        self.surface.fill((0,0,0))
        self.tilemap.DrawGround(self.surface, self.camera)
        pygame.display.update(self.tilemap.groundSprite)

        self.camera.getPlayerPosition(self.player.isoMov)

        self.player.Update(self.camera, self.surface)
        self.kamon.Update(self.surface)

        self.wall.draw(self.surface, self.player)
        
        if(self.firstDialogue == False):
            self.dialogue.setCharName("Kamon")
            self.dialogue.setText("Fico muito feliz pelo seu aprendizado, meu irmão. Um dia você se \ntornará um grande homem!")
            self.firstDialogue = True

        if(len(self.dialogue.text) < len(self.dialogue.completeText)):
            self.dialogue.updateText()

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