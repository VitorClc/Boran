import pygame, sys
from Core.Text import Text

class SceneManager:
    def __init__(self, _scenesArray, _sceneIndex, _gameWindow):
        self.scenesArray = _scenesArray
        self.activeScene = self.scenesArray[_sceneIndex]
        self.window = _gameWindow
        self.activeScene.Start(self.window, self)

        ### DEBUG MODE ###
        self.debug = False
        self.mousePosIsoText = Text("FPS Text", 25, pygame.Vector2(1800, 0), self.window.display, (255,0,0))

    def UpdateScene(self, clock):
        pressed_keys = pygame.key.get_pressed()

        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                
                if event.key == pygame.K_F1:
                    self.debug = not self.debug

            if quit_attempt:
                self.activeScene.Terminate()
            else:
                filtered_events.append(event)
            
            self.activeScene.ProcessInput(event, pressed_keys)
        
        self.activeScene.Update()
        self.activeScene.Render()
        
        if(self.debug == True):
            self.mousePosIsoText.setText("FPS Text: " + str(int(clock.get_fps())))
            self.mousePosIsoText.drawText()
            pygame.display.update(self.mousePosIsoText.textSprite)

        self.activeScene = self.activeScene.next
        
class SceneModel():
    def __init__(self):
        self.next = self

    def Start(self, _gameWindow, sceneManager):
        self.window = _gameWindow
        self.sceneManager = sceneManager
        pass

    def ProcessInput(self, event, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
        if(next_scene != None):
            self.next.Start(self.window, self.sceneManager)
        
    def Terminate(self):
        self.SwitchToScene(None)