import torch

from agent.action import BattleSnakeAction
from game.state import BattleSnakeGameState

import torch.nn as nn
import torch.nn.functional as F


class BattleSnakeConvNet(nn.Module):
    def __init__(self):
        state_n_cs = BattleSnakeGameState.NUM_CHANNELS

        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=state_n_cs, out_channels=state_n_cs, kernel_size=(2, 2))
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(in_channels=state_n_cs, out_channels=state_n_cs * 2, kernel_size=(2, 2))
        self.fc1 = nn.Linear(16, 120)
        self.fc2 = nn.Linear(120, len(BattleSnakeAction))

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x
