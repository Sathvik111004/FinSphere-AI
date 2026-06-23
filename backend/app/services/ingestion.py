import os
import uuid
import shutil
from typing import List, Tuple
from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from app.core.config import settings
from app.core.exceptions import IngestionError
from app.rag.vector_store import vector_store_client

class FinSphereIngestionService:
    def __init__(self):
        os.makedirs(settings.UPLOADS_DIRECTORY, exist_ok=True)
        # Financial context character splitter. Focuses on maintaining integrity of financial statements, balance sheets, and formulas.
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4",
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )

    def validate_file_header(self, file_path: str, file_ext: str) -> None:
        """
        Secure validation checking magic bytes header of the uploaded file to ensure it's not a renamed malicious script.
        """
        try:
            with open(file_path, "rb") as f:
                header = f.read(4)
                
            if file_ext == "pdf":
                if not header.startswith(b"%PDF"):
                    raise IngestionError("Corrupted or invalid PDF format. Magic header check failed.")
            elif file_ext == "csv":
                # Check if it has readable characters
                try:
                    header.decode("utf-8")
                except UnicodeDecodeError:
                    raise IngestionError("Corrupted or invalid CSV file character encoding.")
        except IngestionError:
            raise
        except Exception as e:
            raise IngestionError(f"Security validation error: {str(e)}")

    def process_and_index_document(self, upload_file: UploadFile, user_id: str) -> Tuple[str, str, int]:
        """
        Saves file securely, performs validation, splits document, generates embeddings and saves to Chroma DB.
        Returns:
            Tuple of (secure_saved_path, file_extension, size_bytes)
        """
        # Validate file format via simple extension allow-list
        orig_filename = upload_file.filename or "unknown"
        file_ext = orig_filename.split(".")[-1].lower() if "." in orig_filename else ""
        
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise IngestionError(f"Unsupported file type. Allowed: {settings.ALLOWED_EXTENSIONS}")
            
        # Secure filename generation to avoid directory traversal
        secure_filename = f"{uuid.uuid4()}.{file_ext}"
        save_path = os.path.abspath(os.path.join(settings.UPLOADS_DIRECTORY, secure_filename))
        
        # Enforce sandbox directory escape checks
        if not save_path.startswith(os.path.abspath(settings.UPLOADS_DIRECTORY)):
            raise IngestionError("Directory traversal path violation detected.")
            
        # Write bytes locally while checking size
        size_bytes = 0
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        
        try:
            with open(save_path, "wb") as buffer:
                # Read chunks to avoid memory starvation
                while chunk := upload_file.file.read(1024 * 1024):
                    size_bytes += len(chunk)
                    if size_bytes > max_bytes:
                        raise IngestionError(f"File size exceeds secure limits of {settings.MAX_FILE_SIZE_MB}MB.")
                    buffer.write(chunk)
        except IngestionError:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise
        except Exception as e:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise IngestionError(f"Error saving upload: {str(e)}")
            
        # Validate magic headers
        self.validate_file_header(save_path, file_ext)
        
        # Load and parse text
        documents: List[Document] = []
        try:
            if file_ext == "pdf":
                loader = PyPDFLoader(save_path)
                documents = loader.load()
            elif file_ext in ("csv", "txt"):
                with open(save_path, "r", encoding="utf-8") as f:
                    content = f.read()
                documents = [Document(page_content=content, metadata={"source": orig_filename})]
        except Exception as e:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise IngestionError(f"Failed to parse document content: {str(e)}")
            
        if not documents:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise IngestionError("No text content could be extracted from this document.")
            
        # Generate dynamic UUID for document ID tracking
        doc_id = str(uuid.uuid4())
        
        # Segment text into vector-friendly blocks
        chunks = self.text_splitter.split_documents(documents)
        
        # Append security scoping metadata to every chunk
        for chunk in chunks:
            chunk.metadata["user_id"] = user_id
            chunk.metadata["document_id"] = doc_id
            chunk.metadata["source"] = orig_filename
            
        # Write vectors to Chroma DB
        try:
            vector_store = vector_store_client.get_vector_store()
            vector_store.add_documents(chunks)
        except Exception as e:
            if os.path.exists(save_path):
                os.remove(save_path)
            raise IngestionError(f"Failed to write vector indexes to Chroma DB: {str(e)}")
            
        return save_path, doc_id, size_bytes

ingestion_service = FinSphereIngestionService()
