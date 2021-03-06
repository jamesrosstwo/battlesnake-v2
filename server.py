import os
import random

import cherrypy

from agent.action import BattleSnakeAction
from agent.agent import BattleSnakeAgent
from agent.model.data_generator.dataset import BattleSnakeDataset
from agent.model.model import BattleSnakeConvNet
from definitions import ROOT_PATH, TORCH_DEVICE

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake:

    def __init__(self):
        self.conv_net = BattleSnakeConvNet().to(TORCH_DEVICE)
        self.conv_net.load_model(ROOT_PATH / "agent/model/saved_models/pruzze.pth")
        # dataset: BattleSnakeDataset = BattleSnakeDataset.load_dir(ROOT_PATH / "data/pruzze")
        # self.conv_net.train_from_transitions(dataset.transitions)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        rbc_blue = "#0059b4"
        color = rbc_blue
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data_generator
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": color,  # TODO: Personalize
            "head": "shades",  # TODO: Personalize
            "tail": "sharp",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        agent = BattleSnakeAgent(self.conv_net)
        selected_action = agent.act(data)
        selected_move = BattleSnakeAction.parse_action(selected_action)

        print(f"MOVE: {selected_move}")
        return {"move": selected_move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
