from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import ExponentialLR, ReduceLROnPlateau
from tqdm import tqdm
import pandas as pd
import plotly.express as px

from agent.action import BattleSnakeAction
from definitions import TORCH_DEVICE, ROOT_PATH
from game.state import BattleSnakeGameState, _display_state_tensor


class BattleSnakeConvNet(nn.Module):
    def __init__(self):
        state_n_cs = BattleSnakeGameState.NUM_CHANNELS

        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=state_n_cs, out_channels=state_n_cs * 2, kernel_size=(3, 3))
        self.conv2 = nn.Conv2d(in_channels=state_n_cs * 2, out_channels=state_n_cs * 4, kernel_size=(2, 2))
        self.fc1 = nn.Linear(2592, 1024)
        self.fc2 = nn.Linear(1024, 120)
        self.fc3 = nn.Linear(120, len(BattleSnakeAction))

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def load_model(self, model_path: Path):
        self.load_state_dict(torch.load(str(model_path), map_location=TORCH_DEVICE))

    def train_from_transitions(self, transitions, batch_size=32, num_epochs=2, batch_print_occurrence=1000, plot=True):
        criterion = nn.CrossEntropyLoss().to(TORCH_DEVICE)
        optimizer = optim.Adam(self.parameters(), lr=0.0002)
        scheduler = ReduceLROnPlateau(optimizer, 'min')

        model_actions = []
        labels = []
        losses = []
        for epoch in range(num_epochs):
            print("Epoch", epoch)
            running_loss = 0.0
            # Iterate through data points while ensuring we don't access out of bounds
            for i in tqdm(range(len(transitions))[::batch_size][:-1]):
                batch_data = [[transitions[j].prev_state, transitions[j].action] for j in range(i, i + batch_size)]
                x, y = zip(*batch_data)
                x = torch.stack(x, dim=0).to(TORCH_DEVICE).float()
                y = torch.stack(y, dim=0).to(TORCH_DEVICE).float()
                y_class_idx = torch.max(y, 1)[1]
                labels.extend(y_class_idx.tolist())
                # zero the parameter gradients
                optimizer.zero_grad()

                outputs = self(x)
                model_actions.extend([x.argmax() for x in outputs.detach().cpu().numpy()])
                loss = criterion(outputs, y_class_idx)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                if i % batch_print_occurrence == 0 and i > 0:
                    batch_eval_loss = running_loss / batch_print_occurrence
                    print('[%d, %5d] loss: %.5f' %
                          (epoch + 1, i + 1, batch_eval_loss))
                    losses.append(batch_eval_loss)
                    scheduler.step(batch_eval_loss)
                    running_loss = 0.0

        if plot:
            loss_df = pd.DataFrame(list(enumerate(losses)), columns=["idx", "loss"])
            fig = px.line(loss_df, x="idx", y="loss")
            fig.write_image(str(ROOT_PATH / "agent/model/log/loss_graph.png"))

            outputs_df = pd.DataFrame([(x) for x in model_actions], columns=["action"])
            fig = px.histogram(outputs_df, x="action")
            fig.write_image(str(ROOT_PATH / "agent/model/log/train_action_hist.png"))

            labels_df = pd.DataFrame([(x) for x in labels], columns=["action"])
            fig = px.histogram(labels_df, x="action")
            fig.write_image(str(ROOT_PATH / "agent/model/log/train_action_labels_hist.png"))

    def evaluate_on_transitions(self, transitions, batch_size=1, display_tensors=False):

        model_actions = []
        labels = []
        test = transitions
        correct_count, all_count = 0, 0
        for i in tqdm(range(len(test))[::batch_size][:-1]):
            batch_data = [[transitions[j].prev_state, transitions[j].action] for j in range(i, i + batch_size)]
            x, y = zip(*batch_data)
            x = torch.stack(x, dim=0).to(TORCH_DEVICE).float()
            y = torch.stack(y, dim=0).to(TORCH_DEVICE).float()
            y_class_idx = torch.max(y, 1)[1]
            labels.extend(y_class_idx.tolist())

            with torch.no_grad():
                logps = self(x)
            ps = torch.exp(logps)
            model_actions.extend([x.argmax() for x in ps.cpu().numpy()])
            if display_tensors:
                _display_state_tensor(x[0])
                print(ps, y_class_idx)
            for i in range(len(ps)):
                if ps[i].argmax() == y_class_idx[i]:
                    correct_count += 1
                all_count += 1

        print("Number Of States Tested =", all_count)
        print("\nModel Accuracy =", (correct_count / all_count))

        outputs_df = pd.DataFrame([(x) for x in model_actions], columns=["action"])
        fig = px.histogram(outputs_df, x="action")
        fig.write_image(str(ROOT_PATH / "agent/model/log/test_action_hist.png"))

        labels_df = pd.DataFrame([(x) for x in labels], columns=["action"])
        fig = px.histogram(labels_df, x="action")
        fig.write_image(str(ROOT_PATH / "agent/model/log/test_action_labels_hist.png"))
