import torch
from tqdm import tqdm

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet
import torch.optim as optim
import torch.nn as nn

from definitions import TORCH_DEVICE, ROOT_PATH

if __name__ == "__main__":
    dataset: BattleSnakeDataset = BattleSnakeDataset.load("20210810_222929_pruzze_train_size_7442")
    # dataset.transitions = [x for x in dataset.transitions if x.action.argmax().item() in [0]]

    batch_size = 10
    num_epochs = 2
    batch_print_occurrence = 1000
    conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)

    train_test_split = 0.85
    train_test_idx = int(len(dataset.transitions) * train_test_split)

    train = dataset.transitions[:train_test_idx]
    test = dataset.transitions[train_test_idx:]

    criterion = nn.CrossEntropyLoss().to(TORCH_DEVICE)
    optimizer = optim.Adam(conv_net.parameters(), lr=0.01)
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

            outputs = conv_net(x)
            loss = criterion(outputs, y_class_idx)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if i % batch_print_occurrence == 0 and i > 0:
                batch_eval_loss = running_loss / batch_print_occurrence
                print('[%d, %5d] loss: %.5f' %
                      (epoch + 1, i + 1, batch_eval_loss))
                running_loss = 0.0


    correct_count, all_count = 0, 0
    for i in tqdm(range(len(test))[::batch_size][:-1]):
        batch_data = [list(train[j])[1:] for j in range(i, i + batch_size)]
        x, y = zip(*batch_data)
        x = torch.stack(x, dim=0)
        y = torch.stack(y, dim=0).float()
        y_class_idx = torch.max(y, 1)[1]

        with torch.no_grad():
            logps = conv_net(x)
        ps = torch.exp(logps)
        for i in range(len(ps)):
            if ps[i].argmax() == y_class_idx[i]:
                correct_count += 1
            all_count += 1

    print("Number Of States Tested =", all_count)
    print("\nModel Accuracy =", (correct_count / all_count))

    PATH = str(ROOT_PATH / 'agent/model/saved_models/pruzze.pth')
    torch.save(conv_net.state_dict(), PATH)
