import torch
from tqdm import tqdm

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet
import torch.optim as optim
import torch.nn as nn

from definitions import TORCH_DEVICE

if __name__ == "__main__":
    dataset: BattleSnakeDataset = BattleSnakeDataset.load("20210810_101122_battlesnake_train_size_6135")

    batch_size = 4
    num_epochs = 2
    conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)

    train_test_split = 0.7
    train_test_idx = int(len(dataset.transitions) * train_test_split)

    train = dataset.transitions[:train_test_idx]
    test = dataset.transitions[train_test_idx:]

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(conv_net.parameters(), lr=0.03, momentum=0.9)

    for epoch in range(num_epochs):
        print("Epoch", epoch)
        running_loss = 0.0
        # Iterate through data points while ensuring we don't access out of bounds
        for i in tqdm(range(len(train))[::batch_size][:-1]):
            batch_data = [list(train[j])[1:] for j in range(i, i + batch_size)]
            x, y = zip(*batch_data)
            x = torch.stack(x, dim=0)
            y = torch.stack(y, dim=0).float()
            y_class_idx = torch.max(y, 1)[1]
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = conv_net(x)
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            # print statistics
            running_loss += loss.item()
            if i % (100 // batch_size) == 0 and i > 0:  # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0
