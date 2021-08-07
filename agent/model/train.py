from agent.model.data_generator.dataset import BattleSnakeDataset

if __name__ == "__main__":
    dataset = BattleSnakeDataset.load("20210807_174043_battlesnake_train_size_6497")
    print(type(dataset))