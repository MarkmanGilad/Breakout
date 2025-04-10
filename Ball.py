import pygame
from Constants import*
from math import hypot,sin,cos,atan, radians
from Block import*
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, image,dx,dy) -> None:
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect()
        self.rnd_x = 10
        self.rnd_angle = 2 
        # self.random_init()

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

    def random_init (self, base_x):
        speed = 4.2
        angle_deg = random.uniform(90 - self.rnd_angle, 90 + self.rnd_angle)
        angle = radians(angle_deg)
        self.dx = cos(angle) * speed
        self.dy = sin(angle) * speed

        x = random.uniform(base_x - self.rnd_x, base_x + self.rnd_x)
        self.rect.midbottom=(x ,HEIGHT*0.33)

        self.rnd_angle += 0.05
        self.rnd_angle = min(self.rnd_angle, 50)

        self.rnd_x += 0.1
        self.rnd_x = min(self.rnd_x, WIDTH/2-300)
