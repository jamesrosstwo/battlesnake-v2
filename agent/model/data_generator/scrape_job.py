import time

from apscheduler.schedulers.blocking import BlockingScheduler

from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.data_generator.scraper import BattleSnakeScraper


seen_games: set = {'00971a20-2096-425b-82f3-fb3e7c40d29c',
 '13a5333b-5bf6-47f6-ada4-76307af6a5db',
 '149d9473-a9e3-4da0-9c95-67a3c5102269',
 '2d0c3468-69de-4929-bc58-b562f0f4da46',
 '82b9d516-e73e-497a-87b8-d6d74ee4a34e',
 'a6342970-a0d2-47d2-854c-2adee8f89d62',
 'd83af161-4b4a-4c62-bcbf-72f538563d8a',
 'dccf195d-04b8-41f4-8dcb-87b28b8f446b',
 'e61b10cd-66c9-4971-b986-47f3b9b73fcc'}
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