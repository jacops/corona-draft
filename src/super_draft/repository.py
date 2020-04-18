import os
import yaml
from .models import Team
from .models import Tournament
from .models import get_player_from_raw_data


class YamlRepository:
    def __init__(self, data_file: str):
        self.data_file = data_file
        if not os.path.exists(data_file):
            with open(self.data_file, 'w') as file:
                yaml.dump({"tournaments": []}, file)

    def get_tournament(self) -> Tournament:
        with open(self.data_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        if len(data["tournaments"]) == 0:
            raise Exception("Tournament hasn't started yet.")

        tournament_data = data["tournaments"][0]
        tournament = Tournament(tournament_data["name"], tournament_data["metadata"])

        for team_data in tournament_data["teams"]:

            tournament.add_team(Team(team_data["name"], list(map(
                lambda x: get_player_from_raw_data(x),
                team_data["players"])
            ), team_data["metadata"]))


        return tournament

    def is_tournament_started(self, name: str) -> bool:
        with open(self.data_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        for tournament in data["tournaments"]:
            if tournament["name"] == name:
                return True
        return False

    def save_tournament(self, tournament: Tournament) -> None:
        """Only one tournament can be managed at this time"""

        tournament_dict = {
            "name": tournament.name,
            "metadata": tournament.metadata,
            "teams": list(map(lambda x: {
                "name": x.name,
                "players": list(map(lambda y: y.to_array(), x.players)),
                "metadata": x.metadata
            }, tournament.teams))
        }

        with open(self.data_file, 'w') as file:
            yaml.dump({"tournaments": [tournament_dict]}, file)

    def get_team(self, name: str) -> Team:
        with open(self.data_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        for team_data in data["tournaments"][0]["teams"]:
            if team_data["name"] == name:
                return Team(name, list(map(
                    lambda x: get_player_from_raw_data(x),
                    team_data["players"])
                ))

        raise Exception("Team not found")


class SpreadsheetRepository:
    def __init__(self, api, spreadsheet_id: str):
        self.api = api
        self.spreadsheet_id = spreadsheet_id

    def get_tournament_metadata(self) -> dict:
        sheet_metadata = self.api.get(
            spreadsheetId=self.spreadsheet_id
        ).execute()

        for sheet in sheet_metadata.get('sheets', ''):
            team_name = sheet.get("properties", {}).get("title", "Unknown Team")
            players_rows = self.api.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=team_name + "!A2:D"
            ).execute().get('values', [])

        return {
            "name": sheet_metadata["properties"]["title"],
            "teams": list(map(
                lambda x: x.get("properties", {}).get("title", "Sheet1"),
                sheet_metadata.get('sheets', '')
            ))
        }

    def get_team(self, name) -> Team:
        players_rows = self.api.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=name + "!A2:D"
        ).execute().get('values', [])

        return Team(name, list(map(
            lambda x: get_player_from_raw_data(x),
            players_rows)
        ), {})
