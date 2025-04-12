import pygame
import torch
from Constants import *
from Environment import Environment
from DQN_simple_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from Graphics import*
import os
import wandb

def main (chkpt):

    pygame.init()

    env = Environment()

    best_score = 0

    #region###### params ############
    player = DQN_Agent(train=True)
    player_hat = DQN_Agent(train=True)
    player_hat.DQN = player.DQN.copy()
    batch_size = 64
    buffer = ReplayBuffer(path=None)
    learning_rate = 0.001
    ephocs = 200000
    start_epoch = 0
    C = 5
    MIN_BUFFER = 5000
    loss = torch.tensor(-1)
    avg = 0
    scores, losses, avg_score = [], [], []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000, gamma=0.50)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000], gamma=0.5)
    step = 0
    chk = chkpt
    render= 1
    #endregion
    #region ######## checkpoint Load ############
    checkpoint_path = f"Data/checkpoint{chk}.pth"
    buffer_path = f"Data/buffer{chk}.pth"
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']+1
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        losses = checkpoint['loss']
        scores = checkpoint['scores']
        avg_score = checkpoint['avg_score']
    player.DQN.train()
    player_hat.DQN.eval()

    wandb.init(
            project="Breakout",
            id=f"Breakout{chk}",

            config={
                "learning_rate": learning_rate,
                "epochs": ephocs,
                "batch":batch_size,
                "C": C,
            }
        )

    #endregion################################

    for epoch in range(start_epoch, ephocs):
        env.reset()
        end_of_game = False
        state = env.simple_state()
        step = 0
        while not end_of_game:

            if(render==1):
                env.draw()
            pygame.display.update()
            print (step, end='\r')
            step += 1
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:

                    if event.key==pygame.K_END:
                        render*=-1

            ############## Sample Environement #########################
            action = player.GetAction(state=state, epoch=epoch)
            reward, done = env.move(action=action)
            next_state = env.simple_state()
            reward += env.immidiate_reward(state, next_state, action)
            buffer.push(state, torch.tensor(action, dtype=torch.int32), torch.tensor(reward, dtype=torch.float32), 
                        next_state, torch.tensor(done, dtype=torch.float32))
            if done:
                best_score = max(best_score, env.score)
                break

            state = next_state
            # clock.tick(FPS)
            
            if len(buffer) < MIN_BUFFER:
                continue
    
            ############## Train ################
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = player.Q(states, actions)
            # next_actions, Q_hat_Values = player_hat.get_Actions_Values(next_states)  # DQN
            next_actions, _ = player.get_Actions_Values(next_states)
            Q_hat_Values = player_hat.Q(next_states,next_actions)                       # DDQN
            
            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            scheduler.step()

        if epoch % C == 0:
            player_hat.DQN.load_state_dict(player.DQN.state_dict())

        #region #####   loging and printing ###################################
       
        print (f'chkpt: {chk} epoch: {epoch} loss: {loss:.7f} LR: {scheduler.get_last_lr()} step: {step} ' \
               f'score: {env.score} best_score: {best_score}')
        
        if epoch % 10 == 0:
            scores.append(env.score)
            losses.append(loss.item())

        avg = (avg * (epoch % 10) + env.score) / (epoch % 10 + 1)
        if (epoch + 1) % 10 == 0:
            avg_score.append(avg)
            print (f'average score last 10 games: {avg} ')
            avg = 0
        wandb.log({"step": step, 
                   "loss": loss, 
                   "score": env.score, 
                   "best score": best_score, 
                   "average score": avg,
                   "hits": env.Block_hit
                   })
                

        if epoch % 1000 == 0 and epoch > 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'loss': losses,
                'scores':scores,
                'avg_score': avg_score
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)
        #endregion
    
    wandb.finish()


if __name__ == "__main__":
    if not os.path.exists("Data/checkpoint_num"):
        torch.save(20, "Data/checkpoint_num")    
    
    chkpt = torch.load("Data/checkpoint_num")
    chkpt += 1
    torch.save(chkpt, "Data/checkpoint_num")    
    main (chkpt)
    