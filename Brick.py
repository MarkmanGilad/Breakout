from colorsys import hsv_to_rgb
import pygame
from Constants import*
class Brick(pygame.sprite.Sprite):
    def __init__(self, width,height,color,row,col,padding) -> None:
        super().__init__()
        self.image=pygame.Surface((width-padding,height-padding)) 
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.row=row
        self.col=col