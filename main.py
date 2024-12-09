import os
import uvicorn
import httpx
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from typing import List

# Environnement
load_dotenv()

AIRTABLE_API_TOKEN = os.getenv("AIRTABLE_API_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/'

# En-têtes pour authentification
HEADERS = {
    'Authorization': f'Bearer {AIRTABLE_API_TOKEN}',
    'Content-Type': 'application/json',
}

app = FastAPI()


@app.get('/')
def read():
    return {"message": "Bienvenue bro !"}

####salesPipeline route
#getAllsalesPipeline (Récupérer la liste des commandes )
@app.get('/getAllsalesPipeline')
async def getAllsalesPipeline():
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.get(AIRTABLE_URL+'sales_pipeline',headers=HEADERS)
            response.raise_for_status()
            data= response.json()
            return JSONResponse(
                    content=data         
             )
        except  httpx.HTTPStatusError as e: 
            return JSONResponse(
                status_code=response.status_code,
                content={"message":f"Erreur http :{e}"}
           )

#getAllSalesPipelineById(Récupérer des commandes en fonction de l'ID d'une commande)
@app.get('/getAllsalesPipelineById/{id}')
async def getAllsalesPipelineById(id:str):
    async with httpx.AsyncClient() as http_client:
        try:

            response = await http_client.get(f"{AIRTABLE_URL}sales_pipeline/{id}", headers=HEADERS)
            response.raise_for_status()
            allProductsData = response.json()   
            return JSONResponse(
                status_code=response.status_code,
                content=allProductsData
            )
        except  httpx.HTTPStatusError as e: 
            return JSONResponse(
                status_code=response.status_code,
                content={"message":f"Erreur http :{e}"}
            )

#####products route
#getAll
@app.get('/getAllProducts')
async def getAllProducts():
    async with httpx.AsyncClient() as http_client:
        try:
            response =  await  http_client.get(AIRTABLE_URL+'products',headers=HEADERS)
            response.raise_for_status()
            allProductsData = response.json()   
            allProducts = allProductsData["records"]
            return JSONResponse(
                status_code=response.status_code,
                content=allProducts
            )
        except  httpx.HTTPStatusError as e: 
            return JSONResponse(
                status_code=response.status_code,
                content={"message":f"Erreur http :{e}"}
            )
#find product by id
@app.get('/getAllProductsById/{id}')
async def getAllProductsById(id:str):
    async with httpx.AsyncClient() as http_client:
        try:

            response = await http_client.get(f"{AIRTABLE_URL}products/{id}", headers=HEADERS)
            response.raise_for_status()
            allProductsData = response.json()   
            return JSONResponse(
                status_code=response.status_code,
                content=allProductsData
            )
        except  httpx.HTTPStatusError as e: 
            return JSONResponse(
                status_code=response.status_code,
                content={"message":f"Erreur http :{e}"}
            )



        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
