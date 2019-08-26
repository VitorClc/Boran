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

class SceneModel(ABC):
    @abstractmethod
    def Start(self):
        print("Starting scene")
    
    @abstractmethod
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    @abstractmethod
    def Update(self):
        print("Updating scene")
    
    @abstractmethod
    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")