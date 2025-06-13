"""
Utility functions for reading from and writing to Google Sheets.
"""
import pandas as pd
from typing import Dict, Any

from ..config import SPREADSHEET_ID, SHEET_NAMES
from .logger import setup_logger

logger = setup_logger(__name__)

def read_sheet(sheet_name: str) -> pd.DataFrame:
    """
    Read data from a Google Sheet.
    
    Args:
        sheet_name (str): Name of the sheet to read
        
    Returns:
        pd.DataFrame: DataFrame containing the sheet data
    """
    try:
        export_link = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(export_link)
        logger.info(f"Successfully read sheet: {sheet_name}")
        return df
    except Exception as e:
        logger.error(f"Error reading sheet {sheet_name}: {str(e)}")
        raise

def write_sheet(df: pd.DataFrame, sheet_name: str) -> None:
    """
    Write data to a Google Sheet.
    
    Args:
        df (pd.DataFrame): DataFrame to write
        sheet_name (str): Name of the sheet to write to
    """
    try:
        # Note: In a production environment, you would use the Google Sheets API
        # to write directly to the sheet. For now, we'll save to CSV and provide
        # instructions for manual upload.
        output_path = f"outputs/{sheet_name}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully wrote data to {output_path}")
        logger.info(f"Please manually upload {output_path} to the Google Sheet: {sheet_name}")
    except Exception as e:
        logger.error(f"Error writing to sheet {sheet_name}: {str(e)}")
        raise

def get_all_sheets() -> Dict[str, pd.DataFrame]:
    """
    Read all required sheets from the Google Spreadsheet.
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping sheet names to DataFrames
    """
    sheets = {}
    for key, sheet_name in SHEET_NAMES.items():
        if key in ["products", "emails"]:  # Only read input sheets
            sheets[key] = read_sheet(sheet_name)
    return sheets 