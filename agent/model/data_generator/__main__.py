import time

from agent.model.data_generator.generator import BattleSnakeDataGenerator
from agent.model.data_generator.scraper import BattleSnakeScraper

pruzze_url = "https://play.battlesnake.com/u/pruzze/pruzze-v2/"

scraper = BattleSnakeScraper()
pruzze_games = scraper.scrape_snake(pruzze_url)

generator = BattleSnakeDataGenerator()
train = generator.generate_data(pruzze_games)

file_name = time.strftime("%Y%m%d_%H%M%S") + "_battlesnake_train_size_" + str(len(train.transitions))

train.save(file_name)