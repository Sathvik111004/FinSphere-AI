import os
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

# Global cache of embedding models to avoid reloading model binary on every operation
_embeddings = None

def get_embeddings_client():
    global _embeddings
    if _embeddings is not None:
        return _embeddings
        
    if settings.OPENAI_API_KEY:
        _embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    else:
        # High quality local embeddings, running purely offline on CPU/GPU
        # Model is light (all-MiniLM-L6-v2), loading fast and generating excellent vectors
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            encode_kwargs={'normalize_embeddings': True}
        )
    return _embeddings

class FinSphereVectorStore:
    def __init__(self):
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        # Configure ChromaDB client with persistent local folder storage
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.embeddings = get_embeddings_client()
        
    def get_vector_store(self, collection_name: str = "finsphere_collection") -> Chroma:
        """
        Creates/Retrieves LangChain vector store wrappers.
        """
        return Chroma(
            client=self.chroma_client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
        
    def delete_document_chunks(self, user_id: str, document_id: str):
        """
        Ensures strict tenant scoping by deleting all chunks matching specific owners and documents.
        """
        store = self.get_vector_store()
        try:
            store.delete(where={"$and": [{"user_id": user_id}, {"document_id": document_id}]})
        except Exception as e:
            # Silence error or log if collection doesn't exist yet
            pass

vector_store_client = FinSphereVectorStore()
