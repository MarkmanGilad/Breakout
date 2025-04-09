import torch
import pygame
from Graphics import*
from Constants import*
from human_Agent import *
from Random_Agent import*
from Environment import *
from  DQN_Agent import *
pygame.init()


env=Environment()
env.reset()
player=Human_Agent()

def main():
    run =True
    while(run):
        action = None
        run=not env.is_end_game()
        events = pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                run=False
        action=player.GetAction(events=events,env=env)
        print(action)
        env.move(action)
        screen.fill(black)
        env.draw()
        pygame.display.update()
        clock.tick(FPS) 

if __name__=='__main__':
    main()

