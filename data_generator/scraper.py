import re
import ssl
from typing import List

import requests
from bs4 import BeautifulSoup, SoupStrainer

from game.game import BattleSnakeGame
import websocket


class BattleSnakeScraper:
    def __init__(self):
        self._base_socket_url = "wss://engine.battlesnake.com/socket/"
        self._base_game_url = "https://engine.battlesnake.com/games/"

        self._req_headers = headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    def scrape(self, game_id: str) -> BattleSnakeGame:

        print(game_id)

        # Metadata
        response = requests.request("GET", self._base_game_url + game_id, headers=self._req_headers)
        print(response.text)


        # Turn data
        ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.connect(self._base_socket_url + game_id)
        while ws.connected:
            result = ws.recv()
            print("Received '%s'" % result)
        ws.close()


    def scrape_snake(self, snake_url: str, num_games: int = 500) -> List[BattleSnakeGame]:
        """
        @param snake_url: URL of snake to scrape from. E.G: https://play.battlesnake.com/u/pruzze/pruzze-v2/
        @param num_games: Number of games to scrape from user
        """



        req = requests.get(snake_url, self._req_headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        games = []
        snake_name = soup.find(".")

        for link in soup.findAll('a', attrs={'href': re.compile("/g/.+/")}):
            href = link.get("href")
            game_id = href[3:-1]
            games.append(self.scrape(game_id))

