from data_generator.generator import BattleSnakeDataGenerator
from data_generator.scraper import BattleSnakeScraper
from definitions import SETTINGS

pruzze_url = "https://play.battlesnake.com/u/pruzze/pruzze-v2/"

scraper = BattleSnakeScraper()
pruzze_games = scraper.scrape_snake(pruzze_url)

generator = BattleSnakeDataGenerator()
train = generator.generate_data(pruzze_games)

save_path = SETTINGS["data"]["path"]
train.save(save_path)