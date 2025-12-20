"""
Unified Report Generator - Generates professional reports from analysis results.
"""

import os
import json
import argparse
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv

from utils.export_formats import ReportExporter
from config.prompts import REPORT_GENERATION_SYSTEM_PROMPT, REPORT_GENERATION_PROMPT
from utils.llm_client import get_llm_client

load_dotenv()


class ReportGenerator:
    """Generates professional reports from various analysis results."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.exporter = ReportExporter()
        self.llm = get_llm_client(llm_provider) if llm_provider else None
    
    def generate_report(
        self,
        analysis_results: Dict[str, Any],
        report_type: str = "executive",
        title: Optional[str] = None,
        use_ai_enhancement: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a professional report from analysis results.
        
        Args:
            analysis_results: Results from any analyzer (problem, strategy, transformation, etc.)
            report_type: Type of report (executive, detailed, presentation)
            title: Optional custom title
            use_ai_enhancement: Whether to use AI to enhance the report
            
        Returns:
            Dictionary containing formatted report
        """
        # Determine report type from analysis results
        if not title:
            title = self._determine_title(analysis_results)
        
        # Extract key information
        executive_summary = self._extract_executive_summary(analysis_results)
        sections = self._extract_sections(analysis_results)
        recommendations = self._extract_recommendations(analysis_results)
        
        # Enhance with AI if requested
        if use_ai_enhancement and self.llm:
            try:
                enhanced = self._enhance_with_ai(
                    executive_summary,
                    sections,
                    recommendations,
                    report_type
                )
                executive_summary = enhanced.get("executive_summary", executive_summary)
                sections = enhanced.get("sections", sections)
                recommendations = enhanced.get("recommendations", recommendations)
            except Exception as e:
                print(f"Warning: AI enhancement failed: {e}")
        
        report = {
            "title": title,
            "report_type": report_type,
            "executive_summary": executive_summary,
            "sections": sections,
            "recommendations": recommendations,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "source": analysis_results.get("metadata", {})
            }
        }
        
        return report
    
    def export_report(
        self,
        report: Dict[str, Any],
        format: str = "pdf",
        filename: Optional[str] = None
    ) -> str:
        """
        Export report in specified format.
        
        Args:
            report: Report data from generate_report()
            format: Export format (pdf, pptx, docx, json)
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return self.exporter.export(report, filename, format)
    
    def generate_from_file(
        self,
        input_file: str,
        format: str = "pdf",
        report_type: str = "executive",
        use_ai_enhancement: bool = True
    ) -> str:
        """
        Generate and export report from JSON file.
        
        Args:
            input_file: Path to JSON file with analysis results
            format: Export format
            report_type: Type of report
            use_ai_enhancement: Whether to use AI enhancement
            
        Returns:
            Path to exported file
        """
        with open(input_file, 'r') as f:
            analysis_results = json.load(f)
        
        report = self.generate_report(
            analysis_results=analysis_results,
            report_type=report_type,
            use_ai_enhancement=use_ai_enhancement
        )
        
        filename = os.path.splitext(os.path.basename(input_file))[0]
        return self.export_report(report, format=format, filename=filename)
    
    def _determine_title(self, analysis_results: Dict[str, Any]) -> str:
        """Determine report title from analysis results."""
        if "strategies" in analysis_results:
            return "Strategic Recommendations Report"
        elif "transformation_roadmap" in analysis_results:
            return "Transformation Plan Report"
        elif "optimization_opportunities" in analysis_results:
            return "Operations Optimization Report"
        elif "ai_adoption_roadmap" in analysis_results:
            return "AI Adoption Strategy Report"
        elif "problem_statement" in analysis_results:
            return "Problem Analysis Report"
        else:
            return "Business Analysis Report"
    
    def _extract_executive_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Extract or create executive summary."""
        if "executive_summary" in analysis_results:
            return str(analysis_results["executive_summary"])
        
        # Create summary from available data
        summary_parts = []
        
        if "problem_statement" in analysis_results:
            summary_parts.append(f"Problem: {analysis_results['problem_statement']}")
        
        if "strategies" in analysis_results:
            num_strategies = len(analysis_results["strategies"]) if isinstance(analysis_results["strategies"], list) else 1
            summary_parts.append(f"This report presents {num_strategies} strategic options.")
        
        if "key_findings" in analysis_results:
            summary_parts.append(f"Key Findings: {analysis_results['key_findings']}")
        
        if summary_parts:
            return " ".join(summary_parts)
        else:
            return "This report provides comprehensive analysis and recommendations based on the provided data."
    
    def _extract_sections(self, analysis_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract sections from analysis results."""
        sections = []
        
        # Common section keys
        section_keys = [
            "current_state_assessment",
            "target_state_vision",
            "transformation_roadmap",
            "technology_recommendations",
            "optimization_opportunities",
            "use_cases",
            "ai_adoption_roadmap",
            "root_causes",
            "stakeholders",
            "gap_analysis"
        ]
        
        for key in section_keys:
            if key in analysis_results:
                title = key.replace("_", " ").title()
                content = str(analysis_results[key])
                sections.append({"title": title, "content": content})
        
        # Handle strategies
        if "strategies" in analysis_results:
            strategies = analysis_results["strategies"]
            if isinstance(strategies, list):
                for i, strategy in enumerate(strategies, 1):
                    if isinstance(strategy, dict):
                        title = strategy.get("name", f"Strategy Option {i}")
                        content = strategy.get("description", "")
                        if "roadmap" in strategy:
                            content += f"\n\nRoadmap: {strategy['roadmap']}"
                    else:
                        title = f"Strategy Option {i}"
                        content = str(strategy)
                    sections.append({"title": title, "content": content})
        
        return sections
    
    def _extract_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Extract recommendations from analysis results."""
        recommendations = []
        
        if "recommendations" in analysis_results:
            recs = analysis_results["recommendations"]
            if isinstance(recs, list):
                recommendations.extend(recs)
            else:
                recommendations.append(str(recs))
        
        # Extract from strategies
        if "strategies" in analysis_results:
            strategies = analysis_results["strategies"]
            if isinstance(strategies, list):
                for strategy in strategies:
                    if isinstance(strategy, dict):
                        if "key_objectives" in strategy:
                            obj = strategy["key_objectives"]
                            if isinstance(obj, list):
                                recommendations.extend([f"Strategy: {o}" for o in obj])
                            else:
                                recommendations.append(f"Strategy: {obj}")
        
        # Extract from use cases
        if "use_cases" in analysis_results:
            use_cases = analysis_results["use_cases"]
            if isinstance(use_cases, list):
                for uc in use_cases[:5]:  # Top 5
                    if isinstance(uc, dict):
                        name = uc.get("name", "Use Case")
                        recommendations.append(f"Prioritize AI Use Case: {name}")
        
        return recommendations if recommendations else ["Review the full report for detailed recommendations."]
    
    def _enhance_with_ai(
        self,
        executive_summary: str,
        sections: List[Dict[str, str]],
        recommendations: List[str],
        report_type: str
    ) -> Dict[str, Any]:
        """Enhance report with AI."""
        if not self.llm:
            return {
                "executive_summary": executive_summary,
                "sections": sections,
                "recommendations": recommendations
            }
        
        analysis_text = json.dumps({
            "executive_summary": executive_summary,
            "sections": sections,
            "recommendations": recommendations
        }, indent=2)
        
        prompt = REPORT_GENERATION_PROMPT.format(analysis_results=analysis_text)
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=REPORT_GENERATION_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=3000
            )
            
            # Try to parse enhanced report
            try:
                enhanced = json.loads(response)
                return enhanced
            except json.JSONDecodeError:
                # If not JSON, return original
                return {
                    "executive_summary": executive_summary,
                    "sections": sections,
                    "recommendations": recommendations
                }
        except Exception:
            return {
                "executive_summary": executive_summary,
                "sections": sections,
                "recommendations": recommendations
            }


def main():
    """CLI interface for report generator."""
    parser = argparse.ArgumentParser(description="Generate professional reports")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input JSON file with analysis results"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="pdf",
        choices=["pdf", "pptx", "docx", "json"],
        help="Export format (default: pdf)"
    )
    parser.add_argument(
        "--report-type",
        type=str,
        default="executive",
        choices=["executive", "detailed", "presentation"],
        help="Report type (default: executive)"
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Custom report title"
    )
    parser.add_argument(
        "--no-ai-enhancement",
        action="store_true",
        help="Disable AI enhancement"
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "anthropic", "ollama"],
        help="LLM provider for AI enhancement"
    )
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}")
        return
    
    # Initialize generator
    generator = ReportGenerator(llm_provider=args.provider)
    
    # Generate and export report
    export_path = generator.generate_from_file(
        input_file=args.input,
        format=args.format,
        report_type=args.report_type,
        use_ai_enhancement=not args.no_ai_enhancement
    )
    
    print(f"Report exported to {export_path}")


if __name__ == "__main__":
    main()

