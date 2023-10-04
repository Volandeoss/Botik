from pprint import pprint

from oauth2client.service_account import ServiceAccountCredentials
import apiclient

import httplib2
from config import SERVICE_ACC_INFO
from environs import Env

env = Env()
env.read_env()

# ID Google Sheets документа (можно взять из его URL)
# id до таблички буде також у венв (на всяк випадок)
spreadsheet_id = env.str("spreadsheet_id")

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    SERVICE_ACC_INFO,
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build("sheets", "v4", http=httpAuth)

# Пример чтения файла
values = (
    service.spreadsheets()
    .values()
    .get(spreadsheetId=spreadsheet_id, range="A1:E20", majorDimension="COLUMNS")
    .execute()
)
pprint(values)
