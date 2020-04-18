import os
from . import config
from . import models
from .models import Tournament
from .repository import YamlRepository
from .repository import SpreadsheetRepository
from .lineup_generator import generate_lineup


def start_tournament() -> None:
    yaml_repository = YamlRepository(config.get_data_source_yaml_file())
    spreadsheet_repository = SpreadsheetRepository(config.get_spreadsheet_api(), config.get_spreadsheet_id())

    tournament_metadata = spreadsheet_repository.get_tournament_metadata()

    if yaml_repository.is_tournament_started(tournament_metadata["name"]):
        print("Tournament already started")
        return

    message = "Wystartował turniej o nazwie \"{0}\"\nBiorą w nim udział następujące drużyny:\n{1}".format(
        tournament_metadata["name"],
        "\n".join(list(map(lambda x: " - " + x, tournament_metadata["teams"])))
    )

    tweet_id = config.get_twitter_api().PostUpdate(status=message).id_str
    tournament = Tournament(tournament_metadata["name"], {"tweet_id": tweet_id})

    for team_name in tournament_metadata["teams"]:
        tournament.add_team(spreadsheet_repository.get_team(team_name))

    yaml_repository.save_tournament(tournament)


def fetch_changes() -> None:
    yaml_repository = YamlRepository(config.get_data_source_yaml_file())
    spreadsheet_repository = SpreadsheetRepository(config.get_spreadsheet_api(), config.get_spreadsheet_id())

    tournament = yaml_repository.get_tournament()

    for team in tournament.teams:
        fresh_team = spreadsheet_repository.get_team(team.name)
        team_changes = models.get_team_player_changes(fresh_team, team)
        for new_player in team_changes:
            team.add_player(new_player)

        team_data_dir = os.getcwd() + "/data/" + team.name
        os.makedirs(team_data_dir, exist_ok=True)
        lineup_image = generate_lineup(team, team_data_dir)

        if len(team_changes) > 0:
            player_string = []
            for change in team_changes:
                player_string.append(" - {0} z sezonów {1}".format(change.name, change.seasons))
            message = "Drużyna {0} wydraftowała:\n{1}".format(team.name, "\n".join(player_string))

            if "tweet_id" in team.metadata:
                parent_tweet = team.metadata["tweet_id"]
            else:
                parent_tweet = tournament.metadata["tweet_id"]

            tweet = config.get_twitter_api().PostUpdate(
                status=message,
                media=lineup_image,
                in_reply_to_status_id=parent_tweet
            )

            team.metadata["tweet_id"] = tweet.id_str

    yaml_repository.save_tournament(tournament)
