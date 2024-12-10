

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

1. **Total Products (Nombre total de produits)**  
   **Explication** : C'est le total des produits disponibles dans le système ou en stock.  
   **Ce que cela mesure** : Permet de mesurer l'inventaire global et de suivre la disponibilité des produits.

2. **Total Revenue (Chiffre d'affaires total)**  
   **Explication** : Le montant total des revenus générés par les ventes de produits/services.  
   **Ce que cela mesure** : Indicateur principal de la performance financière d'une entreprise.

3. **Average Revenue per Product (Revenu moyen par produit)**  
   **Explication** : La moyenne des revenus générés par chaque produit.  
   **Ce que cela mesure** : Permet de voir quels produits génèrent le plus de revenus en moyenne, et de comprendre la rentabilité par produit.

4. **Products per Sector (Produits par secteur)**  
   **Explication** : Le nombre de produits répartis par secteur d’activité ou catégorie.  
   **Ce que cela mesure** : Permet de suivre la diversité et la concentration des produits dans chaque secteur ou catégorie.

5. **Highest Revenue Agent (Agent ayant généré le revenu le plus élevé)**  
   **Explication** : L'agent de vente ayant réalisé le plus grand chiffre d'affaires.  
   **Ce que cela mesure** : Permet d'identifier les agents les plus performants en termes de revenus générés.

6. **Total Sales (Nombre total de ventes)**  
   **Explication** : Le total des ventes réalisées sur une période donnée.  
   **Ce que cela mesure** : Un indicateur global de l'activité commerciale et du volume de transactions réalisées.

7. **Average Revenue per Sale (Revenu moyen par vente)**  
   **Explication** : Le revenu moyen généré par chaque vente réalisée.  
   **Ce que cela mesure** : Permet d’évaluer la valeur moyenne de chaque vente, utile pour ajuster la stratégie commerciale.

8. **Total Revenue per Sector (Revenu total par secteur)**  
   **Explication** : Le revenu total généré par chaque secteur ou catégorie de produits.  
   **Ce que cela mesure** : Permet de voir la contribution de chaque secteur au revenu global de l'entreprise.

9. **Average Revenue per Sector (Revenu moyen par secteur)**  
   **Explication** : Le revenu moyen généré par chaque secteur d’activité.  
   **Ce que cela mesure** : Permet de comprendre la rentabilité de chaque secteur.

10. **Total Won Sales (Nombre total de ventes gagnées)**  
    **Explication** : Le nombre de ventes conclues avec succès.  
    **Ce que cela mesure** : Mesure de l'efficacité du processus de vente.

11. **Total Won Revenue (Revenu total des ventes gagnées)**  
    **Explication** : Le revenu total généré par les ventes réussies.  
    **Ce que cela mesure** : Permet de quantifier le succès des ventes conclues.

12. **Total Engaging Sales (Nombre total de ventes engageantes)**  
    **Explication** : Ventes nécessitant une interaction prolongée, souvent plus complexes.  
    **Ce que cela mesure** : Permet de mesurer l'engagement des prospects et la qualité des ventes réalisées.

13. **Total Engaging Revenue (Revenu total des ventes engageantes)**  
    **Explication** : Le revenu généré par les ventes engageantes.  
    **Ce que cela mesure** : Permet de voir si les ventes plus complexes ou engageantes sont plus rentables.

14. **Total Lost Sales (Nombre total de ventes perdues)**  
    **Explication** : Le nombre de ventes qui ont échoué.  
    **Ce que cela mesure** : Indicateur des opportunités perdues et aide à comprendre pourquoi les ventes échouent.

15. **Total Lost Revenue (Revenu total perdu)**  
    **Explication** : Le revenu qui aurait pu être généré mais qui a été perdu à cause de ventes non conclues.  
    **Ce que cela mesure** : Permet de quantifier l'impact des ventes perdues sur le revenu global.

16. **Total Prospecting Sales (Ventes provenant de la prospection)**  
    **Explication** : Le nombre de ventes réalisées grâce à la prospection active de nouveaux clients.  
    **Ce que cela mesure** : Mesure l'efficacité des efforts de prospection et la conversion des prospects.

17. **Total Prospecting Revenue (Revenu provenant de la prospection)**  
    **Explication** : Le revenu généré par les ventes obtenues via la prospection.  
    **Ce que cela mesure** : Permet de voir la rentabilité des efforts de prospection.

18. **Total Sales per Office Location (Ventes par emplacement/bureau)**  
    **Explication** : Le nombre total de ventes réalisées par chaque emplacement ou bureau.  
    **Ce que cela mesure** : Permet de comparer les performances entre différents sites.

19. **Total Revenue per Office Location (Revenu par emplacement/bureau)**  
    **Explication** : Le revenu total généré par chaque emplacement ou bureau.  
    **Ce que cela mesure** : Permet de comparer la rentabilité de chaque site de l'entreprise.

20. **Average Revenue per Office Location (Revenu moyen par emplacement/bureau)**  
    **Explication** : Le revenu moyen généré par chaque bureau ou emplacement.  
    **Ce que cela mesure** : Permet de comparer l'efficacité des différents bureaux.

21. **Total Sales per Agent (Ventes par agent)**  
    **Explication** : Le nombre total de ventes réalisées par chaque agent.  
    **Ce que cela mesure** : Permet d’évaluer la productivité individuelle des agents de vente.

22. **Total Revenue per Agent (Revenu par agent)**  
    **Explication** : Le revenu généré par chaque agent.  
    **Ce que cela mesure** : Permet de voir la contribution de chaque agent au chiffre d'affaires total.

23. **Average Revenue per Agent (Revenu moyen par agent)**  
    **Explication** : Le revenu moyen généré par chaque agent.  
    **Ce que cela mesure** : Permet de voir la performance moyenne des agents de vente.

24. **Total Sales per Manager (Ventes par manager)**  
    **Explication** : Le nombre total de ventes réalisées par chaque manager ou responsable.  
    **Ce que cela mesure** : Permet de mesurer l'efficacité des managers dans la supervision des ventes.

25. **Total Revenue per Manager (Revenu par manager)**  
    **Explication** : Le revenu total généré sous la direction de chaque manager.  
    **Ce que cela mesure** : Permet de suivre l'impact des managers sur les résultats financiers.

26. **Average Revenue per Manager (Revenu moyen par manager)**  
    **Explication** : Le revenu moyen généré par chaque manager.  
    **Ce que cela mesure** : Permet de comprendre l'efficacité des managers en termes de revenu moyen généré.

###obj
Ces KPIs permettent de mesurer la performance commerciale à différents niveaux (produit, secteur, agent, manager, bureau) et d'identifier les points forts et les zones d'amélioration dans l'entreprise. Ils offrent des insights précieux pour optimiser les stratégies de vente, de prospection, de gestion des agents et de gestion des bureaux.