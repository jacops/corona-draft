import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def generate_token_pickle(credentials_path: str, token_pickle_path: str) -> None:
    print(credentials_path)
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, SCOPES)
    credentials = flow.run_local_server(port=0)
    with open(token_pickle_path, 'wb') as token:
        pickle.dump(credentials, token)


def get_authenticated_service(pickle_path: str):
    credentials = None

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        with open(pickle_path, 'wb') as token:
            pickle.dump(credentials, token)

    return build('sheets', 'v4', credentials=credentials)
