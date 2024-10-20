"""
    author: sahalajosuasinaga@gmail.com
"""

import gspread
import os
from dotenv import load_dotenv


class ConnectionGoogleSheet:

    def get_google_sheet_data(self):

        load_dotenv()

        API_KEY         = os.environ['api_key']
        SPREADSHEET_ID  = os.environ['spreadsheet_id']
        SHEET_NAME      = os.environ['sheet_name']
        CELL_BOX        = os.environ['cell_box']

        # Authentication using API
        gc = gspread.api_key(API_KEY)
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(SHEET_NAME)

        try:
            # Get data from worksheet
            data = worksheet.get(CELL_BOX)
            print("Get data from spreadsheet SUCCESS")
            return data
        
        except Exception as e:
            print(f"Get data from spreadsheet ERROR: {e}")
            return None