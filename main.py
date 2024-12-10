import os
import uvicorn
import httpx
import pprint
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from typing import List
from typing import Dict
from fastapi import FastAPI, HTTPException, Query

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
            response = await http_client.get(f"{AIRTABLE_URL}sales_pipeline",headers=HEADERS)
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
#find product by id product
@app.get('/getProductById/{id}')
async def getProductById(id:str):
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
##products KPIs

#getAllProductsKpis
@app.get('/getAllProductsKpis/')
async def getAllProductsKpis():
    async with httpx.AsyncClient() as http_client:
        try:
            # Requête à l'API Airtable
            response = await http_client.get(f"{AIRTABLE_URL}sales_pipeline", headers=HEADERS)
            response.raise_for_status()

            # Récupérer les données JSON
            data = response.json()
            records = data.get("records", [])

            if not records:
                return JSONResponse(
                    status_code=200,
                    content={"message": "Aucun enregistrement trouvé."}
                )

            # Initialiser les métriques
            total_products = len(records)
            total_revenue = 0
            products_per_sector = {}
            total_sales_per_agent = {}  # Pour compter les ventes par agent
            total_revenue_per_agent = {}  # Pour calculer le revenu par agent
            total_sales_per_manager = {}  # Pour compter les ventes par manager
            total_revenue_per_manager = {}  # Pour calculer le revenu par manager
            highest_revenue_agent = None  # Agent générant le plus de revenu
            max_revenue_agent = 0
            total_sales = 0  # Compteur des ventes totales
            total_won_sales = 0  # Compteur des ventes "Won"
            total_engaging_sales = 0  # Compteur des ventes "Engaging"
            total_lost_sales = 0  # Compteur des ventes "Lost"
            total_prospecting_sales = 0  # Compteur des ventes "Prospecting"
            total_won_revenue = 0  # Revenu total des ventes "Won"
            total_engaging_revenue = 0  # Revenu total des ventes "Engaging"
            total_lost_revenue = 0  # Revenu total des ventes "Lost"
            total_prospecting_revenue = 0  # Revenu total des ventes "Prospecting"
            total_sales_per_office_location = {}  # Pour compter les ventes par office_location
            total_revenue_per_office_location = {}  # Pour calculer le revenu total par office_location
            total_revenue_per_sector = {}  # Initialisation de total_revenue_per_sector

            # Calcul des métriques
            for record in records:
                fields = record.get("fields", {})

                # Extraire et valider le revenu
                revenue = fields.get("revenue (from account)", 0)
                if isinstance(revenue, list):
                    revenue = revenue[0] if len(revenue) > 0 else 0
                try:
                    revenue = float(revenue)
                except (ValueError, TypeError):
                    revenue = 0

                # Ajouter au revenu total
                total_revenue += revenue

                # Extraire et valider le secteur (convertir les listes en chaînes de caractères)
                sector = fields.get("sector (from account)", "Unknown")
                if isinstance(sector, list):
                    sector = ", ".join(sector) if len(sector) > 0 else "Unknown"

                # Comptabiliser les produits par secteur
                if sector not in products_per_sector:
                    products_per_sector[sector] = 0
                products_per_sector[sector] += 1

                # Calcul du revenu total par secteur
                if sector not in total_revenue_per_sector:
                    total_revenue_per_sector[sector] = 0
                total_revenue_per_sector[sector] += revenue

                # Comptabiliser les ventes par agent
                sales_agent = fields.get("sales_agent", "Unknown")
                if isinstance(sales_agent, list):
                    sales_agent = ", ".join(sales_agent) if len(sales_agent) > 0 else "Unknown"

                if sales_agent not in total_sales_per_agent:
                    total_sales_per_agent[sales_agent] = 0
                    total_revenue_per_agent[sales_agent] = 0
                total_sales_per_agent[sales_agent] += 1
                total_revenue_per_agent[sales_agent] += revenue

                # Identifier l'agent avec le plus grand revenu
                if revenue > max_revenue_agent:
                    max_revenue_agent = revenue
                    highest_revenue_agent = sales_agent

                # Comptabiliser les ventes par manager
                manager = fields.get("manager (from sales_agent)", "Unknown")
                if isinstance(manager, list):
                    manager = ", ".join(manager) if len(manager) > 0 else "Unknown"

                if manager not in total_sales_per_manager:
                    total_sales_per_manager[manager] = 0
                    total_revenue_per_manager[manager] = 0
                total_sales_per_manager[manager] += 1
                total_revenue_per_manager[manager] += revenue

                # Incrémenter le nombre total de ventes
                total_sales += 1

                # Vérifier le deal_stage et incrémenter les compteurs et revenus correspondants
                deal_stage = fields.get("deal_stage", "")
                if deal_stage == "Won":
                    total_won_sales += 1
                    total_won_revenue += revenue
                elif deal_stage == "Engaging":
                    total_engaging_sales += 1
                    total_engaging_revenue += revenue
                elif deal_stage == "Lost":
                    total_lost_sales += 1
                    total_lost_revenue += revenue
                elif deal_stage == "Prospecting":
                    total_prospecting_sales += 1
                    total_prospecting_revenue += revenue

                # Extraire et valider le office_location
                office_location = fields.get("office_location (from account)", "Unknown")
                if isinstance(office_location, list):
                    office_location = ", ".join(office_location) if len(office_location) > 0 else "Unknown"

                # Comptabiliser les ventes et revenus par office_location
                if office_location not in total_sales_per_office_location:
                    total_sales_per_office_location[office_location] = 0
                    total_revenue_per_office_location[office_location] = 0
                total_sales_per_office_location[office_location] += 1
                total_revenue_per_office_location[office_location] += revenue

            # Calcul des KPIs
            avg_revenue = total_revenue / total_products if total_products > 0 else 0
            avg_revenue_per_product = total_revenue / total_sales if total_sales > 0 else 0  # Revenu moyen par vente

            # Calcul du revenu moyen par secteur
            avg_revenue_per_sector = {sector: total_revenue / products_per_sector[sector] for sector, total_revenue in total_revenue_per_sector.items()}

            # Calcul du revenu moyen par office_location
            avg_revenue_per_office_location = {
                office_location: total_revenue / total_sales_per_office_location[office_location]
                for office_location, total_revenue in total_revenue_per_office_location.items()
            }

            # Calcul du revenu moyen par agent
            avg_revenue_per_agent = {
                agent: total_revenue / total_sales_per_agent[agent] for agent, total_revenue in total_revenue_per_agent.items()
            }

            # Calcul du revenu moyen par manager
            avg_revenue_per_manager = {
                manager: total_revenue / total_sales_per_manager[manager] for manager, total_revenue in total_revenue_per_manager.items()
            }

            # Retourner les KPIs
            return {         
                "total_products": total_products,  # Nombre total de produits dans le système.
                "total_revenue": total_revenue,  # Chiffre d'affaires total généré par toutes les ventes.
                "avg_revenue_per_product": avg_revenue,  # Revenu moyen généré par produit.
                "products_per_sector": products_per_sector,  # Nombre de produits répartis par secteur.
                "highest_revenue_agent": highest_revenue_agent,  # Agent ayant généré le revenu le plus élevé.
                "total_sales": total_sales,  # Nombre total de ventes réalisées.
                "avg_revenue_per_sale": avg_revenue_per_product,  # Revenu moyen généré par vente.
                "total_revenue_per_sector": total_revenue_per_sector,  # Revenu total généré par chaque secteur.
                "avg_revenue_per_sector": avg_revenue_per_sector,  # Revenu moyen généré par secteur.
                "total_won_sales": total_won_sales,  # Nombre total de ventes gagnées.
                "total_won_revenue": total_won_revenue,  # Revenu total généré par les ventes gagnées.
                "total_engaging_sales": total_engaging_sales,  # Nombre total de ventes engageantes (par exemple, des ventes plus longues ou plus complexes).
                "total_engaging_revenue": total_engaging_revenue,  # Revenu total généré par les ventes engageantes.
                "total_lost_sales": total_lost_sales,  # Nombre total de ventes perdues.
                "total_lost_revenue": total_lost_revenue,  # Revenu total perdu à cause des ventes ratées.
                "total_prospecting_sales": total_prospecting_sales,  # Nombre total de ventes provenant de la prospection.
                "total_prospecting_revenue": total_prospecting_revenue,  # Revenu total généré par les ventes issues de la prospection.
                "total_sales_per_office_location": total_sales_per_office_location,  # Nombre total de ventes par emplacement (bureau).
                "total_revenue_per_office_location": total_revenue_per_office_location,  # Revenu total par emplacement (bureau).
                "avg_revenue_per_office_location": avg_revenue_per_office_location,  # Revenu moyen par emplacement (bureau).
                "total_sales_per_agent": total_sales_per_agent,  # Nombre total de ventes réalisées par chaque agent.
                "total_revenue_per_agent": total_revenue_per_agent,  # Revenu total généré par chaque agent.
                "avg_revenue_per_agent": avg_revenue_per_agent,  # Revenu moyen généré par chaque agent.
                "total_sales_per_manager": total_sales_per_manager,  # Nombre total de ventes réalisées par chaque manager.
                "total_revenue_per_manager": total_revenue_per_manager,  # Revenu total généré par chaque manager.
                "avg_revenue_per_manager": avg_revenue_per_manager,  # Revenu moyen généré par chaque manager.
            }

        except httpx.HTTPStatusError as e:
            return JSONResponse(
                status_code=e.response.status_code,
                content={"message": f"Erreur HTTP : {e}"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": f"Erreur interne : {str(e)}"}
            )


@app.get("/product/kpis")
async def get_specific_product_kpis(product_name: str = Query(..., description="Name of the product to filter")):
    async with httpx.AsyncClient() as http_client:
        try:
            # Requête à l'API Airtable
            response = await http_client.get(f"{AIRTABLE_URL}sales_pipeline", headers=HEADERS)
            response.raise_for_status()

            # Récupérer les données JSON
            data = response.json()
            records = data.get("records", [])
            pprint.pprint(records)

            # Initialize metrics
            total_revenue = 0
            total_products = 0
            products_in_sector = {}

            # Process data
            for record in records:
                fields = record.get("fields", {})

                # Check if the product matches the filter
                product = fields.get("product")
                if product == product_name:
                    total_products += 1
                    revenue = fields.get("revenue (from account)", 0)
                    total_revenue += revenue

                    # Sector-specific information
                    sector = fields.get("sector (from account)", "Unknown")
                    if sector not in products_in_sector:
                        products_in_sector[sector] = 0
                    products_in_sector[sector] += 1

            if total_products == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"No records found for product: {product_name}"
                )

            # Calculate KPIs
            avg_revenue = total_revenue / total_products if total_products > 0 else 0

            return {
                "product_name": product_name,
                "total_products": total_products,
                "total_revenue": total_revenue,
                "avg_revenue_per_product": avg_revenue,
                "products_in_sector": products_in_sector
            }


        except httpx.HTTPStatusError as e:
            return JSONResponse(
                status_code=e.response.status_code,
                content={"message": f"Erreur HTTP : {e}"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": f"Erreur interne : {str(e)}"}
            )






####Sales


        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
