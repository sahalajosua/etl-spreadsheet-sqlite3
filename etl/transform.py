"""
    author: sahalajosuasinaga@gmail.com
"""

import pandas as pd
import re
from . read import ConnectionGoogleSheet


class TransformData:

    def convert_to_dataframe(self):
        # Convert Google Sheet data to a DataFrame and transform it
        read_data = ConnectionGoogleSheet.get_google_sheet_data(self)
        
        if read_data is None or len(read_data) < 2:
            print("No data available to transform.")
            return None

        df = pd.DataFrame(read_data[1:], columns=read_data[0])

        # Transform DataFrame by standardizing columns
        df['id'] = df['id'].astype(str)
        df['name'] = df['name'].astype(str)
        df['phone_number'] = df['phone_number'].apply(self._standardize_phone_number)

        # Convert date string to datetime format
        df['born_day'] = df['born_day'].apply(self._standardize_date)
        df['born_day'] = df['born_day'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else None)

        print("Data transformation SUCCESS")
        return df

    def _standardize_phone_number(self, phone_number):
        # Standardize phone number to include country code
        return '62' + phone_number if not phone_number.startswith('62') else phone_number

    def _standardize_date(self, date_str):
        # Convert date string to datetime format, returning NaT on failure
        date_str = re.sub(r'/', '-', date_str)
        try:
            return pd.to_datetime(date_str, format='%Y-%m-%d')
        except ValueError:
            return pd.NaT