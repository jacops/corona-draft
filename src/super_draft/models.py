from typing import List
from . import utils


class PlayerMetadata:
    def __init__(self, comment: str = None, link: str = None):
        self.comment = comment
        self.link = link


class Player:
    def __init__(self, name: str, position: str, seasons: str, metadata: PlayerMetadata = PlayerMetadata):
        self.name = name
        self.position = position
        self.seasons = seasons
        self.metadata = metadata

    def to_array(self) -> list:
        return [
            self.position,
            self.name,
            self.seasons,
            self.metadata.comment,
            self.metadata.link
        ]


class Team:
    def __init__(self, name: str, players: list = None, metadata: dict = None):
        self.name = name
        self.players = players if players is not None else []
        self.metadata = metadata if metadata is not None else {}
        self.team_grid = None

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def get_players(self) -> List[Player]:
        return self.players

    def set_metadata(self, metadata: dict) -> None:
        self.metadata = metadata

    def get_grid(self):
        if self.team_grid is None:
            team_grid = {
                0: [],
                1: [],
                3: [],
                4: []
            }
            for player in self.players:
                player_line = utils.get_line_by_position(player.position)
                if player_line not in team_grid:
                    team_grid[player_line] = []

                team_grid[player_line].append(player)
                team_grid[player_line].sort(key=lambda x: utils.POSITIONS_ORDER[player_line].index(x.position))

            self.team_grid = dict(sorted(team_grid.items()))

        return self.team_grid


class Tournament:
    def __init__(self, name: str, metadata: dict = None):
        self.name = name
        self.metadata = metadata if metadata is not None else {}
        self.teams = list()

    def add_team(self, team: Team) -> None:
        self.teams.append(team)

    def get_teams(self) -> List[Team]:
        return self.teams

    def get_name(self):
        return self.name


def get_player_from_raw_data(raw_data: list) -> Player:
    return Player(
        raw_data[1], raw_data[0], raw_data[2],
        PlayerMetadata(utils.get_list_value(raw_data, 3), utils.get_list_value(raw_data, 4))
    )


def get_team_player_changes(team1: Team, team2: Team) -> list:
    changes = []
    for team1_player in team1.players:
        player_found = False
        for team2_player in team2.players:
            if team1_player.name == team2_player.name:
                player_found = True
                break
        if not player_found:
            changes.append(team1_player)

    return changes
