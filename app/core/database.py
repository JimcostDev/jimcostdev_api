from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.is_connected = False
    
    async def connect(self):
        if not self.is_connected:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[settings.MONGODB_NAME]
            await self.client.admin.command('ping')
            self.is_connected = True
            print("Conexión a MongoDB exitosa.")
    
    async def disconnect(self):
        if self.client:
            self.client.close()
            self.is_connected = False
            print("Conexión a MongoDB cerrada.")
    
    async def get_collection(self, collection_name: str):
        """Obtiene una colección conectando automáticamente si es necesario"""
        if not self.is_connected:
            await self.connect()
        return self.db[collection_name]

mongodb = MongoDB()