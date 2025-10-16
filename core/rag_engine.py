"""
RAG Engine - Retrieval-Augmented Generation Implementation
"""

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from datetime import datetime

class RAGEngine:
    """RAG Engine for retrieving relevant documentation"""
    
    def __init__(self, 
                 collection_name: str = "programming_docs",
                 embedding_model: str = "all-MiniLM-L6-v2",
                 persist_directory: str = "./data/vector_db"):
        """Initialize RAG Engine"""
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        self._initialize_chromadb()
        
    def _initialize_chromadb(self):
        """Initialize ChromaDB client and collection"""
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False, allow_reset=True)
            )
            
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                print(f"Loaded existing collection: {self.collection_name}")
            except:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Programming documentation for RAG"}
                )
                print(f"Created new collection: {self.collection_name}")
                
        except Exception as e:
            print(f"Error initializing ChromaDB: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100):
        """Add documents to the vector database"""
        print(f"Adding {len(documents)} documents to vector database...")
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            texts = [doc['text'] for doc in batch]
            metadatas = [doc.get('metadata', {}) for doc in batch]
            
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True).tolist()
            
            ids = [f"doc_{i+j}_{datetime.now().timestamp()}" for j in range(len(batch))]
            
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        
        print("✅ All documents added successfully!")
    
    def retrieve(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        retrieved_docs = []
        for i in range(len(results['documents'][0])):
            doc = {
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i],
                'relevance': 1 - (results['distances'][0][i] / 2)
            }
            retrieved_docs.append(doc)
        
        return retrieved_docs
    
    def semantic_search(self, query: str, language: Optional[str] = None, 
                       n_results: int = 5) -> List[Dict[str, Any]]:
        """Semantic search with optional filters"""
        results = self.retrieve(query=query, n_results=n_results)
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database"""
        count = self.collection.count()
        
        return {
            'collection_name': self.collection_name,
            'document_count': count,
            'embedding_model': str(self.embedding_model),
            'persist_directory': self.persist_directory
        }


class DocumentChunker:
    """Utility class for chunking documents"""
    
    @staticmethod
    def chunk_by_paragraphs(text: str, max_length: int = 1000) -> List[str]:
        """Chunk text by paragraphs with max length"""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < max_length:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks