import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging
from typing import Optional

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

# Configurações do MongoDB
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fetalcare_db")
COLLECTION_NAME = "registros_exames"

async def connect_to_mongo():
    """Conecta ao MongoDB"""
    try:
        MongoDB.client = AsyncIOMotorClient(MONGODB_URL)
        MongoDB.database = MongoDB.client[DATABASE_NAME]
        
        # Testa a conexão
        await MongoDB.client.admin.command('ping')
        logger.info(f"✅ Conectado ao MongoDB: {MONGODB_URL}")
        logger.info(f"📊 Banco de dados: {DATABASE_NAME}")
        
        # Cria índices para otimização
        await criar_indices()
        
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Fecha a conexão com MongoDB"""
    if MongoDB.client:
        MongoDB.client.close()
        logger.info("📴 Conexão com MongoDB encerrada")

def get_database():
    """Retorna a instância do banco de dados"""
    if MongoDB.database is None:
        raise Exception("Banco de dados não inicializado. Execute connect_to_mongo() primeiro.")
    return MongoDB.database

def get_collection():
    """Retorna a collection de registros de exames"""
    database = get_database()
    return database[COLLECTION_NAME]

async def criar_indices():
    """Cria índices para otimização das consultas"""
    try:
        collection = get_collection()
        
        # Índice no CPF para busca rápida
        await collection.create_index("dados_gestante.patient_cpf")
        
        # Índice no ID da gestante
        await collection.create_index("dados_gestante.patient_id")
        
        # Índice na data do exame
        await collection.create_index("data_exame")
        
        # Índice composto para busca por CPF e data
        await collection.create_index([
            ("dados_gestante.patient_cpf", 1),
            ("data_exame", -1)
        ])
        
        # Índice no status de saúde para relatórios
        await collection.create_index("saude_feto.status_saude")
        
        logger.info("📈 Índices criados com sucesso")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar índices: {e}")

# Configuração para uso síncrono (para testes ou operações específicas)
def get_sync_database():
    """Retorna conexão síncrona com MongoDB (para testes)"""
    sync_client = MongoClient(MONGODB_URL)
    return sync_client[DATABASE_NAME]

def get_sync_collection():
    """Retorna collection síncrona"""
    sync_db = get_sync_database()
    return sync_db[COLLECTION_NAME]

# Verificação de saúde do banco
async def verificar_saude_banco():
    """Verifica se o banco está funcionando corretamente"""
    try:
        database = get_database()
        collection = get_collection()
        
        # Conta documentos
        total_registros = await collection.count_documents({})
        
        # Verifica conectividade
        server_info = await MongoDB.client.server_info()
        
        return {
            "status": "healthy",
            "mongodb_version": server_info.get("version"),
            "total_registros": total_registros,
            "database_name": DATABASE_NAME,
            "collection_name": COLLECTION_NAME
        }
        
    except Exception as e:
        logger.error(f"❌ Erro na verificação de saúde: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        } 