from dataclasses import dataclass
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import boto3
import os
from urllib.error import ContentTooShortError
import urllib.request
import json




@dataclass
class DataHandler():
    s3_client = boto3.client('s3')
    try:
        path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dbdetailss.json')
        with open(path_to_json) as json_file:
            data = json.load(json_file)
            for d in data['db_details']:
                _DATABASE_TYPE = d["type"]
                _DBAPI = d["dbapi"]
                _ENDPOINT = d["endpoint"]
                _USER = d["user"]
                _PASSWORD = d["password"]
                _DATABASE = d["database"]
                _PORT = d["port"]
    
    except FileNotFoundError:
        print("please upload database server details in json file, which can be found in the module found at: ", os.getcwd())

    def store_as_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv('watch_data/mens_watches.csv', index=False)

    def store_data_online(self, data):
        df = pd.DataFrame(data)
        try:
            engine = create_engine(f"{self._DATABASE_TYPE}+{self._DBAPI}://{self._USER}:{self._PASSWORD}@{self._ENDPOINT}:{self._PORT}/{self._DATABASE}")
            df.to_sql('mens_watches', engine, if_exists='replace', index=False)
        except AttributeError:
            print("DB engine not connected...")

    def download_images(self, src: str, i: int) -> None:

        if not os.path.exists('watch_data/images'):
            os.makedirs('watch_data/images')

        try:
            urllib.request.urlretrieve(src, f"watch_data/images/watch_image_{i}.jpg")
        except TypeError:
            pass
        except ContentTooShortError:
            pass

    def cloud_Store(self, src, i):
        self.s3_client.upload_file(f'watch_data/images/watch_image_{i}.png', 'aicore-new-bucket', f'watch_data/images/watch_image_{i}.png')