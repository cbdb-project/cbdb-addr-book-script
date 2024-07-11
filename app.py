import requests
from flask import Flask, jsonify, render_template
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a spreadsheet
SPREADSHEET_ID = "19SUbSezEZ_ObEqfoNY3BDAM8z3cyBR-raql0Rs7_N3A"
# can be sheet name
RANGE_NAME = "current"


# Read data from Google Sheets directly:
# Credentials and authentication from Google sheet API
# Error: Cannot get all of the data same with the Google sheet
def read_google_sheet():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            print("token installed")
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        # values: list of list/row
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
    except HttpError as err:
        print(err)


# Download the Google sheet data and process locally
def download_google_sheet(spreadsheet_id, out_file):
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
    response = requests.get(url)
    if response.status_code == 200:
        with open(out_file, 'wb') as f:
            f.write(response.content)
            print('CSV file saved to: {}'.format(out_file))
        df = pd.read_csv(out_file)
        return df
    else:
        print(f'Error downloading Google Sheet: {response.status_code}')
        return


@app.route('/')
def index():
    # df = read_google_sheet()
    df = download_google_sheet(SPREADSHEET_ID, "copy.csv")
    return render_template('index.html', tables=[df.to_html(classes='data', header=True, index=False)])
    # return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    # read_google_sheet()

    # test read in .csv from local
    # df = pd.read_csv("cbdb_addr_book - current.csv")
    # for index, row in df.iterrows():
    #     print(len(row))



