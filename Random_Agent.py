from typing import Any
import pygame
from Constants import*
from Block import *
import random as rnd

class Random_Agent:
    def __init__(self) -> None:
        pass

    def GetAction(self,event, env):
        match rnd.choice((-2,-1,1,2)):
            case 1:
               env.right = True
            case -1:
               env.left = True
            case 2:
               env.right = False
            case -2:
               env.left = False
           
    
    def __call__(self) -> Any:
         self.GetAction()