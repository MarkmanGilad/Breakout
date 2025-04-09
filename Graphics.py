import pygame
from Ball import*
from Block import*
from Brick import*
from Constants import*
import random
pygame.init()
background=pygame.transform.scale(pygame.image.load("img/background.png"),(WIDTH,HEIGHT))
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Breakout")
clock=pygame.time.Clock() 
font=pygame.font.Font("fonts/score_font.ttf",60)

ball_img=pygame.image.load("img/ball.png")
ball_img=pygame.transform.scale(ball_img,(15,15))

block_img=pygame.image.load("img/block.png")
block_img=pygame.transform.scale(block_img,(100,20))







