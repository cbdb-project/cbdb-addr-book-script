from flask import Flask, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)

# Google Sheets credentials and configuration
SCOPE = ['https://docs.google.com/spreadsheets/d/19SUbSezEZ_ObEqfoNY3BDAM8z3cyBR-raql0Rs7_N3A/edit?gid=0#gid=0',
         'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPE)


# Read data from Google Sheets
def read_google_sheet():
    client = gspread.authorize(CREDS)
    sheet = client.open('Your Google Sheet Name').sheet1  # Open the first sheet
    data = sheet.get_all_records()  # Get all records as a list of dictionaries
    return pd.DataFrame(data)  # Convert to pandas DataFrame


@app.route('/api/table')
def get_table():
    df = read_google_sheet()
    data = df.to_dict(orient='records')
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
