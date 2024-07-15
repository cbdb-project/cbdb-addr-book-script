from flask import Flask, render_template

from utils import download_google_sheet
from config import SPREADSHEET_ID

app = Flask(__name__)


@app.route('/')
def index():
    df = download_google_sheet(SPREADSHEET_ID, "copy.xlsx")
    data = df.to_dict(orient='records')
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
    # read_google_sheet_by_api()
    # df = download_google_sheet(SPREADSHEET_ID, "copy.xlsx")
    # print(df.head())
    # print(extract_images_from_excel("copy.xlsx"))
