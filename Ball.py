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
        self.rnd_x = 100
        self.rnd_angle = 20
        self.x = WIDTH / 2
        self.y = HEIGHT*0.33
        # self.random_init()

    def collide_block(self,block_rect):
        if pygame.sprite.collide_rect(self,block_rect):
            v=hypot(self.dx,self.dy)
            angle=atan((self.rect.centerx-block_rect.rect.centerx)/(block_rect.rect.width/2))

            if abs(angle) < 0.1:
                angle = random.choice([-0.12, 0.12])

            self.dx=v*sin(angle)
            self.dy=-v*cos(angle)
            return True
        return False

    def collide_brick(self,collided):
        if self.rect.left>=collided[0].rect.left and self.rect.right<=collided[0].rect.right:
            self.dy*=-1
        else:
            self.dx*=-1

    def move(self):
        # Update float position
        self.x += self.dx
        self.y += self.dy
        
        if self.y <= 70:
            self.y=70
            self.dy *= -1
        
        if self.x >= WIDTH - 70:
            self.x = WIDTH-70
            self.dx *= -1
        
        if self.x <= 70:
            self.x = 70
            self.dx *= -1

        self.rect.midtop= round(self.x), round(self.y)

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def random_init (self, base_x):
        speed = 4.2
        angle_deg_down = random.uniform(90 - self.rnd_angle, 90 + self.rnd_angle)
        # angle_deg_up = random.uniform(270 - self.rnd_angle, 270 + self.rnd_angle)
        # angle_deg = random.choice([angle_deg_down, angle_deg_up])
        angle = radians(angle_deg_down)
        self.dx = cos(angle) * speed
        self.dy = sin(angle) * speed
        
        self.y = 300 #HEIGHT / 2
        # self.x = random.uniform(base_x - self.rnd_x, base_x + self.rnd_x)
        self.x = WIDTH / 2
        self.rect.center=(round(self.x) ,round(self.y))

        self.rnd_angle += 0.1
        self.rnd_angle = min(self.rnd_angle, 50)

        self.rnd_x += 0.5
        self.rnd_x = min(self.rnd_x, WIDTH/2-300)
