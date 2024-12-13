

# Projet HeticEtronics - Dashboard Performances Commerciales

## Introduction

Ce projet consiste à créer un dashboard interactif pour analyser les performances commerciales de l'entreprise fictive HeticEtronics. Les données CRM sont stockées dans Airtable et l'API FastAPI est utilisée pour interagir avec ces données et fournir des informations agrégées pour la visualisation.

## Prérequis

Avant de commencer, vous devez avoir installé :

- **Python** : Téléchargez Python ici : [python.org](https://www.python.org/downloads/).
- **PyCharm** : Téléchargez PyCharm ici : [JetBrains](https://www.jetbrains.com/pycharm/download/).
- **pip** : Le gestionnaire de paquets Python, normalement installé avec Python.





## Avec Visual Studio Code, si vous comptez utiliser PyCharm, il faut ignorer cette section
### 1. Cloner le repository

Clonez le repository sur votre machine à l'aide de la commande suivante :

```bash
git clone https://github.com/mariusdjen/crm-groupe2-api.git
```

### 2. Créer un environnement virtuel

Un environnement virtuel permet d'isoler les dépendances du projet pour éviter les conflits avec d'autres projets. Créez un environnement virtuel avec la commande suivante :

```bash
python -m venv env
```

Activez l'environnement virtuel :

- Sur Windows :

  ```bash
  venv\Scripts\activate
  ```

- Sur Mac/Linux :

  ```bash
  source venv/bin/activate
  ```

### 3. Installer les dépendances

Une fois l'environnement virtuel activé, installez toutes les dépendances nécessaires en utilisant le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement

Le projet utilise un fichier `.env` pour stocker des variables sensibles (par exemple, les clés API). Créez un fichier `.env` à la racine du projet et ajoutez les variables suivantes (en remplaçant par vos propres valeurs) :

```env
AIRTABLE_API_TOKEN=your_AIRTABLE_API_TOKEN
AIRTABLE_BASE_ID=your_airtable_base_id
```

### 5. Démarrer le serveur FastAPI

Une fois les dépendances installées et la configuration terminée, vous pouvez démarrer le serveur FastAPI avec la commande suivante :

```bash
uvicorn main:app --reload
```

Cela démarrera le serveur localement. Vous pourrez accéder à l'API en ouvrant votre navigateur et en visitant [http://localhost:8000](http://localhost:8000).

### 6. Tester les endpoints

L'API expose plusieurs endpoints pour interagir avec les données d'Airtable. Par exemple :

- **GET /getAllsalesPipeline** : récupère la liste des commandes.


Les endpoints peuvent être testés en utilisant un outil comme [http://localhost:8000/docs](http://localhost:8000/docs), où une documentation interactive est générée automatiquement par FastAPI.

## Structure du projet

Voici un aperçu de la structure des fichiers du projet :

```
heticetronics-dashboard(ou le nom de votre projet)/
├── main.py            # Code principal de l'application FastAPI
├── requirements.txt   # Liste des dépendances
├── .env               # Fichier de configuration des variables d'environnement
├── README.md          # Ce fichier
└── venv/              # Environnement virtuel
```

## Dépannage

- Si vous obtenez une erreur liée à l'installation des dépendances, assurez-vous que `pip` est à jour :

  ```bash
  pip install --upgrade pip
  ```

- Si le serveur ne démarre pas, vérifiez que toutes les variables d'environnement sont correctement configurées dans le fichier `.env`.






## Étapes pour démarrer le projet avec PyCharm

### 1. Cloner le repository

Clonez le repository sur votre machine en utilisant la commande suivante ou en ouvrant PyCharm et en clonant directement depuis l'interface de l'IDE.

- Ouvrez **PyCharm**.
- Allez dans **File > New Project from Version Control**.
- Collez l'URL du repository Git.

Alternativement, vous pouvez cloner le repository via la ligne de commande :

```bash
git clone https://github.com/mariusdjen/crm-groupe2-api.gi
```

### 2. Ouvrir le projet dans PyCharm

Après avoir cloné le projet, ouvrez-le avec PyCharm :

- Ouvrez PyCharm, puis allez dans **File > Open** et sélectionnez le dossier où vous avez cloné le projet.

### 3. Créer un environnement virtuel

Un environnement virtuel permet de garder les dépendances du projet isolées.

- **Dans PyCharm** : Lorsque vous ouvrez le projet, PyCharm vous demandera si vous souhaitez créer un environnement virtuel. Acceptez et PyCharm configurera automatiquement un environnement virtuel pour vous.

Si cela ne se fait pas automatiquement, vous pouvez le faire manuellement en suivant ces étapes :

- Allez dans **File > Settings > Project: votre_projet > Python Interpreter**.
- Cliquez sur l'icône de roue dentée et choisissez **Add**.
- Sélectionnez **New environment** et **Virtualenv**, puis choisissez l'emplacement de votre environnement.

### 4. Installer les dépendances

Une fois l'environnement virtuel configuré, PyCharm détectera automatiquement le fichier `requirements.txt`. Pour installer les dépendances :

- **PyCharm** : Allez dans **Terminal** (en bas de l'IDE) et tapez :

  ```bash
  pip install -r requirements.txt
  ```

PyCharm devrait aussi proposer d'installer les dépendances manquantes si elles ne sont pas déjà installées.

### 5. Configuration de l'environnement

Le projet utilise un fichier `.env` pour stocker des variables sensibles comme les clés API.

- Créez un fichier `.env` dans la racine du projet et ajoutez les variables nécessaires (par exemple) :

```env
AIRTABLE_API_TOKEN=your_AIRTABLE_API_TOKEN
AIRTABLE_BASE_ID=your_airtable_base_id
```

### 6. Démarrer le serveur FastAPI

Une fois les dépendances installées et la configuration terminée, vous pouvez démarrer le serveur FastAPI.

- **PyCharm** : Allez dans **Run > Edit Configurations**.
  - Cliquez sur l'icône **+** en haut à gauche et sélectionnez **Python**.
  - Dans **Script Path**, choisissez le fichier `main.py`.
  - Dans **Parameters**, entrez :

    ```bash
    uvicorn main:app --reload
    ```

- Ensuite, cliquez sur **Run** ou utilisez **Shift + F10** pour démarrer le serveur. Vous verrez dans le terminal de PyCharm que le serveur démarre et est accessible sur [http://localhost:8000](http://localhost:8000).

### 7. Tester les endpoints

Une fois le serveur démarré, vous pouvez tester les endpoints de l'API en allant sur la documentation générée automatiquement par FastAPI.

- Ouvrez un navigateur et allez sur [http://localhost:8000/docs](http://localhost:8000/docs).
- Vous pouvez interagir avec les endpoints directement depuis cette interface.

### 8. Déboguer avec PyCharm

Si vous avez besoin de déboguer votre code, PyCharm offre une excellente fonctionnalité de débogage.

- Mettez un point d'arrêt (breakpoint) dans votre code en cliquant à côté du numéro de ligne.
- Ensuite, dans **Run > Debug**, lancez le débogage. Le programme s'arrêtera au point d'arrêt et vous pourrez inspecter les variables et suivre l'exécution pas à pas.

## Structure du projet

Voici un aperçu de la structure des fichiers du projet :

```
heticetronics-dashboard(ou le nom de votre projet)/
├── main.py            # Code principal de l'application FastAPI
├── requirements.txt   # Liste des dépendances
├── .env               # Fichier de configuration des variables d'environnement
├── README.md          # Ce fichier
└── venv/              # Environnement virtuel
```

## Dépannage

- Si vous obtenez une erreur liée à l'installation des dépendances, assurez-vous que `pip` est à jour :

  ```bash
  pip install --upgrade pip
  ```

- Si le serveur ne démarre pas, vérifiez que toutes les variables d'environnement sont correctement configurées dans le fichier `.env`.

## Contribution







Les indicateurs clés de performance (KPIs) liés à l'analyse des ventes et des revenus:


Pour nos KPI’s sélectionnés, nous les avons classés par catégorie afin de mieux organiser notre vision du Dashboard. Au total, nous avons choisi 20 KPI’s.

### 1. Performance des ventes :
- Suivre l’évolution du nombre de ventes réalisées par année pour identifier les tendances dans le temps.
- Analyser la répartition des ventes par région et mesurer les différences de performance géographique.
- Étudier la répartition des ventes par produit afin de détecter les produits les plus performants.
- Identifier les secteurs d’activité associés aux produits vendus pour comprendre leur distribution.
- Déterminer les secteurs d’activité générant le plus grand volume de ventes, ainsi que ceux ayant les plus faibles performances, par année.
- Calculer le total des ventes réalisées chaque année pour avoir une vue d’ensemble des performances globales.
- Comptabiliser le nombre total de ventes perdues, par secteur et par année, pour repérer les faiblesses.
- Identifier le client qui rapporte le plus de revenus/ventes.

### 2. Performances des équipes :
- Identifier le meilleur agent de vente en termes de nombre de ventes réalisées, par année.
- Déterminer le meilleur agent de vente selon le chiffre d’affaires généré par année.
- Cartographier les équipes par manager pour analyser leur structure et leur efficacité.
- Évaluer quelle équipe réalise le plus de ventes et identifier les clients associés à ces ventes.

### 3. Performances financières :
- Suivre le chiffre d’affaires réalisé sur la dernière année de référence (2017).
- Calculer les revenus moyens générés par région, par année, pour évaluer les différences géographiques.
- Mesurer le prix moyen du panier par client, par année, pour comprendre les habitudes d’achat.
- Identifier le meilleur pourcentage de remise accordé, du point de vue de l’entreprise, pour optimiser les politiques tarifaires.

### 4. Gestion des comptes et fidélisation :
- Analyser l’évolution du nombre de comptes (accounts) créés par année afin de mesurer la croissance client.
- Calculer le pourcentage de clients actifs sur une période donnée pour évaluer le taux de rétention.
- Mesurer le taux de récurrence des commandes par secteur et par année pour identifier les secteurs fidélisés.


### Intérêt Global de ces KPIs  
- Ces KPIs permettent une vue d’ensemble des performances commerciales d’un produit.  
- Ils facilitent la prise de décision, par exemple :  
  - Renforcer les efforts marketing sur les régions ou secteurs sous-performants.  
  - Ajuster les stratégies de tarification ou de distribution.  
  - Identifier les opportunités de diversification ou d’amélioration.

