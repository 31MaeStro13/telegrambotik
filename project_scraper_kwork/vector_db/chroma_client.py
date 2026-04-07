import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)

# Инициализация клиента ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db",  # папка для хранения данных
    settings=Settings(anonymized_telemetry=False)
)

# Создаём или получаем коллекцию
def get_projects_collection():
    """Возвращает коллекцию проектов"""
    try:
        collection = chroma_client.get_collection("kwork_projects")
        logger.info("✅ Коллекция kwork_projects получена")
        return collection
    except:
        collection = chroma_client.create_collection(
            name="kwork_projects",
            metadata={"hnsw:space": "cosine"}  # косинусная близость
        )
        logger.info("✅ Коллекция kwork_projects создана")
        return collection


def get_all_vector_ids():
    """Возвращает список всех project_id, уже лежащих в векторной БД"""
    try:
        collection = get_projects_collection()
        results = collection.get()
        return results['ids']  # это список project_id
    except Exception as e:
        logger.error(f"Ошибка получения ID из векторной БД: {e}")
        return []