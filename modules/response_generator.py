"""
Response generator module for formatting and managing email responses.
"""
from typing import Dict, Any, List
import pandas as pd
from openai import OpenAI

from ..config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ResponseGenerator:
    """Generates and formats email responses."""
    
    def __init__(self):
        """Initialize the response generator with OpenAI client."""
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )
    
    def format_response(
        self,
        email_id: str,
        response_content: str,
        response_type: str
    ) -> Dict[str, Any]:
        """
        Format an email response with proper structure and tone.
        
        Args:
            email_id (str): ID of the email being responded to
            response_content (str): Main content of the response
            response_type (str): Type of response ("order" or "inquiry")
            
        Returns:
            Dict[str, Any]: Formatted response with metadata
        """
        try:
            # Generate email subject
            subject = self._generate_subject(response_type)
            
            # Format the response
            formatted_response = self._format_email(
                subject=subject,
                content=response_content,
                response_type=response_type
            )
            
            return {
                "email_id": email_id,
                "response": formatted_response
            }
            
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            raise
    
    def _generate_subject(self, response_type: str) -> str:
        """
        Generate an appropriate email subject.
        
        Args:
            response_type (str): Type of response ("order" or "inquiry")
            
        Returns:
            str: Generated email subject
        """
        if response_type == "order":
            return "Re: Your Order Confirmation"
        else:
            return "Re: Your Product Inquiry"
    
    def _format_email(
        self,
        subject: str,
        content: str,
        response_type: str
    ) -> str:
        """
        Format the email with proper structure and tone.
        
        Args:
            subject (str): Email subject
            content (str): Main content of the response
            response_type (str): Type of response ("order" or "inquiry")
            
        Returns:
            str: Formatted email
        """
        prompt = f"""
        Format the following email response with proper structure and tone.
        The response should be professional, clear, and well-organized.
        
        Subject: {subject}
        Content: {content}
        
        Please format the email with:
        1. A professional greeting
        2. Clear paragraphs
        3. Proper spacing
        4. A professional signature
        5. Contact information
        
        Formatted email:
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an email formatting assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def process_responses(
        self,
        responses: List[Dict[str, Any]],
        response_type: str
    ) -> pd.DataFrame:
        """
        Process multiple responses and create a DataFrame.
        
        Args:
            responses (List[Dict[str, Any]]): List of response data
            response_type (str): Type of responses ("order" or "inquiry")
            
        Returns:
            pd.DataFrame: DataFrame containing formatted responses
        """
        try:
            formatted_responses = []
            for response in responses:
                formatted_response = self.format_response(
                    email_id=response["email_id"],
                    response_content=response["content"],
                    response_type=response_type
                )
                formatted_responses.append(formatted_response)
            
            return pd.DataFrame(formatted_responses)
            
        except Exception as e:
            logger.error(f"Error processing responses: {str(e)}")
            raise 