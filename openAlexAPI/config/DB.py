import mysql.connector
import configparser

class DB():

    def __init__(self):
        self.config = self.getConfig()
        self.connector = self.getConnector()
        self.cursor = self.getCursor()
        self.logConnect()

    def getCursor(self):
        return self.connector.cursor()

    def getConnector(self):
        return  mysql.connector.connect(
            host = self.config['DATABASE']['host'],
            user = self.config['DATABASE']['user'],
            password = self.config['DATABASE']['password'],
            database = self.config['DATABASE']['dbname']
        )

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('././config.ini')
        return config

    def logConnect(self):

        self.cursor.execute("SELECT VERSION()")

        results = self.cursor.fetchone()

        if results:
            print("INFO | Connexion effectuée avec votre base de donnée")
        else:
            print("ERROR | Problème avec la connexion de votre base de donnée")


