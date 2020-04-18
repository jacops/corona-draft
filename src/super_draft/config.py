import os
import twitter
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def get_twitter_api() -> twitter.Api:
    return twitter.Api(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )


def get_spreadsheet_api():
    credentials = None
    pickle_path = os.getcwd() + "/token.pickle"

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        with open(pickle_path, 'wb') as token:
            pickle.dump(credentials, token)

    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()


def get_spreadsheet_id() -> str:
    return os.environ["SPREADSHEET_ID"]


def get_data_source_yaml_file() -> str:
    return os.environ["DATA_SOURCE_YAML_FILE"]


def get_rules() ->str:
    with open(os.environ["RULES_FILE"]) as f:
        return f.read()
