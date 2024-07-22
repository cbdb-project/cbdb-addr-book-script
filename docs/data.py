import json
import math

from utils import download_google_sheet
from config import SPREADSHEET_ID


def prepare_data():
    processed_data = []
    df = download_google_sheet(SPREADSHEET_ID, "copy.xlsx")
    data = df.to_dict(orient='records')

    for record in data:
        # skip the empty lines between in boston and not in boston
        if isinstance(record.get("Preferred First Name"), float) and math.isnan(record.get("Preferred First Name")):
            continue
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = ""
            if key == "Cell":
                if math.isnan(value):
                    record[key] = ""
                else:
                    record[key] = int(value)
            elif key == "Arrive/Depart":
                if isinstance(value, float) and math.isnan(value):
                    record[key] = ""
                else:
                    record[key] = str(value)
        processed_data.append(record)
    with open('data.json', 'w') as f:
        json.dump(processed_data, f)


if __name__ == "__main__":
    prepare_data()
