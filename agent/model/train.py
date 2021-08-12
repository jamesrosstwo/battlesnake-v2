import torch

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet


from definitions import TORCH_DEVICE, ROOT_PATH

if __name__ == "__main__":
    dataset: BattleSnakeDataset = BattleSnakeDataset.load("20210812_045331_pruzze_train_size_5559")


    train_test_split = 0.2
    train_test_idx = int(len(dataset.transitions) * train_test_split)

    test = dataset.transitions[:train_test_idx]
    train = dataset.transitions[train_test_idx:]

    conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)
    conv_net.load_model(ROOT_PATH / "agent/model/saved_models/pruzze.pth")

    # conv_net.train_from_transitions(train, num_epochs=10)
    conv_net.evaluate_on_transitions(test)

    PATH = str(ROOT_PATH / 'agent/model/saved_models/pruzze.pth')
    torch.save(conv_net.state_dict(), PATH)
