from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet

if __name__ == "__main__":
    dataset: BattleSnakeDataset = BattleSnakeDataset.load("20210807_184653_battlesnake_train_size_6202")

    batch_size = 4
    net = BattleSnakeConvNet(dataset.metadata)
    print(net)
