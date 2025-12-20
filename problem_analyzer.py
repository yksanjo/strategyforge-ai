"""
Problem Analysis Engine - Analyzes business problems and identifies root causes.
"""

import os
import json
import argparse
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from utils.llm_client import get_llm_client, LLMProvider
from utils.data_processor import DataProcessor
from config.prompts import PROBLEM_ANALYSIS_SYSTEM_PROMPT, PROBLEM_ANALYSIS_PROMPT

load_dotenv()


class ProblemAnalyzer:
    """Analyzes business problems using AI."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.llm = get_llm_client(llm_provider)
        self.data_processor = DataProcessor()
    
    def analyze(
        self,
        problem_description: str,
        industry: Optional[str] = None,
        company_size: Optional[str] = None,
        additional_context: Optional[str] = None,
        document_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a business problem.
        
        Args:
            problem_description: Description of the business problem
            industry: Industry sector (e.g., 'financial-services', 'healthcare')
            company_size: Company size (e.g., 'startup', 'small', 'medium', 'large', 'enterprise')
            additional_context: Additional context about the problem
            document_path: Optional path to document with additional information
            
        Returns:
            Dictionary containing problem analysis
        """
        # Process document if provided
        document_text = ""
        if document_path:
            try:
                document_text = self.data_processor.process_document(document_path)
                if additional_context:
                    additional_context += f"\n\nDocument Content:\n{document_text}"
                else:
                    additional_context = f"Document Content:\n{document_text}"
            except Exception as e:
                print(f"Warning: Could not process document: {e}")
        
        # Build prompt
        prompt = PROBLEM_ANALYSIS_PROMPT.format(
            problem_description=problem_description,
            industry=industry or "not specified",
            company_size=company_size or "not specified",
            additional_context=additional_context or "none"
        )
        
        # Generate analysis
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=PROBLEM_ANALYSIS_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=3000
            )
            
            # Try to parse as JSON
            try:
                analysis = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, create structured response
                analysis = {
                    "raw_analysis": response,
                    "problem_statement": problem_description,
                    "industry": industry,
                    "company_size": company_size
                }
            
            # Add metadata
            analysis["metadata"] = {
                "analyzed_at": datetime.now().isoformat(),
                "provider": self.llm.provider.value,
                "model": self.llm.model
            }
            
            return analysis
            
        except Exception as e:
            return {
                "error": str(e),
                "problem_statement": problem_description,
                "industry": industry,
                "company_size": company_size
            }
    
    def analyze_from_file(
        self,
        file_path: str,
        industry: Optional[str] = None,
        company_size: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze problem from a file.
        
        Args:
            file_path: Path to file containing problem description
            industry: Industry sector
            company_size: Company size
            
        Returns:
            Dictionary containing problem analysis
        """
        try:
            text = self.data_processor.process_document(file_path)
            return self.analyze(
                problem_description=text,
                industry=industry,
                company_size=company_size
            )
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}


def main():
    """CLI interface for problem analyzer."""
    parser = argparse.ArgumentParser(description="Analyze business problems")
    parser.add_argument(
        "--input",
        type=str,
        help="Problem description or path to file"
    )
    parser.add_argument(
        "--industry",
        type=str,
        help="Industry sector"
    )
    parser.add_argument(
        "--company-size",
        type=str,
        choices=["startup", "small", "medium", "large", "enterprise"],
        help="Company size"
    )
    parser.add_argument(
        "--context",
        type=str,
        help="Additional context"
    )
    parser.add_argument(
        "--document",
        type=str,
        help="Path to document with additional information"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (JSON)"
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "anthropic", "ollama"],
        help="LLM provider to use"
    )
    
    args = parser.parse_args()
    
    if not args.input:
        print("Error: --input is required")
        return
    
    # Initialize analyzer
    analyzer = ProblemAnalyzer(llm_provider=args.provider)
    
    # Check if input is a file path
    if os.path.isfile(args.input):
        result = analyzer.analyze_from_file(
            file_path=args.input,
            industry=args.industry,
            company_size=args.company_size
        )
    else:
        result = analyzer.analyze(
            problem_description=args.input,
            industry=args.industry,
            company_size=args.company_size,
            additional_context=args.context,
            document_path=args.document
        )
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Analysis saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

