import os
from fastapi import FastAPI
from dotenv import load_dotenv


# Environnement
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = os.getenv("TABLE_NAME")
AIRTABLE_URL = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}'

app = FastAPI()


@app.get('/')
def read():
        return  {"message": "Bienvenue bro !"}

