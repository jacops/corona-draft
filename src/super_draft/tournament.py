from googleapiclient.discovery import Resource
from .team import Team

IGNORED_SHEETS = ["Zasady", "Pozycje"]


class Tournament:
    def __init__(self, service: Resource, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.spreadsheets = service.spreadsheets()

    def get_teams(self):
        sheet_metadata = self.spreadsheets.get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        teams = []

        for sheet in sheets:
            sheet_name = sheet.get("properties", {}).get("title", "Sheet1")
            if sheet_name in IGNORED_SHEETS:
                continue
            result = self.spreadsheets.values().get(spreadsheetId=self.spreadsheet_id,
                                                    range=sheet_name + "!A2:D").execute()
            teams.append(Team(sheet_name, result.get('values', [])))

        return teams
