import pygame, sys

class SceneManager:
    def __init__(self, _scenesArray, _sceneIndex, _gameWindow):
       self.scenesArray = _scenesArray
       self.activeScene = self.scenesArray[_sceneIndex]
       self.window = _gameWindow
       self.activeScene.Start(self.window)

    def UpdateScene(self):
        self.window.display.fill((0,0,0))
        pressed_keys = pygame.key.get_pressed()
        
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
            
            if quit_attempt:
                self.activeScene.Terminate()
            else:
                filtered_events.append(event)
        
        self.activeScene.ProcessInput(filtered_events, pressed_keys)
        self.activeScene.Update()
        self.activeScene.Render()
        
        self.activeScene = self.activeScene.next
        
class SceneModel():
    def __init__(self):
        self.next = self
    
    def Start(self, _gameWindow):
        pass

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)