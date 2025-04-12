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
        self.temp = 2.0            # start high
        self.min_temp = 0.01       # avoid full greed
        self.temp_decay = 0.995    # decay rate

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def GetAction (self, epoch = 0, events= None,env=None,state=None) -> tuple:
        # if state is None: state = env.getState()
        actions = [-1,0,1]
        with torch.no_grad():
            # Ensure state has batch dimension
            # state = state.to(self.device)
            Q_values = self.DQN(state)
        
        if self.train:
            index = self.softmax_action_selection(Q_values, self.temp)
            self.temp = max(self.min_temp, self.temp * self.temp_decay)
        else:
            index = torch.argmax(Q_values).item()
        return actions[index]


    def softmax_action_selection(self, q_values, temp=0.1):
        q_values = q_values.squeeze(0)
        probs = torch.softmax(q_values / temp, dim=-1)
        return torch.multinomial(probs, num_samples=1).item() 

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