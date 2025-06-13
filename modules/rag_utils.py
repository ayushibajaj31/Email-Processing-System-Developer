"""
Utilities for Retrieval-Augmented Generation (RAG) operations.
"""
from typing import List, Dict, Any
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K_RESULTS
)
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ProductVectorStore:
    """Manages the vector store for product information."""
    
    def __init__(self):
        """Initialize the vector store with OpenAI embeddings."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_BASE_URL,
            model=EMBEDDING_MODEL
        )
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
    
    def create_documents(self, products_df: pd.DataFrame) -> List[Document]:
        """
        Create Document objects from product data.
        
        Args:
            products_df (pd.DataFrame): DataFrame containing product information
            
        Returns:
            List[Document]: List of Document objects
        """
        documents = []
        for _, row in products_df.iterrows():
            # Create a comprehensive text representation of the product
            text = f"""
            Product ID: {row['product_id']}
            Name: {row['name']}
            Category: {row['category']}
            Description: {row['description']}
            Season: {row['season']}
            Stock: {row['stock']}
            """
            documents.append(Document(
                page_content=text,
                metadata={
                    "product_id": row["product_id"],
                    "name": row["name"],
                    "category": row["category"],
                    "season": row["season"],
                    "stock": row["stock"]
                }
            ))
        return documents
    
    def build_vector_store(self, products_df: pd.DataFrame) -> None:
        """
        Build the vector store from product data.
        
        Args:
            products_df (pd.DataFrame): DataFrame containing product information
        """
        try:
            documents = self.create_documents(products_df)
            split_docs = self.text_splitter.split_documents(documents)
            self.vector_store = FAISS.from_documents(split_docs, self.embeddings)
            logger.info("Successfully built vector store")
        except Exception as e:
            logger.error(f"Error building vector store: {str(e)}")
            raise
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for relevant products using semantic similarity.
        
        Args:
            query (str): Search query
            
        Returns:
            List[Dict[str, Any]]: List of relevant products with their metadata
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call build_vector_store first.")
        
        try:
            docs = self.vector_store.similarity_search(query, k=TOP_K_RESULTS)
            results = []
            for doc in docs:
                results.append({
                    "product_id": doc.metadata["product_id"],
                    "name": doc.metadata["name"],
                    "category": doc.metadata["category"],
                    "season": doc.metadata["season"],
                    "stock": doc.metadata["stock"],
                    "relevance_score": doc.metadata.get("score", 0)
                })
            return results
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            raise 