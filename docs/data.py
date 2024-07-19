import json
import math

from utils import download_google_sheet
from config import SPREADSHEET_ID


def prepare_data():
    df = download_google_sheet(SPREADSHEET_ID, "copy.xlsx")
    data = df.to_dict(orient='records')
    for record in data:
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = ""
            if key == "Cell":
                if math.isnan(value):
                    record[key] = ""
                else:
                    record[key] = int(value)
            elif key == "Arrive/Depart":
                record[key] = str(value)
    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    prepare_data()
