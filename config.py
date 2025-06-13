"""
Configuration settings for the Email Processor AI project.
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Default to provided key
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")

# Google Sheets Configuration
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
SHEET_NAMES = {
    "products": "products",
    "emails": "emails",
    "email_classification": "email-classification",
    "order_status": "order-status",
    "order_response": "order-response",
    "inquiry_response": "inquiry-response"
}

# Model Configuration
MODEL_NAME = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-ada-002"

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = PROJECT_ROOT / "email_processor.log" 