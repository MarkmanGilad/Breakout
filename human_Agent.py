from typing import Any
import pygame
from Constants import*
from Block import *

class Human_Agent:
    def __init__(self) -> None:
        pass
    

    def GetAction(self,events, env):
        for event in events:
            if event.type==pygame.KEYDOWN:
                
                if event.key==pygame.K_RIGHT:
                    env.right = True

                elif event.key==pygame.K_LEFT:
                    env.left = True

            elif event.type==pygame.KEYUP:

                if event.key==pygame.K_RIGHT:
                    env.right = False

                elif event.key==pygame.K_LEFT:
                    env.left = False
        
    def __call__(self,event) -> Any:
         self.GetAction(event)

