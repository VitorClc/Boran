import pygame, sys
from abc import ABC, abstractmethod

class SceneManager:
    def __init__(self, _scenesArray, _sceneIndex, _gameWindow):
       self.scenesArray = _scenesArray
       self.actualScene = self.scenesArray[_sceneIndex]
       self.window = _gameWindow

    def InitScene(self):
        self.actualScene.Start(self, self.window)

    def UpdateScene(self):
        self.actualScene.Update(self)
        self.actualScene.Render(self)
        self.actualScene.CheckQuit(self)

class SceneModel(ABC):
    @abstractmethod
    def Init(self):
        print("Starting scene")
   
    @abstractmethod
    def Update(self):
        print("Updating scene")
    
    def Render(self):
        print("Rendering scene")

    def CheckQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)