import torch

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet


from definitions import TORCH_DEVICE, ROOT_PATH

if __name__ == "__main__":
    dataset: BattleSnakeDataset = BattleSnakeDataset.load("20210811_202004_pruzze_train_size_6303")


    train_test_split = 0.7
    train_test_idx = int(len(dataset.transitions) * train_test_split)

    train = dataset.transitions[:train_test_idx]
    test = dataset.transitions[train_test_idx:]

    conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)
    conv_net.train_from_transitions(train, num_epochs=1)
    conv_net.evaluate_on_transitions(test)

    PATH = str(ROOT_PATH / 'agent/model/saved_models/pruzze.pth')
    torch.save(conv_net.state_dict(), PATH)
