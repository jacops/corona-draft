#!/usr/bin/env python

import os
from super_draft.utils import get_authenticated_service
from super_draft.tournament import Tournament
import twitter


def main():
    if os.path.exists('data/master-tweet.txt'):
        return

    service = get_authenticated_service(os.getcwd() + "/token.pickle")
    tournament = Tournament(service, os.environ["SPREADSHEET_ID"])

    twitter_api = twitter.Api(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )

    message = "Wystartował turniej \"{0}\"!\nBiorą w nim następujące drużyny:\n{1}".format(
        os.environ["TOURNAMENT_NAME"],
        "\n".join(list(map(lambda x: " - " + x.name, tournament.get_teams())))
    )

    with open('data/master-tweet.txt', "w") as f:
        tweet_id = twitter_api.PostUpdate(status=message).id_str
        f.write(tweet_id)



if __name__ == '__main__':
    main()
