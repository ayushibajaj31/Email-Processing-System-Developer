"""
Inquiry handling module for processing product inquiries using RAG.
"""
from typing import Dict, Any, List
import pandas as pd
from openai import OpenAI

from ..config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from ..utils.logger import setup_logger
from .rag_utils import ProductVectorStore

logger = setup_logger(__name__)

class InquiryHandler:
    """Handles product inquiries using RAG techniques."""
    
    def __init__(self, products_df: pd.DataFrame):
        """
        Initialize the inquiry handler with product data.
        
        Args:
            products_df (pd.DataFrame): DataFrame containing product information
        """
        self.products_df = products_df
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
        self.vector_store = ProductVectorStore()
        self.vector_store.build_vector_store(products_df)
    
    def process_inquiry(self, email_id: str, email_body: str) -> str:
        """
        Process a product inquiry and generate a response.
        
        Args:
            email_id (str): ID of the email
            email_body (str): Email body containing the inquiry
            
        Returns:
            str: Generated response email
        """
        try:
            # Search for relevant products
            relevant_products = self.vector_store.search_products(email_body)
            
            if not relevant_products:
                return self._generate_no_products_response()
            
            # Generate response using the relevant products
            return self._generate_inquiry_response(email_body, relevant_products)
            
        except Exception as e:
            logger.error(f"Error processing inquiry: {str(e)}")
            raise
    
    def _generate_no_products_response(self) -> str:
        """
        Generate a response when no relevant products are found.
        
        Returns:
            str: Generated response email
        """
        prompt = """
        Generate a professional email response when no relevant products are found.
        The response should:
        1. Acknowledge the customer's inquiry
        2. Explain that we couldn't find exact matches
        3. Offer to help with a more specific search
        4. Provide contact information for further assistance
        
        Response:
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful customer service representative."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _generate_inquiry_response(
        self,
        inquiry: str,
        relevant_products: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a response using relevant product information.
        
        Args:
            inquiry (str): Customer's inquiry
            relevant_products (List[Dict[str, Any]]): List of relevant products
            
        Returns:
            str: Generated response email
        """
        # Prepare product information
        product_info = []
        for product in relevant_products:
            product_info.append(
                f"Product: {product['name']}\n"
                f"Category: {product['category']}\n"
                f"Season: {product['season']}\n"
                f"Stock: {product['stock']} units available"
            )
        
        prompt = f"""
        Generate a professional email response for the following product inquiry:
        
        Customer Inquiry:
        {inquiry}
        
        Relevant Products:
        {chr(10).join(product_info)}
        
        The response should:
        1. Address the specific inquiry
        2. Provide relevant product information
        3. Include stock availability
        4. Offer additional assistance
        5. Maintain a professional and helpful tone
        
        Response:
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a knowledgeable product specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content 