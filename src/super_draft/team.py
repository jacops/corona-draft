import csv

import os
from .lineup_generator import LineUpGenerator

POSITIONS_ORDER = [
    ["LW", "LF", "FW", "ST", "CF", "RF", "RW"],
    ["LM", "MF", "AM", "CM", "RM"],
    ["LWB", "DM", "RWB"],
    ["LB", "CBL", "CB", "SW", "CBR", "RB"],
    ["GK"]
]


def get_line_by_position(position: str) -> int:
    for line_number, line in enumerate(POSITIONS_ORDER):
        for line_position in line:
            if line_position == position:
                return line_number
    return -1


class Team:
    def __init__(self, name, data):
        self.name = name
        self.data = sorted(data, key=lambda r: r[1])
        self.team_grid = None
        os.makedirs(self.get_data_path(), exist_ok = True)

    def get_data_path(self) -> str:
        return os.getcwd() + "/data/" + self.name

    def save(self) -> None:
        writer = csv.writer(open(self.get_data_path() + '/data.csv', 'w'))
        for row in self.data:
            writer.writerow(row)

    def get_last_team_data(self) -> list:
        if os.path.exists(self.get_data_path() + '/data.csv'):
            with open(self.get_data_path() + '/data.csv', 'rt') as f:
                return list(csv.reader(f))
        return []

    def get_team_changes(self):
        last_team_data = self.get_last_team_data()
        return list(set(map(tuple, self.data)).symmetric_difference(set(map(tuple, last_team_data))))

    def get_team_grid(self):
        if self.team_grid is None:
            team_grid = {
                0: [],
                1: [],
                3: [],
                4: []
            }
            for player in self.data:
                player_line = get_line_by_position(player[0])
                if player_line not in team_grid:
                    team_grid[player_line] = []

                team_grid[player_line].append(player)
                team_grid[player_line].sort(key=lambda x: POSITIONS_ORDER[player_line].index(x[0]))

            self.team_grid = dict(sorted(team_grid.items()))

        return self.team_grid

    def render_grid(self) -> None:
        generator = LineUpGenerator(self.name, self.get_team_grid())
        generator.generate(self.get_data_path())

    def get_lineup_image(self) -> str:
        return self.get_data_path() + "/lineup.png"

    def get_parent_tweet(self):
        if os.path.exists(self.get_data_path() + '/last-tweet.txt'):
            with open(self.get_data_path() + '/last-tweet.txt') as f:
                return f.read()

        with open(os.getcwd() + "/data/master-tweet.txt") as f:
            return f.read()

    def announce(self, tweeter_api):
        player_string = []
        for change in self.get_team_changes():
            player_string.append(" - {0} z sezonów {1}".format(change[1], change[2]))
        message = "Drużyna {0} wydraftowała:\n{1}".format(self.name, "\n".join(player_string))

        tweet = tweeter_api.PostUpdate(
            status = message,
            media=self.get_lineup_image(),
            in_reply_to_status_id=self.get_parent_tweet()
        )

        with open(self.get_data_path() + '/last-tweet.txt', 'w') as f:
            return f.write(tweet.id_str)

