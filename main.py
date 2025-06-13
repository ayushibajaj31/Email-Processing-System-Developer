"""
Main application module for the Email Processor AI project.
"""
import pandas as pd
from typing import Dict, Any

from .config import SHEET_NAMES
from .utils.logger import setup_logger
from .utils.spreadsheet_io import get_all_sheets, write_sheet
from .modules.classifier import EmailClassifier
from .modules.order_processor import OrderProcessor
from .modules.inquiry_handler import InquiryHandler
from .modules.response_generator import ResponseGenerator

logger = setup_logger(__name__)

class EmailProcessor:
    """Main class for processing emails and generating responses."""
    
    def __init__(self):
        """Initialize the email processor with all required components."""
        # Load data
        self.data = get_all_sheets()
        self.products_df = self.data["products"]
        self.emails_df = self.data["emails"]
        
        # Initialize components
        self.classifier = EmailClassifier()
        self.order_processor = OrderProcessor(self.products_df)
        self.inquiry_handler = InquiryHandler(self.products_df)
        self.response_generator = ResponseGenerator()
    
    def process_emails(self) -> None:
        """Process all emails and generate responses."""
        try:
            # Step 1: Classify emails
            logger.info("Classifying emails...")
            classifications = self.classifier.process_emails(self.emails_df)
            write_sheet(classifications, SHEET_NAMES["email_classification"])
            
            # Step 2: Process orders and inquiries
            order_responses = []
            inquiry_responses = []
            
            for _, row in self.emails_df.iterrows():
                email_id = row["email_id"]
                email_body = row["body"]
                
                # Get classification for this email
                classification = classifications[
                    classifications["email_id"] == email_id
                ]["category"].iloc[0]
                
                if classification == "order_request":
                    # Process order
                    order_status, updated_products = self.order_processor.process_order(
                        email_id,
                        email_body
                    )
                    write_sheet(order_status, SHEET_NAMES["order_status"])
                    
                    # Generate order response
                    response_content = self.order_processor.generate_order_response(
                        email_id,
                        order_status
                    )
                    order_responses.append({
                        "email_id": email_id,
                        "content": response_content
                    })
                    
                else:  # product_inquiry
                    # Process inquiry
                    response_content = self.inquiry_handler.process_inquiry(
                        email_id,
                        email_body
                    )
                    inquiry_responses.append({
                        "email_id": email_id,
                        "content": response_content
                    })
            
            # Step 3: Generate and save responses
            if order_responses:
                order_response_df = self.response_generator.process_responses(
                    order_responses,
                    "order"
                )
                write_sheet(order_response_df, SHEET_NAMES["order_response"])
            
            if inquiry_responses:
                inquiry_response_df = self.response_generator.process_responses(
                    inquiry_responses,
                    "inquiry"
                )
                write_sheet(inquiry_response_df, SHEET_NAMES["inquiry_response"])
            
            logger.info("Email processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing emails: {str(e)}")
            raise

def main():
    """Main entry point for the application."""
    try:
        processor = EmailProcessor()
        processor.process_emails()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 