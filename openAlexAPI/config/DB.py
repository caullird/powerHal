import mysql.connector
import configparser

class DB():

    # Initialisation des informations de la base de données
    def __init__(self):
        self.config = self.getConfig()
        self.connector = self.getConnector()
        self.cursor = self.getCursor()
        self.logConnect()

    # Permet la récupération du connector depuis l'ensemble du projet
    def getConnector(self):
        return self.connector

    # Permet la récupération du curseur depuis l'ensemble du projet
    def getCursor(self):
        return self.connector.cursor()
    
    # Permet de connecter depuis les informations du fichier de configuration
    def getConnector(self):
        return  mysql.connector.connect(
            host = self.config['DATABASE']['host'],
            user = self.config['DATABASE']['user'],
            password = self.config['DATABASE']['password'],
            database = self.config['DATABASE']['dbname']
        )

    # Permet de récupérer la configuration du fichier config.ini
    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('././config.ini')
        return config

    # Permet d'insérer une ligne dans la base de données
    def makeInsertion(self, sql, val):
        self.cursor.execute(sql,val)
        self.connector.commit()

    # Permet de verifier si la ligne existe déjà
    def checkIfExists(self, table, values):
        print(values)

    # Permet de vérifier la bonne connexion a la base de données
    def logConnect(self):

        self.cursor.execute("SELECT VERSION()")

        results = self.cursor.fetchone()

        if results:
            print("INFO | Connexion effectuée avec votre base de donnée")
        else:
            print("ERROR | Problème avec la connexion de votre base de donnée")
