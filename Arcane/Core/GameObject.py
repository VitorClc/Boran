import pygame
from abc import ABC, abstractmethod

class GameObjectBase(object):
    def __init__(self, x, y):
        self.position = [x,y]

    @abstractmethod
    def Start(self):
        print("Game Object start")

    @abstractmethod
    def ProcessInputs():
        print("Processing Inputs")

    @abstractmethod
    def Render(self, _gameWindow):
        print("Updating Game Object")