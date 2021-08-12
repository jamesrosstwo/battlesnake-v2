import random
from dataclasses import dataclass
from typing import List
import pickle

from agent.model.data_generator.transition import BattleSnakeTransition
from definitions import SETTINGS, ROOT_PATH
from game.game import BattleSnakeGame
from game.state import _display_state_tensor


def _save_path_from_name(filename):
    return str(ROOT_PATH / SETTINGS["data"]["path"] / filename) + ".pickle"


@dataclass
class BattleSnakeDataset:
    width: int
    height: int
    transitions: List[BattleSnakeTransition]
    game_ids: List[str]


    def shuffle(self):
        random.shuffle(self.transitions)

    def save(self, filename):
        save_path = _save_path_from_name(filename)
        pickle.dump(self, open(save_path, "wb"))

    @classmethod
    def load(cls, filename):
        save_path = _save_path_from_name(filename)
        obj = pickle.load(open(save_path, "rb"))
        # obj.shuffle()
        return obj

    @classmethod
    def load_direct(cls, file_path):
        obj = pickle.load(open(file_path, "rb"))
        # obj.shuffle()
        # t: BattleSnakeTransition = obj.transitions[0]
        # _display_state_tensor(t.prev_state)
        # _display_state_tensor(t.next_state)
        return obj

    @classmethod
    def load_dir(cls, dir_path):
        datasets: List[BattleSnakeDataset] = []

        for x in dir_path.iterdir():
            if x.is_file():
                datasets.append(pickle.load(open(str(x), "rb")))

        assert (len(datasets) > 0)
        w = datasets[0].width
        h = datasets[0].height
        out_transitions: List[BattleSnakeTransition] = []
        out_game_ids: List[str] = []
        for d in datasets:
            out_transitions.extend(d.transitions)
            out_game_ids.extend(d.game_ids)

        obj = cls(w, h, out_transitions, out_game_ids)
        # obj.shuffle()
        return obj

    @classmethod
    def from_games(cls, games: List[BattleSnakeGame]):
        assert (len(games) > 0)
        out_transitions: List[BattleSnakeTransition] = games[0].transitions
        width = games[0].metadata.width
        height = games[0].metadata.height
        game_ids = [x.metadata.id for x in games]
        raw_games = [games[0].raw_json]
        for game in games[1:]:
            out_transitions.extend(game.transitions)
            raw_games.append(game.raw_json)
            assert (game.metadata.width == width)
            assert (game.metadata.height == height)
        obj = cls(width, height, out_transitions, game_ids)
        # obj.shuffle()
        return raw_games, obj
