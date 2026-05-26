import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.exceptions import IngestionError, PermissionDeniedError
from app.services.ingestion import ingestion_service
from app.rag.vector_store import vector_store_client
from app.database.connection import get_db
from app.database.models import User, DocumentMetadata
from app.api.deps import get_current_user

router = APIRouter()

class DocumentResponse(BaseModel):
    id: str
    filename: str
    document_type: str
    size_bytes: int
    ingestion_status: str
    created_at: str

    class Config:
        from_attributes = True

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("annual_report"), # annual_report, SEC_filing, transcript
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and index financial documents securely.
    Supports PDF, CSV, TXT parsing and Chroma DB embeddings write.
    """
    try:
        # Ingest and write vector store
        saved_path, doc_uuid, size_bytes = ingestion_service.process_and_index_document(
            file, current_user.id
        )
    except IngestionError as e:
        raise e
    except Exception as e:
        raise IngestionError(f"Upload ingestion process failed: {str(e)}")
        
    # Write SQL metadata record
    doc_meta = DocumentMetadata(
        id=doc_uuid,
        user_id=current_user.id,
        filename=file.filename or "unknown",
        file_path=saved_path,
        document_type=document_type,
        size_bytes=size_bytes,
        ingestion_status="success"
    )
    
    db.add(doc_meta)
    db.commit()
    db.refresh(doc_meta)
    
    # Cast created_at datetime to standard ISO string format
    return {
        "id": doc_meta.id,
        "filename": doc_meta.filename,
        "document_type": doc_meta.document_type,
        "size_bytes": doc_meta.size_bytes,
        "ingestion_status": doc_meta.ingestion_status,
        "created_at": doc_meta.created_at.isoformat()
    }

@router.get("/", response_model=List[DocumentResponse])
def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    List all uploaded documents and indices owned by the current user.
    """
    docs = db.query(DocumentMetadata).filter(DocumentMetadata.user_id == current_user.id).all()
    res = []
    for d in docs:
        res.append({
            "id": d.id,
            "filename": d.filename,
            "document_type": d.document_type,
            "size_bytes": d.size_bytes,
            "ingestion_status": d.ingestion_status,
            "created_at": d.created_at.isoformat()
        })
    return res

@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes the document: removes raw disk files, SQL records, and Chroma vector chunks.
    """
    doc = db.query(DocumentMetadata).filter(DocumentMetadata.id == document_id).first()
    if not doc:
        raise IngestionError("Document indices not found.")
        
    if doc.user_id != current_user.id:
        raise PermissionDeniedError("Ownership access violation. Cannot delete metadata indices.")
        
    # Delete file from local uploads storage
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception as e:
            pass
            
    # Delete vector embeddings from ChromaDB matching user scope
    vector_store_client.delete_document_chunks(current_user.id, document_id)
    
    # Delete database record
    db.delete(doc)
    db.commit()
    
    return {"status": "success", "message": "Document file and corresponding vector indexes deleted."}
