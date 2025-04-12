import torch
import random
import math
from DQN_simple import DQN
from Constants import *


class DQN_Agent:
    def __init__(self, parametes_path = None, train = False, device = torch.device('cpu')):
        self.DQN = DQN(device=device)
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train = train
        self.setTrainMode()
        self.actions_choosen = {0: {-1: 0, 0: 0, 1: 0}}
        self.actions_choosen_epsilon = {0: {-1: 0, 0: 0, 1: 0}}

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def GetAction (self, epoch = 0, events= None,env=None,state=None) -> tuple:
        # if state is None: state = env.getState()
        actions = [-1,0,1]
        if self.train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                res = random.choice(actions)
                actions_results_epsilon = self.actions_choosen_epsilon.get(epoch, {-1:0, 0:0, 1:0})
                actions_results_epsilon[res] += 1
                self.actions_choosen_epsilon[epoch] = actions_results_epsilon
                return res
        
        with torch.no_grad():
            Q_values = self.DQN(state)
        max_index = torch.argmax(Q_values)
        res = actions[max_index]
        actions_results = self.actions_choosen.get(epoch, {-1:0, 0:0, 1:0})
        actions_results[res] += 1
        self.actions_choosen[epoch] = actions_results
        return res

    def get_Actions_Values (self, states):
        with torch.no_grad():
            Q_values = self.DQN(states)
            max_values, max_indices = torch.max(Q_values,dim=1) # best_values, best_actions
        
        return max_indices.reshape(-1,1), max_values.reshape(-1,1)

    def Q (self, states, actions):
        Q_values = self.DQN(states) 
        rows = torch.arange(Q_values.shape[0]).reshape(-1,1)
        cols = actions.reshape(-1,1)
        return Q_values[rows, cols]

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        # res = final + (start - final) * math.exp(-1 * epoch/decay)
        if epoch < decay:
            return start - (start - final) * epoch/decay
        return final
        
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def fix_update (self, dqn, tau=0.001):
        self.DQN.load_state_dict(dqn.state_dict())

    def soft_update (self, dqn, tau=0.001):
        with torch.no_grad():
            for dqn_hat_param, dqn_param in zip(self.DQN.parameters(), dqn.parameters()):
                dqn_hat_param.data.copy_(tau * dqn_param.data + (1.0 - tau) * dqn_hat_param.data)

    def get_Actions_Values (self, states):
        with torch.no_grad():
            Q_values = self.DQN(states)
            max_values, max_indices = torch.max(Q_values,dim=1) # best_values, best_actions
        
        return max_indices.unsqueeze(1), max_values.unsqueeze(1)
    # def __call__(self, events= None, state=None):
    #     return self.GetAction(state)