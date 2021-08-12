import time

from apscheduler.schedulers.blocking import BlockingScheduler

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.data_generator.scraper import BattleSnakeScraper


seen_games: set = {}
def scrape_pruzze():
    pruzze_url = "https://play.battlesnake.com/u/pruzze/pruzze-v2/"

    scraper = BattleSnakeScraper()
    pruzze_games = scraper.scrape_snake(pruzze_url)


    new_games = []
    for game in pruzze_games:
        if game.metadata.id in seen_games:
            continue
        new_games.append(game)
        seen_games.add(game.metadata.id)

    if len(new_games) == 0:
        return

    print("found new games:", [game.metadata.id for game in new_games])

    dataset = BattleSnakeDataset.from_games(new_games)

    file_name = time.strftime("%Y%m%d_%H%M%S") + "_pruzze_train_size_" + str(len(dataset.transitions))

    dataset.save(file_name)

scrape_pruzze()
scheduler = BlockingScheduler()
scheduler.add_job(scrape_pruzze, 'interval', hours=0.15)
scheduler.start()