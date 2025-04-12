import numpy as np
import torch
from colorsys import hsv_to_rgb
import pygame
from Graphics import*
from Constants import*
from Block import*
from Ball import*
from Brick import*
import random 


class Environment:
    def __init__(self) -> None:
        self.left=False
        self.right=False
        self.score=0
        self.bricks=pygame.sprite.Group()
        self.block=Block(block_img)
        self.ball=Ball(ball_img,0,3*1.412)
        self.ball_group=pygame.sprite.GroupSingle()
        self.i_reward = 0.1
        self.hit_reward = 1
        self.miss_reward = -1
        self.above_reward = 0.2

        self.Block_hit = 0
    
    def move(self,action):
        # dx= hypot(self.ball.dx,self.ball.dy)+3
        dx = 7
        if action==1:
            self.block.move(dx)
        elif action==-1:
            self.block.move(dx*-1)  
        
        self.ball.move()          
        self.collide_brick()
        if self.ball.collide_block(self.block):
            self.Block_hit += 1
        
        reward = self.reward(action)
        done=self.is_end_game()
        return reward,done
        
    def getState(self):
        l = rows*cols
        state = np.zeros(l+8, dtype=np.float32)
        for brick in self.bricks:
            x, y = brick.col, brick.row
            state[x+y*cols] = 1
        bx,by = self.ball.rect.center
        maxV = 6.2
        state[l:l+2] = bx/WIDTH, by/HEIGHT
        state[l+2:l+4] = self.ball.dx/maxV, self.ball.dy/maxV
        x1, y1 = self.block.rect.topleft
        x2, y2 = self.block.rect.bottomright
        state[l+4:] = x1/WIDTH,y1/HEIGHT,x2/WIDTH,y2/HEIGHT
        state = torch.from_numpy(state)
        return state

    def simple_state(self):
        player_x = self.block.rect.midtop[0] / scrwidth
        player_y = self.block.rect.midtop[1] / scrheight
        ball_x = self.ball.x / scrwidth
        ball_y = self.ball.y / scrheight
        ball_dx, ball_dy = self.ball.dx / 5, self.ball.dy / 5
        state = torch.tensor([-player_x-ball_x,player_y-ball_y, ball_dx, ball_dy], dtype=torch.float32)
        return state

    def immidiate_reward (self, state, next_state, action):
        state_dx = state[0].item()
        # next_state_dx = next_state[0].item()
        ball_dx = state[2].item()
        # dist_x = state_dx - ball_dx
        trashhold = 50 / scrwidth    # half the block
        
        if action == -1:
            if abs(state_dx) < trashhold: # stay
                return -self.i_reward        
            elif state_dx < 0:            # right
                return +self.i_reward
            else:                       # left
                return self.i_reward
        elif action == 1:
            if abs(state_dx) < trashhold: # stay
                return -self.i_reward        
            elif state_dx < 0:            # right
                return self.i_reward
            else:                       # left
                return -self.i_reward
        
        else: # action == 0
            if abs(state_dx) < trashhold: # stay
                return self.i_reward        
            elif state_dx < 0:            # right
                return -self.i_reward
            else:                       # left
                return -self.i_reward

    def collide_brick(self):
        collided=pygame.sprite.spritecollide(self.ball,self.bricks,True)
        if collided:
            self.score+=10*collided.__len__()
            if self.ball.rect.center[0]>=collided[0].rect.left and self.ball.rect.center[0]<=collided[0].rect.right:
                self.ball.dy*=-1
            else:
                self.ball.dx*=-1
  
    def is_end_game(self):
        if self.ball.rect.center[1]>HEIGHT-70:
            return True
        if self.bricks.__len__()==0:
            return True
        return False
    
    def reset(self):
        self.left=False
        self.right=False
        self.bricks.empty()
        self.score=0
        self.Block_hit = 0
        # base_x = random.randint(500, WIDTH-500)
        base_x = WIDTH / 2
        self.ball.random_init(base_x)
        self.block.rect.midbottom=(base_x, 800)
        for col in range(cols):
            for row in range(rows):
                brick=Brick(scrwidth/cols,200/rows,[x*255 for x in hsv_to_rgb((col+row)/cols,1,1)],row=row,col=col,padding=2)
                brick.rect.topleft=(70+col*scrwidth/cols,70+row*200/rows)
                
                self.bricks.add(brick)

    def reward(self, action):
        if pygame.sprite.collide_rect(self.ball,self.block):
            return self.hit_reward
        if self.ball.rect.center[1]>HEIGHT-70:
            return self.miss_reward
        # if self.ball.rect.centerx>self.block.rect.topleft[0] and self.ball.rect.centerx<self.block.rect.topright[0]:
        #     return self.above_reward
        # x_distace = abs(self.ball.rect.centerx - self.block.rect.centerx)
        # return -x_distace/WIDTH
        return 0

    def draw(self):
        screen.blit(background,(0,0))
        self.ball.draw(screen)        
        self.bricks.draw(screen)
        self.block.draw(screen)
        text=font.render(f"Score:{self.score}",True,blue)
        screen.blit(text,(90,scrheight))

    
        


