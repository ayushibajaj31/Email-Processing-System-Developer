"""
Email classification module for categorizing emails as order requests or product inquiries.
"""
from typing import Dict, Any
import pandas as pd
from openai import OpenAI

from ..config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class EmailClassifier:
    """Classifies emails as order requests or product inquiries."""
    
    def __init__(self):
        """Initialize the classifier with OpenAI client."""
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
    
    def classify_email(self, email_subject: str, email_body: str) -> str:
        """
        Classify an email as either an order request or product inquiry.
        
        Args:
            email_subject (str): Email subject
            email_body (str): Email body
            
        Returns:
            str: Classification result ("order_request" or "product_inquiry")
        """
        try:
            prompt = f"""
            Analyze the following email and classify it as either an "order_request" or "product_inquiry".
            An order request is when the customer wants to purchase products.
            A product inquiry is when the customer is asking for information about products.
            
            Email Subject: {email_subject}
            Email Body: {email_body}
            
            Classification (respond with exactly one of: "order_request" or "product_inquiry"):
            """
            
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an email classification assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Low temperature for more consistent results
            )
            
            classification = response.choices[0].message.content.strip().lower()
            if classification not in ["order_request", "product_inquiry"]:
                logger.warning(f"Unexpected classification: {classification}")
                classification = "product_inquiry"  # Default to product inquiry if uncertain
                
            return classification
            
        except Exception as e:
            logger.error(f"Error classifying email: {str(e)}")
            raise
    
    def process_emails(self, emails_df: pd.DataFrame) -> pd.DataFrame:
        """
        Process all emails and create classification results.
        
        Args:
            emails_df (pd.DataFrame): DataFrame containing emails
            
        Returns:
            pd.DataFrame: DataFrame with email classifications
        """
        try:
            results = []
            for _, row in emails_df.iterrows():
                classification = self.classify_email(row["subject"], row["body"])
                results.append({
                    "email_id": row["email_id"],
                    "category": classification
                })
            
            return pd.DataFrame(results)
            
        except Exception as e:
            logger.error(f"Error processing emails: {str(e)}")
            raise 