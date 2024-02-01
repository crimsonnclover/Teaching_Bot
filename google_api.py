from gsheets import Sheets
from gsheets.models import WorkSheet


def get_sheet():
    sheets = Sheets.from_files('client_secrets.json', 'storage.json')
    url = "https://docs.google.com/spreadsheets/d/1IFJxFyDJL-T8bUvSFEvx4H-QhjwysR8dn-wiqzD437I"

    return sheets.get(url)


def get_next_row(worksheet, index):
    rows = worksheet.values()
    if len(rows) - 2 < index:
        return None
    return rows[index + 1]
