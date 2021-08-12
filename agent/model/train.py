import torch

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet


from definitions import TORCH_DEVICE, ROOT_PATH

if __name__ == "__main__":
    dataset: BattleSnakeDataset = BattleSnakeDataset.load_dir(ROOT_PATH / "data/pruzze")


    train_test_split = 0.8
    train_test_idx = int(len(dataset.transitions) * train_test_split)

    train = dataset.transitions[:train_test_idx]
    test = dataset.transitions[train_test_idx:]

    conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)
    # conv_net.load_model(ROOT_PATH / "agent/model/saved_models/pruzze_old.pth")

    conv_net.train_from_transitions(train, num_epochs=10)
    conv_net.evaluate_on_transitions(test)

    PATH = str(ROOT_PATH / 'agent/model/saved_models/pruzze_old.pth')
    torch.save(conv_net.state_dict(), PATH)
