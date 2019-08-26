class SceneManager:
    def __init__(self, _scenesArray, _sceneIndex):
       self.scenesArray = _scenesArray
       self.actualScene = self.scenesArray[_sceneIndex]

    def StartScene(self):
        self.actualScene.Start()

    def UpdateScene(self):
        self.actualScene.Update()

class SceneModel:
    def Start(self):
        print("Starting scene")

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("Updating scene")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")