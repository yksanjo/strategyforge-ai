"""
Data processing utilities for handling various input formats.
"""

import pandas as pd
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import PyPDF2
from docx import Document


class DataProcessor:
    """Process various data formats for analysis."""
    
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Load CSV file into DataFrame."""
        return pd.read_csv(file_path)
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """Load JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    @staticmethod
    def process_document(file_path: str) -> str:
        """Process document and extract text based on file extension."""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return DataProcessor.extract_text_from_pdf(file_path)
        elif extension == '.docx':
            return DataProcessor.extract_text_from_docx(file_path)
        elif extension == '.txt':
            with open(file_path, 'r') as f:
                return f.read()
        elif extension == '.json':
            data = DataProcessor.load_json(file_path)
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    @staticmethod
    def summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for a DataFrame."""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "summary_stats": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
            "null_counts": df.isnull().sum().to_dict(),
            "sample_rows": df.head(5).to_dict('records')
        }
    
    @staticmethod
    def extract_key_metrics(data: Any) -> Dict[str, Any]:
        """Extract key metrics from various data formats."""
        if isinstance(data, pd.DataFrame):
            return DataProcessor.summarize_dataframe(data)
        elif isinstance(data, dict):
            return {
                "keys": list(data.keys()),
                "size": len(data),
                "sample": {k: str(v)[:100] for k, v in list(data.items())[:5]}
            }
        elif isinstance(data, list):
            return {
                "length": len(data),
                "sample": data[:5] if len(data) > 0 else []
            }
        else:
            return {"type": type(data).__name__, "value": str(data)[:200]}

