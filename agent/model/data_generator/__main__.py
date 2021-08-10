import time

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.data_generator.scraper import BattleSnakeScraper


def scrape_pruzze():
    pruzze_url = "https://play.battlesnake.com/u/pruzze/pruzze-v2/"

    scraper = BattleSnakeScraper()
    pruzze_games = scraper.scrape_snake(pruzze_url)

    dataset = BattleSnakeDataset.from_games(pruzze_games)

    file_name = time.strftime("%Y%m%d_%H%M%S") + "_battlesnake_train_size_" + str(len(dataset.transitions))

    dataset.save(file_name)
