# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a spreadsheet
SPREADSHEET_ID = "19SUbSezEZ_ObEqfoNY3BDAM8z3cyBR-raql0Rs7_N3A"

# i.e. sheet name
RANGE_NAME = "current"

# Columns to publish, in output order. Selecting by name rather than dropping
# unwanted ones and slicing by position keeps the output stable when editors
# add, remove or reorder columns in the spreadsheet.
KEEP_COLUMN = [
    "LAST, First Name EN",
    "Chinese Name",
    "Email",
    "Home Institution",
    "Specialty",
    "Task",
    "Arrive/Depart",
    "Affiliation",
    "Photo",
]
