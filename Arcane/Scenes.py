class SceneManager:

    def __init__(self, _scenesArray, _sceneIndex):
       self.scenesArray = _scenesArray
       self.actualScene = self.scenesArray[_sceneIndex]

    def UpdateScene():
        self.actualScene.Update()

class SceneModel:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")