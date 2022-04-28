import mysql.connector
import configparser
import inspect

class DB():

    # Initialisation des informations de la base de données
    def __init__(self):
        self.config = self.getConfig()
        self.connector = self.getConnector()
        self.cursor = self.getCursor()
        self.logConnect()


    # Permet la récupération du curseur depuis l'ensemble du projet
    def getCursor(self):
        return self.connector.cursor(buffered=True)


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
        config.read('./././config.ini')
        return config


    # Permet de vérifier la bonne connexion a la base de données
    def logConnect(self):

        self.cursor.execute("SELECT VERSION()")

        results = self.cursor.fetchone()

        if results:
            print("INFO | Connexion effectuée avec votre base de donnée")
        else:
            print("ERROR | Problème avec la connexion de votre base de donnée")


    # Permet de verifier si la ligne existe déjà, et de l'insérer sinon
    def checkIfExistsOrInsert(self, object, fieldsComparable, autoUpdate = False):

        fields = self.sortByFieldName(self.getObjectFields(object, type = "all"), fieldsComparable)

        sql = 'SELECT * FROM ' + self.getClassName(object) + ' WHERE '

        for field in fields:
            sql += field[0] + ' = "' + str(field[1]) + '" AND '

        self.cursor.execute(sql[:-4])
        
        row = self.cursor.fetchone()
        if row == None: 
            return self.autoInsert(object)
        else:
            if(autoUpdate):
                return self.autoUpdate(object,row)
            return row[0]


    # Permet de mettre à jour le modèle en fonction de la demande
    def autoUpdate(self, object, mySQLObject):
        
        className = self.getClassName(object)

        objectFields = dict((x, y) for x, y in self.getObjectFields(object, type = "all"))
        mySQLFields = dict((x, y) for x, y in tuple(zip(self.cursor.column_names, mySQLObject)))

        removeFields = ["id_" + str(className).lower(),"created_at","updated_at","deleted_at"]
        for removeField in removeFields:
            del mySQLFields[removeField]

        for key, value in objectFields.items():
            objectFields[key] = str(value)


        if(sorted(mySQLFields.items(), key=lambda t: t[0]) != sorted(objectFields.items(), key=lambda t: t[0])):
            sql = 'UPDATE ' + str(className) + ' SET '
            for key, value in objectFields.items():
                if value not in ["","[]","{}","()","NULL","None"]:
                    sql += key + ' = "' + str(value) + '", '
            sql = sql[:-2] + ' WHERE id_' + str(className).lower() + ' = ' + str(mySQLObject[0])

            self.cursor.execute(sql)
            #print("INFO | Un(e) " + str(className) + " a été mis à jour sur votre base de données")

            self.addActionAt(className, mySQLObject[0], "updated")

        return mySQLObject[0]


    # Permet de filtrer en fonction des champs de recherche 
    def sortByFieldName(self, fields, fieldsComparable):
        results = []

        for field in fields:
            if field[0] in fieldsComparable:
                results.append(field)
        
        return results


    # Automatisation de l'insertion dans la base de données
    def autoInsert(self, object):

        className = self.getClassName(object)
        fieldsNames = self.getObjectFields(object, type = "names")
        fieldsValues = self.getObjectFields(object, type = "values")

        sql = 'INSERT INTO ' + str(className) + '(' + ", ".join(fieldsNames) + ') VALUES ("' + '", "'.join(fieldsValues) + '")'
        
        self.cursor.execute(sql)

        #print("INFO | Un(e) nouveau/elle " + str(className) + " a été ajouté sur votre base de données")
        
        insertId = self.cursor.lastrowid

        self.addActionAt(className, insertId, "created")

        return insertId


    # Permet de récupérer les champs d'un objet, que ce soit des noms ou des values
    def getObjectFields(self, object, type):
        fields = []

        for field in inspect.getmembers(object):
            if not field[0].startswith('_') and not inspect.ismethod(field[1]) and not field[0] == "database":
                if(type == "names"):
                    fields.append(field[0])
                elif(type == "values"):
                    fields.append(str(field[1]))
                elif(type == "all"):
                    fields.append(field)
        return fields


    # Permet de récupérer le nom de la classe actuelle
    def getClassName(self,object):
        return type(object).__name__


    # Permet de récupérer l'ID de la source actuelle
    def getSourceID(self, className):
        self.cursor.execute("SELECT DISTINCT id_source FROM source WHERE display_name = '" + str(className) + "'")
        return self.cursor.fetchone()[0]


    # Permet de fermer la connexion a la base de données
    def close(self):
        self.cursor.close()
        self.connector.close()

    # Permet d'ajouter ou de modifier le statut d'un objet
    def addActionAt(self, classname, id, action):
        self.cursor.execute("UPDATE " + str(classname) + " SET " + action + "_at = NOW() WHERE id_" + str(classname).lower() + " = " + str(id))

    def getFieldsWithId(self, id, table, searchField, getField, quantity):
        self.cursor.execute('SELECT ' + getField + ' FROM ' + table + ' WHERE ' + searchField + ' = ' + str(id))

        if(quantity == "many"):
            return [item[0] for item in self.cursor.fetchall()]
        
        return self.cursor.fetchone()[0]
