import torch

from agent.action import BattleSnakeAction
from game.metadata import BattleSnakeGameMetadata
from game.state import BattleSnakeGameState

import torch.nn as nn
import torch.nn.functional as F


class BattleSnakeConvNet(nn.Module):
    def __init__(self, metadata: BattleSnakeGameMetadata):
        state_n_cs = BattleSnakeGameState.NUM_CHANNELS

        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=state_n_cs, out_channels=state_n_cs * 2, kernel_size=(3, 3))
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(in_channels=state_n_cs * 2, out_channels=state_n_cs * 4, kernel_size=(2, 2))
        self.fc1 = nn.Linear(12, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, len(BattleSnakeAction))

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
