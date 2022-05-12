# ⚡ PowerHAL

## But du projet

HAL est une archive ouverte pluridisciplinaire, destinée au dépôt et à la diffusion d'articles scientifiques de niveau recherche, publiés ou non, et de thèses, émanant des établissements d'enseignement et de recherche français ou étrangers, des laboratoires publics ou privés.  


## Comment l'utiliser

1. Installation des librairies

TODO

2. Lancement de la base de données
    - Dans une base de donnée SQL ayant un user "root" sans mot de passe, créer une base nomée "proj831"
    - Importer le script "script.sql"

3. Lancement de l'API interne
    - Dans le dossier "scraperAPI", dans un terminale, lancer la commande :
    ```ps
    python -m uvicorn api:app --reload
    ```

4. Lancement du server Web
Dans le dossier powerHal :
    - Pour windows :
        ```ps
        set FLASK_APP=run.py
        set FLASK_ENV=development
        python -m flask run --host=0.0.0.0 --port=5000
        ```
    - Pour Unix/MacOS :
        ```ps
        export FLASK_APP=run.py
        export FLASK_ENV=development
        python -m flask run --host=0.0.0.0 --port=5000
        ```
    - Dans un PowwerShell :
        ```ps
        $env:FLASK_APP = ".\run.py"
        $env:FLASK_ENV = "development"
        python -m flask run --host=0.0.0.0 --port=5000
        ```

5. Accès à l'interface

Dans un navigateur, aller a l'adresse http://127.0.0.1:5000/