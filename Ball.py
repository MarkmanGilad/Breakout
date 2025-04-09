import pygame
from Constants import*
from math import hypot,sin,cos,atan
from Block import*
from random import random
class Ball(pygame.sprite.Sprite):
    def __init__(self, image,dx,dy) -> None:
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect()
        self.dx=dx
        self.dy=dy

    def collide_block(self,rect):
        if pygame.sprite.collide_rect(self,rect):
            v=hypot(self.dx,self.dy)
            angle=atan((self.rect.centerx-rect.rect.centerx)/(rect.rect.width/2))

            if abs(angle) < 0.1:
                if angle<0:
                    angle=-0.12
                else:
                    angle=0.12

            self.dx=v*sin(angle)
            self.dy=-v*cos(angle)
            return True
        return False

    def collide_brick(self,collided):
        if self.rect.leftx>=collided[0].rect.left and self.rect.rightx<=collided[0].rect.right:
            self.dy*=-1
        else:
            self.dx*=-1

    def move(self):
        x,y=self.rect.midtop
        if y<=70:
            y=70
            self.dy=self.dy*-1
        if x>=WIDTH-70:
            x=WIDTH-70
            self.dx=self.dx*-1
        if x<=70:
            x=70
            self.dx=self.dx*-1

        x=x+self.dx
        y=y+self.dy
        self.rect.midtop=x,y

    def draw(self,surface):
        surface.blit(self.image,self.rect)