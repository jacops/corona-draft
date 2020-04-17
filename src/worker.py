#!/usr/bin/env python

import os
from super_draft.utils import get_authenticated_service
from super_draft.tournament import Tournament
import twitter

def main():
    service = get_authenticated_service(os.getcwd() + "/token.pickle")
    tournament = Tournament(service, os.environ["SPREADSHEET_ID"])

    teams = tournament.get_teams()
    twitter_api = twitter.Api(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )

    for team in teams:
        team.render_grid()
        team.announce(twitter_api)
        team.save()


if __name__ == '__main__':
    main()
