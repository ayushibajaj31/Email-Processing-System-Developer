"""
Order processing module for handling order requests and stock management.
"""
from typing import Dict, Any, List, Tuple
import pandas as pd
from openai import OpenAI

from ..config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class OrderProcessor:
    """Processes order requests and manages stock levels."""
    
    def __init__(self, products_df: pd.DataFrame):
        """
        Initialize the order processor with product data.
        
        Args:
            products_df (pd.DataFrame): DataFrame containing product information
        """
        self.products_df = products_df.copy()
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
    
    def extract_order_items(self, email_body: str) -> List[Dict[str, Any]]:
        """
        Extract order items from email body using LLM.
        
        Args:
            email_body (str): Email body containing order information
            
        Returns:
            List[Dict[str, Any]]: List of ordered items with quantities
        """
        try:
            prompt = f"""
            Extract the ordered items and their quantities from the following email.
            Return the information in JSON format with the following structure:
            [
                {{"product_name": "name", "quantity": number}},
                ...
            ]
            
            Email Body: {email_body}
            
            JSON response:
            """
            
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an order extraction assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            # Parse the JSON response
            import json
            items = json.loads(response.choices[0].message.content)
            return items
            
        except Exception as e:
            logger.error(f"Error extracting order items: {str(e)}")
            raise
    
    def process_order(self, email_id: str, email_body: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Process an order request and update stock levels.
        
        Args:
            email_id (str): ID of the email
            email_body (str): Email body containing order information
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: Order status and updated products data
        """
        try:
            # Extract order items
            order_items = self.extract_order_items(email_body)
            
            # Process each item
            order_status = []
            for item in order_items:
                product_name = item["product_name"]
                quantity = item["quantity"]
                
                # Find matching product
                product = self.products_df[
                    self.products_df["name"].str.lower() == product_name.lower()
                ]
                
                if product.empty:
                    logger.warning(f"Product not found: {product_name}")
                    continue
                
                product_id = product.iloc[0]["product_id"]
                current_stock = product.iloc[0]["stock"]
                
                # Check stock availability
                if current_stock >= quantity:
                    status = "created"
                    # Update stock
                    self.products_df.loc[
                        self.products_df["product_id"] == product_id,
                        "stock"
                    ] -= quantity
                else:
                    status = "out_of_stock"
                
                order_status.append({
                    "email_id": email_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "status": status
                })
            
            return pd.DataFrame(order_status), self.products_df
            
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")
            raise
    
    def generate_order_response(self, email_id: str, order_status: pd.DataFrame) -> str:
        """
        Generate a response email for the order.
        
        Args:
            email_id (str): ID of the email
            order_status (pd.DataFrame): DataFrame containing order status information
            
        Returns:
            str: Generated response email
        """
        try:
            # Prepare order summary
            order_summary = []
            for _, row in order_status.iterrows():
                product = self.products_df[
                    self.products_df["product_id"] == row["product_id"]
                ].iloc[0]
                
                status = "confirmed" if row["status"] == "created" else "out of stock"
                order_summary.append(
                    f"- {product['name']}: {row['quantity']} units ({status})"
                )
            
            prompt = f"""
            Generate a professional email response for the following order:
            
            Order Summary:
            {chr(10).join(order_summary)}
            
            Please include:
            1. A thank you message
            2. Confirmation of successful orders
            3. Information about out-of-stock items
            4. Next steps or alternatives for out-of-stock items
            5. A professional closing
            
            Response:
            """
            
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a professional customer service representative."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating order response: {str(e)}")
            raise 