from typing import List

from game.game import BattleSnakeGame


class BattleSnakeScraper:
    def __init__(self):
        pass

    def scrape(self, game_id: str) -> BattleSnakeGame:
        pass


    def scrape_snake(self, snake_url: str, num_games: int = 500) -> List[BattleSnakeGame]:
        """
        @param snake_url: URL of snake to scrape from. E.G: https://play.battlesnake.com/u/pruzze/pruzze-v2/
        @param num_games: Number of games to scrape from user
        """
        pass
