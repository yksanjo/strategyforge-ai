"""
Operations Optimizer - Business process optimization and resource allocation.
Competes with Accenture's SynOps platform.
"""

import os
import json
import argparse
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

from utils.llm_client import get_llm_client
from utils.data_processor import DataProcessor
from utils.export_formats import ReportExporter
from config.prompts import OPERATIONS_OPTIMIZATION_SYSTEM_PROMPT, OPERATIONS_OPTIMIZATION_PROMPT

load_dotenv()


class OperationsOptimizer:
    """Optimizes business operations and processes."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.llm = get_llm_client(llm_provider)
        self.data_processor = DataProcessor()
        self.exporter = ReportExporter()
    
    def optimize(
        self,
        operations_summary: str,
        metrics: Optional[Dict[str, Any]] = None,
        challenges: Optional[List[str]] = None,
        data_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize operations.
        
        Args:
            operations_summary: Summary of current operations
            metrics: Key performance metrics
            challenges: List of current challenges
            data_file: Optional path to CSV/data file with operations data
            
        Returns:
            Dictionary containing optimization recommendations
        """
        # Process data file if provided
        data_summary = ""
        if data_file:
            try:
                df = self.data_processor.load_csv(data_file)
                summary = self.data_processor.summarize_dataframe(df)
                data_summary = json.dumps(summary, indent=2)
                if operations_summary:
                    operations_summary += f"\n\nData Analysis:\n{data_summary}"
                else:
                    operations_summary = f"Data Analysis:\n{data_summary}"
            except Exception as e:
                print(f"Warning: Could not process data file: {e}")
        
        # Prepare metrics text
        metrics_text = json.dumps(metrics, indent=2) if metrics else "not provided"
        
        # Prepare challenges text
        challenges_text = "\n".join(challenges) if challenges else "not specified"
        
        # Build prompt
        prompt = OPERATIONS_OPTIMIZATION_PROMPT.format(
            operations_summary=operations_summary,
            metrics=metrics_text,
            challenges=challenges_text
        )
        
        try:
            # Generate optimization recommendations
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=OPERATIONS_OPTIMIZATION_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=4000
            )
            
            # Try to parse as JSON
            try:
                optimization = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, create structured response
                optimization = {
                    "raw_recommendations": response,
                    "operations_summary": operations_summary,
                    "metrics": metrics
                }
            
            # Add metadata
            optimization["metadata"] = {
                "optimized_at": datetime.now().isoformat(),
                "provider": self.llm.provider.value,
                "model": self.llm.model
            }
            
            return optimization
            
        except Exception as e:
            return {
                "error": str(e),
                "operations_summary": operations_summary
            }
    
    def optimize_from_file(
        self,
        data_file: str,
        operations_summary: Optional[str] = None,
        challenges: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Optimize operations from data file.
        
        Args:
            data_file: Path to CSV/data file
            operations_summary: Optional operations summary
            challenges: Optional list of challenges
            
        Returns:
            Dictionary containing optimization recommendations
        """
        try:
            df = self.data_processor.load_csv(data_file)
            summary = self.data_processor.summarize_dataframe(df)
            
            if not operations_summary:
                operations_summary = f"Operations data from {data_file}"
            
            return self.optimize(
                operations_summary=operations_summary,
                metrics=summary,
                challenges=challenges,
                data_file=data_file
            )
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}
    
    def export_optimization_report(
        self,
        optimization: Dict[str, Any],
        format: str = "pdf",
        filename: Optional[str] = None
    ) -> str:
        """
        Export optimization report in specified format.
        
        Args:
            optimization: Optimization data
            format: Export format (pdf, pptx, docx, json)
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            filename = f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare report content
        report_content = {
            "title": "Operations Optimization Report",
            "executive_summary": self._create_executive_summary(optimization),
            "sections": self._create_report_sections(optimization),
            "recommendations": self._extract_recommendations(optimization)
        }
        
        return self.exporter.export(report_content, filename, format)
    
    def _create_executive_summary(self, optimization: Dict[str, Any]) -> str:
        """Create executive summary from optimization."""
        summary = "This report provides comprehensive operations optimization recommendations. "
        summary += "Key focus areas include process improvements, resource allocation, and performance enhancement. "
        summary += "All recommendations are prioritized based on expected impact and implementation feasibility."
        
        return summary
    
    def _create_report_sections(self, optimization: Dict[str, Any]) -> List[Dict[str, str]]:
        """Create report sections from optimization."""
        sections = []
        
        if "current_state_analysis" in optimization:
            sections.append({
                "title": "Current State Analysis",
                "content": str(optimization["current_state_analysis"])
            })
        
        if "identified_inefficiencies" in optimization:
            sections.append({
                "title": "Identified Inefficiencies",
                "content": str(optimization["identified_inefficiencies"])
            })
        
        if "optimization_opportunities" in optimization:
            sections.append({
                "title": "Optimization Opportunities",
                "content": str(optimization["optimization_opportunities"])
            })
        
        if "process_improvements" in optimization:
            sections.append({
                "title": "Process Improvements",
                "content": str(optimization["process_improvements"])
            })
        
        if "resource_reallocation" in optimization:
            sections.append({
                "title": "Resource Reallocation Suggestions",
                "content": str(optimization["resource_reallocation"])
            })
        
        if "expected_improvements" in optimization:
            sections.append({
                "title": "Expected Improvements",
                "content": str(optimization["expected_improvements"])
            })
        
        return sections
    
    def _extract_recommendations(self, optimization: Dict[str, Any]) -> List[str]:
        """Extract recommendations from optimization."""
        recommendations = []
        
        if "recommended_improvements" in optimization:
            recs = optimization["recommended_improvements"]
            if isinstance(recs, list):
                recommendations.extend(recs)
            else:
                recommendations.append(str(recs))
        
        if "optimization_opportunities" in optimization:
            opps = optimization["optimization_opportunities"]
            if isinstance(opps, list):
                recommendations.extend([f"Opportunity: {o}" for o in opps])
            elif isinstance(opps, dict):
                for key, value in opps.items():
                    recommendations.append(f"{key}: {value}")
            else:
                recommendations.append(str(opps))
        
        return recommendations if recommendations else ["Review the full optimization report for detailed recommendations."]


def main():
    """CLI interface for operations optimizer."""
    parser = argparse.ArgumentParser(description="Optimize business operations")
    parser.add_argument(
        "--input",
        type=str,
        help="Operations summary or path to data file"
    )
    parser.add_argument(
        "--summary",
        type=str,
        help="Operations summary (if input is a data file)"
    )
    parser.add_argument(
        "--challenges",
        type=str,
        nargs="+",
        help="List of current challenges"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        help="Path to JSON file with metrics"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (JSON)"
    )
    parser.add_argument(
        "--export",
        type=str,
        choices=["pdf", "pptx", "docx", "json"],
        help="Export format for report"
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
    
    # Initialize optimizer
    optimizer = OperationsOptimizer(llm_provider=args.provider)
    
    # Check if input is a file
    if os.path.isfile(args.input) and args.input.endswith('.csv'):
        result = optimizer.optimize_from_file(
            data_file=args.input,
            operations_summary=args.summary,
            challenges=args.challenges
        )
    else:
        # Load metrics if provided
        metrics = None
        if args.metrics and os.path.isfile(args.metrics):
            with open(args.metrics, 'r') as f:
                metrics = json.load(f)
        
        result = optimizer.optimize(
            operations_summary=args.input,
            metrics=metrics,
            challenges=args.challenges
        )
    
    # Output results
    if args.export:
        export_path = optimizer.export_optimization_report(result, format=args.export)
        print(f"Report exported to {export_path}")
    elif args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Optimization saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

