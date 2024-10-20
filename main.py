"""
    author: sahalajosuasinaga@gmail.com
"""

# relative import
from etl import ( 
    ConnectionGoogleSheet, TransformData, LoadData
)


if __name__ == '__main__':

    run_data = LoadData()
    run_data.load_data()