from pymongo import MongoClient, TEXT
import os
from dotenv import load_dotenv

class Database:
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client['jimcostdev_api']

        # Colecciones en la base de datos
        self.contact_collection = self.db['contact']
        self.social_networks_collection = self.db['social_networks']
        self.perfil_collection = self.db['perfil']
        self.work_experience_collection = self.db['work_experience']
        self.education_collection = self.db['education']
        self.projects_collection = self.db['projects']
        self.certifications_collection = self.db['certifications']
        self.users_collection = self.db['users']
        self.customization_collection = self.db['customization']
        
        # Crear índices de texto
        self.users_collection.create_index([("email", TEXT)])
        self.users_collection.create_index([("username", TEXT)])

    def get_db(self):
        return self.db

    def close_connection(self):
        self.client.close()

# Función para obtener una instancia de la base de datos
def get_database_instance():
    # Obtener la cadena de conexión desde config.env
    load_dotenv("config.env")
    mongo_uri = os.getenv("MONGO_URI")

    # Instanciar la clase Database para manejar la conexión
    db = Database(mongo_uri)
    return db
