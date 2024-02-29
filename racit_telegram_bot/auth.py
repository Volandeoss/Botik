from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from environs import Env

env = Env()
env.read_env()


def spreadsheet_auth():
    flow = InstalledAppFlow.from_client_config(
        {
            "web": {
                "client_id": env.str("auth_client_id"),
                "project_id": env.str("project_id"),
                "auth_uri": env.str("auth_uri"),
                "token_uri": env.str("token_uri"),
                "auth_provider_x509_cert_url": env.str("auth_provider_x509_cert_url"),
                "client_secret": env.str("client_secret"),
                "redirect_uris": [
                    env.str("redirect_uri"),
                ],
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    flow.run_local_server()

    credentials = flow.credentials

    spreadsheet_id = env.str("spreadsheet_id")

    service = build("sheets", "v4", credentials=credentials)

    # Optionally, view the email address of the authenticated user.
    user_info_service = build("oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    print(user_info)

    try:
        values = (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id, range="A10:G21", majorDimension="COLUMNS"
            )
            .execute()
        )
    except HttpError as e:
        if e.resp.status:
            return e.resp.status
        else:
            return 0
    return str(values)
