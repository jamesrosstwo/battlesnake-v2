import numpy as np

from agent.model.data_generator.dataset import BattleSnakeDataset
from definitions import ROOT_PATH

save_pth = str(ROOT_PATH / "state_tensors/state_img_0.png.npy")
ndarr = np.load(ROOT_PATH)

new_transitions = BattleSnakeDataset.load("single_game_test").transitions

print("yes")