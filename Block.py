import pygame
from Constants import*
class Block(pygame.sprite.Sprite):
    def __init__(self, image) -> None:
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect()

    def move(self,dx):
        x,y= self.rect.midbottom
        if(x+50<WIDTH-70 and x-50>70):
            x+=dx
        elif(x+50>=WIDTH-70 and dx<0):
            x+=dx
        elif(x-50<=70 and dx>0):
            x+=dx
        elif x-50<=70:
            x=120
        else:
            x=WIDTH-120
        self.rect.midbottom=x,y

    def draw(self,surface):
        surface.blit(self.image,self.rect)