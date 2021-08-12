import numpy as np
import torch

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.data_generator.scraper import BattleSnakeScraper
from agent.model.model import BattleSnakeConvNet
from definitions import ROOT_PATH, TORCH_DEVICE

save_pth = str(ROOT_PATH / "state_tensors/state_img_0.npy")
ndarr = np.load(save_pth)

new_transitions = BattleSnakeDataset.load("single_game_test").transitions
loaded_state = new_transitions[0].prev_state.cpu().numpy()
conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)
conv_net.load_model(ROOT_PATH / "agent/model/saved_models/pruzze.pth")


torch_test_state = conv_net(torch.from_numpy(ndarr).unsqueeze(0).to(TORCH_DEVICE))
with torch.no_grad():
    print(torch_test_state)

torch_test_state_np = torch_test_state.cpu().numpy()

scraper = BattleSnakeScraper()
scraped_game = scraper.scrape_game("a86180cb-3bb8-47c1-b029-865a13f80172", "Prüzze v2")
dtst = BattleSnakeDataset.from_games([scraped_game])
conv_net.evaluate_on_transitions(dtst.transitions)

game_test_state_np = dtst.transitions[1].prev_state.unsqueeze(0).numpy()