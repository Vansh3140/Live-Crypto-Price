import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from gspread_formatting import format_cell_ranges, cellFormat, TextFormat
import logging
import os
from dotenv import load_dotenv
import json

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Set up the necessary credentials and API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = json.loads(os.getenv("CREDS_FILE"))

SPREADSHEET_NAME = "Live Crypto"


def update_google_sheet(df):
    """Update Google Sheets with cryptocurrency data."""
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDS_FILE, SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open(SPREADSHEET_NAME).sheet1

    # Clear the sheet
    sheet.clear()

    # Add headers
    headers = [
        "Cryptocurrency Name",
        "Symbol",
        "Current Price (USD)",
        "Market Capitalization (USD)",
        "24h Trading Volume (USD)",
        "Price Change (24h %)"
    ]
    sheet.append_row(headers)

    # Format headers to be bold
    header_range = 'A1:F1'  # assuming the headers are in the first row
    bold_format = cellFormat(textFormat=TextFormat(bold=True))  # Set bold text
    format_cell_ranges(sheet, [(header_range, bold_format)])

    # Convert DataFrame to list of lists and add data
    rows = df[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]].values.tolist()
    for row in rows:
        sheet.append_row(row)
