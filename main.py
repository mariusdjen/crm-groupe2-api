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
from urllib.parse import unquote
from collections import defaultdict
from datetime import datetime



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
            total_sales_won = 0
            total_sales_prospecting = 0
            total_sales_engaging = 0
            total_sales_lost = 0

            total_revenue = 0
            total_won_revenue = 0
            total_prospecting_revenue = 0
            total_engaging_revenue = 0
            total_lost_revenue = 0

            total_sales = 0
            products_per_sector = {}
            total_revenue_per_sector = {}
            avg_revenue_per_sector = {}
            total_sales_per_agent = {}
            total_revenue_per_agent = {}
            avg_revenue_per_agent = {}
            total_sales_per_manager = {}
            total_revenue_per_manager = {}
            avg_revenue_per_manager = {}
            revenue_per_month = defaultdict(float)
            sales_per_month = defaultdict(int)  # Répartition des ventes par mois

            # Traitement des enregistrements pour calculer les KPIs
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

                # Extraire et traiter le deal_stage pour le calcul des ventes
                deal_stage = fields.get("deal_stage", "")
                if deal_stage == "Won":
                    total_sales_won += 1
                    total_won_revenue += revenue
                elif deal_stage == "Prospecting":
                    total_sales_prospecting += 1
                    total_prospecting_revenue += revenue
                elif deal_stage == "Engaging":
                    total_sales_engaging += 1
                    total_engaging_revenue += revenue
                elif deal_stage == "Lost":
                    total_sales_lost += 1
                    total_lost_revenue += revenue

                # Extraire et traiter les Unknown champs pour les KPIs
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

                # Comptabiliser les ventes et revenus par agent
                sales_agent = fields.get("sales_agent (from sales_agent)", "Unknown")
                if isinstance(sales_agent, list):
                    sales_agent = ", ".join(sales_agent) if len(sales_agent) > 0 else "Unknown"

                if sales_agent not in total_sales_per_agent:
                    total_sales_per_agent[sales_agent] = 0
                    total_revenue_per_agent[sales_agent] = 0
                total_sales_per_agent[sales_agent] += 1
                total_revenue_per_agent[sales_agent] += revenue

                # Comptabiliser les ventes et revenus par manager
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

                # Extraire la date de fermeture (close_date) pour les revenus par mois
                close_date = fields.get("close_date", "")
                try:
                    # Convertir la date en format datetime
                    close_date = datetime.strptime(close_date, "%Y-%m-%d") if close_date else None
                    if close_date:
                        # Extraire le mois et l'année
                        month_year = close_date.strftime("%Y-%m")
                        # Ajouter le revenu au mois correspondant
                        revenue_per_month[month_year] += revenue
                        sales_per_month[month_year] += 1  # Compter les ventes par mois
                except ValueError:
                    pass  # Si la date est invalide ou absente, ignorer cette entrée

            # Calcul des KPIs
            avg_revenue_per_product = total_revenue / total_sales if total_sales > 0 else 0  # Revenu moyen par vente

            # Calcul du revenu moyen par secteur
            avg_revenue_per_sector = {sector: total_revenue / products_per_sector[sector] for sector, total_revenue in total_revenue_per_sector.items()}

            # Calcul du revenu moyen par agent
            avg_revenue_per_agent = {
                agent: total_revenue / total_sales_per_agent[agent] for agent, total_revenue in total_revenue_per_agent.items()
            }

            # Calcul du revenu moyen par manager
            avg_revenue_per_manager = {
                manager: total_revenue / total_sales_per_manager[manager] for manager, total_revenue in total_revenue_per_manager.items()
            }

            # Calcul du taux d'engagement (engaging / total_sales)
            engagement_rate = total_sales_engaging / total_sales if total_sales > 0 else 0


            # Function to filter out "Unknown" values
            def filter_unknown(data):
                return {k: v for k, v in data.items() if k != "Unknown" and v != "Unknown"}
            
            products_per_sector = filter_unknown(products_per_sector)
            total_revenue_per_sector = filter_unknown(total_revenue_per_sector)
            avg_revenue_per_sector = filter_unknown(avg_revenue_per_sector)
            total_sales_per_agent = filter_unknown(total_sales_per_agent)
            total_revenue_per_agent = filter_unknown(total_revenue_per_agent)
            avg_revenue_per_agent = filter_unknown(avg_revenue_per_agent)
            total_sales_per_manager = filter_unknown(total_sales_per_manager)
            total_revenue_per_manager = filter_unknown(total_revenue_per_manager)
            avg_revenue_per_manager = filter_unknown(avg_revenue_per_manager)


            # Retourner les KPIs et le classement des revenus par mois
            return {         
                "total_sales_won": total_sales_won,
                "total_sales_prospecting": total_sales_prospecting,
                "total_sales_engaging": total_sales_engaging,
                "total_sales_lost": total_sales_lost,
                "total_revenue": total_revenue,
                "total_won_revenue": total_won_revenue,
                "total_prospecting_revenue": total_prospecting_revenue,
                "total_engaging_revenue": total_engaging_revenue,
                "total_lost_revenue": total_lost_revenue,
                "avg_revenue_per_product": avg_revenue_per_product,
                "products_per_sector": products_per_sector,
                "total_revenue_per_sector": total_revenue_per_sector,
                "avg_revenue_per_sector": avg_revenue_per_sector,
                "total_sales_per_agent": total_sales_per_agent,
                "total_revenue_per_agent": total_revenue_per_agent,
                "avg_revenue_per_agent": avg_revenue_per_agent,
                "total_sales_per_manager": total_sales_per_manager,
                "total_revenue_per_manager": total_revenue_per_manager,
                "avg_revenue_per_manager": avg_revenue_per_manager,
                "revenue_per_month": dict(revenue_per_month),
                "sales_per_month": dict(sales_per_month),  # Répartition des ventes par mois
                "engagement_rate": engagement_rate  # Taux d'engagement
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

@app.get('/getProductKpis/{product_name}')
async def getProductKpis(product_name: str):
    async with httpx.AsyncClient() as http_client:
        try:
            # Requête à l'API Airtable pour récupérer les données du sales_pipeline
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
            # Fonction pour filtrer les valeurs inconnues
            def filter_unknown(data):
                return {k: v for k, v in data.items() if k not in ["Unknown", "Inconnu"] and v not in ["Unknown", "Inconnu"]}

            # Initialisation des métriques
            total_sales_won = 0
            total_sales_lost = 0
            total_revenue = 0
            total_deals = 0
            sales_by_region = defaultdict(int)
            sales_by_sector = defaultdict(int)

            # Calcul des KPIs
            for record in records:
                fields = record.get("fields", {})

                # Extraire le nom du produit et vérifier si c'est une liste
                product = fields.get("product (from product)", [])
                if isinstance(product, list):
                    product_name_record = product[0] if len(product) > 0 else ""                 
                else:
                    product_name_record = str(product)

                # Comparer avec le produit recherché
                if product_name.lower() != product_name_record.lower():
                    continue

                # Statistiques sur le deal_stage
                deal_stage = fields.get("deal_stage", "").lower()
                total_deals += 1  # Compte total des deals
                if deal_stage == "won":
                    total_sales_won += 1
                    # Extraire et valider le revenu
                    revenue = fields.get("sales_price (from product)", 0)
                    if isinstance(revenue, list):
                        revenue = revenue[0] if len(revenue) > 0 else 0
                    try:
                        revenue = float(revenue)
                    except (ValueError, TypeError):
                        revenue = 0
                    total_revenue += revenue
                elif deal_stage == "lost":
                    total_sales_lost += 1

                # Calculer les ventes par région
                region = fields.get("office_location (from account)", "Inconnu")
                if isinstance(region, list):
                    region = region[0] if len(region) > 0 else "Inconnu"
                sales_by_region[region] += 1

                # Calculer les ventes par secteur
                sector = fields.get("sector (from account)", "Inconnu")
                if isinstance(sector, list):
                    sector = sector[0] if len(sector) > 0 else "Inconnu"
                sales_by_sector[sector] += 1

            # Si aucun produit n'a été trouvé
            if total_sales_won == 0 and total_sales_lost == 0:
                return JSONResponse(
                    status_code=200,
                    content={"message": f"Aucune donnée disponible pour le produit: '{product_name}' d."}
                )

            # Calcul des taux
            total_sales = total_sales_won + total_sales_lost
            resignation_rate = (total_sales_lost / total_sales) * 100 if total_sales > 0 else 0
            engagement_rate = (total_sales_won / total_deals) * 100 if total_deals > 0 else 0
            # Filtrer les valeurs inconnues
            sales_by_region = filter_unknown(sales_by_region)
            sales_by_sector = filter_unknown(sales_by_sector)
            # Retourner les KPIs pour le produit spécifique
            return {
                "product_name": product_name,
                "total_deals": total_deals,
                "total_sales_won": total_sales_won,
                "total_sales_lost": total_sales_lost,
                "total_sales": total_sales,
                "total_revenue": total_revenue,
                "avg_revenue": total_revenue / total_sales_won if total_sales_won > 0 else 0,
                "resignation_rate": resignation_rate,
                "engagement_rate": engagement_rate,
                "sales_by_region": dict(sales_by_region),
                "sales_by_sector": dict(sales_by_sector)
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

# ###agent and team  

@app.get('/getAllTeamsKpis/')
async def getAllTeamsKpis():
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
            total_sales = 0
            total_revenue = 0
            total_sales_per_agent = {}
            total_revenue_per_agent = {}
            avg_revenue_per_agent = {}
            total_sales_per_manager = {}
            total_revenue_per_manager = {}
            avg_revenue_per_manager = {}
            sales_per_month = defaultdict(int)
            revenue_per_month = defaultdict(float)

            # Comptage des transactions par statut
            deals_status_count = {"Won": 0, "Lost": 0, "Engaging": 0, "Prospecting": 0}

            # Traitement des enregistrements pour calculer les KPIs
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

                # Extraire et traiter le deal_stage pour le calcul des ventes
                deal_stage = fields.get("deal_stage", "")
                if deal_stage in deals_status_count:
                    deals_status_count[deal_stage] += 1
                    if deal_stage == "Won":
                        total_sales += 1  # On ne compte que les ventes "Won" dans le total

                # Extraire l'agent de vente pour les KPIs individuels
                sales_agent = fields.get("sales_agent (from sales_agent)", "Unknown")
                if isinstance(sales_agent, list):
                    sales_agent = ", ".join(sales_agent) if len(sales_agent) > 0 else "Unknown"

                # Comptabiliser les ventes et revenus par agent
                if sales_agent not in total_sales_per_agent:
                    total_sales_per_agent[sales_agent] = 0
                    total_revenue_per_agent[sales_agent] = 0
                total_sales_per_agent[sales_agent] += 1
                total_revenue_per_agent[sales_agent] += revenue

                # Extraire le manager et comptabiliser les ventes et revenus par manager
                manager = fields.get("manager (from sales_agent)", "Unknown")
                if isinstance(manager, list):
                    manager = ", ".join(manager) if len(manager) > 0 else "Unknown"

                if manager not in total_sales_per_manager:
                    total_sales_per_manager[manager] = 0
                    total_revenue_per_manager[manager] = 0
                total_sales_per_manager[manager] += 1
                total_revenue_per_manager[manager] += revenue

                # Incrémenter les ventes et les revenus par mois
                close_date = fields.get("close_date", "")
                try:
                    close_date = datetime.strptime(close_date, "%Y-%m-%d") if close_date else None
                    if close_date:
                        month_year = close_date.strftime("%Y-%m")
                        revenue_per_month[month_year] += revenue
                        sales_per_month[month_year] += 1
                except ValueError:
                    pass

            # Calcul des KPIs moyens
            avg_revenue_per_agent = {
                agent: total_revenue / total_sales_per_agent[agent] for agent, total_revenue in total_revenue_per_agent.items()
            }

            avg_revenue_per_manager = {
                manager: total_revenue / total_sales_per_manager[manager] for manager, total_revenue in total_revenue_per_manager.items()
            }

            # Calcul des ratios de performance par agent
            won_ratio_per_agent = {
                agent: (deals_status_count["Won"] / total_sales_per_agent[agent]) * 100
                if total_sales_per_agent[agent] > 0 else 0
                for agent in total_sales_per_agent
            }

            lost_ratio_per_agent = {
                agent: (deals_status_count["Lost"] / total_sales_per_agent[agent]) * 100
                if total_sales_per_agent[agent] > 0 else 0
                for agent in total_sales_per_agent
            }

            # Calcul des ratios de performance par manager
            won_ratio_per_manager = {
                manager: (deals_status_count["Won"] / total_sales_per_manager[manager]) * 100
                if total_sales_per_manager[manager] > 0 else 0
                for manager in total_sales_per_manager
            }

            lost_ratio_per_manager = {
                manager: (deals_status_count["Lost"] / total_sales_per_manager[manager]) * 100
                if total_sales_per_manager[manager] > 0 else 0
                for manager in total_sales_per_manager
            }

            # Calcul des ratios globaux
            total_deals = sum(deals_status_count.values())
            won_ratio = (deals_status_count["Won"] / total_deals) * 100 if total_deals > 0 else 0
            lost_ratio = (deals_status_count["Lost"] / total_deals) * 100 if total_deals > 0 else 0

            # Filtrer les résultats "Unknown"
            def filter_unknown(data):
                return {k: v for k, v in data.items() if k != "Unknown" and v != "Unknown"}

            total_sales_per_agent = filter_unknown(total_sales_per_agent)
            total_revenue_per_agent = filter_unknown(total_revenue_per_agent)
            avg_revenue_per_agent = filter_unknown(avg_revenue_per_agent)
            total_sales_per_manager = filter_unknown(total_sales_per_manager)
            total_revenue_per_manager = filter_unknown(total_revenue_per_manager)
            avg_revenue_per_manager = filter_unknown(avg_revenue_per_manager)

            # Retourner les KPIs
            return {
                "total_sales": total_sales,
                "total_revenue": total_revenue,
                "total_sales_per_agent": total_sales_per_agent,
                "total_revenue_per_agent": total_revenue_per_agent,
                "avg_revenue_per_agent": avg_revenue_per_agent,
                "total_sales_per_manager": total_sales_per_manager,
                "total_revenue_per_manager": total_revenue_per_manager,
                "avg_revenue_per_manager": avg_revenue_per_manager,
                "sales_per_month": dict(sales_per_month),
                "revenue_per_month": dict(revenue_per_month),
                "deals_status_count": deals_status_count,
                "won_ratio": won_ratio,
                "lost_ratio": lost_ratio,
                "won_ratio_per_agent": won_ratio_per_agent,
                "lost_ratio_per_agent": lost_ratio_per_agent,
                "won_ratio_per_manager": won_ratio_per_manager,
                "lost_ratio_per_manager": lost_ratio_per_manager,
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
