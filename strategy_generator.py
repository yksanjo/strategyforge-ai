"""
Strategy Generator - Generates multi-option strategic recommendations with implementation roadmaps.
"""

import os
import json
import argparse
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv

from utils.llm_client import get_llm_client
from utils.export_formats import ReportExporter
from config.prompts import STRATEGY_GENERATION_SYSTEM_PROMPT, STRATEGY_GENERATION_PROMPT

load_dotenv()


class StrategyGenerator:
    """Generates strategic recommendations and implementation roadmaps."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.llm = get_llm_client(llm_provider)
        self.exporter = ReportExporter()
    
    def generate(
        self,
        problem_analysis: Dict[str, Any],
        num_options: int = 3,
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate strategic recommendations.
        
        Args:
            problem_analysis: Problem analysis from ProblemAnalyzer
            num_options: Number of strategic options to generate (default: 3)
            focus_areas: Optional list of focus areas (e.g., ['cost-reduction', 'digital-transformation'])
            
        Returns:
            Dictionary containing strategic options and recommendations
        """
        # Prepare problem analysis text
        if isinstance(problem_analysis, dict):
            analysis_text = json.dumps(problem_analysis, indent=2)
        else:
            analysis_text = str(problem_analysis)
        
        # Build prompt
        prompt = STRATEGY_GENERATION_PROMPT.format(
            problem_analysis=analysis_text,
            num_options=num_options
        )
        
        if focus_areas:
            prompt += f"\n\nFocus on these areas: {', '.join(focus_areas)}"
        
        try:
            # Generate strategies
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=STRATEGY_GENERATION_SYSTEM_PROMPT,
                temperature=0.8,
                max_tokens=4000
            )
            
            # Try to parse as JSON
            try:
                strategies = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, create structured response
                strategies = {
                    "raw_strategies": response,
                    "num_options": num_options,
                    "problem_analysis": problem_analysis
                }
            
            # Ensure it's a list of strategies
            if isinstance(strategies, dict) and "strategies" in strategies:
                strategy_list = strategies["strategies"]
            elif isinstance(strategies, list):
                strategy_list = strategies
            else:
                strategy_list = [strategies]
            
            result = {
                "strategies": strategy_list,
                "num_options": len(strategy_list),
                "problem_analysis_summary": {
                    "problem": problem_analysis.get("problem_statement", "Unknown"),
                    "industry": problem_analysis.get("industry", "Unknown"),
                    "company_size": problem_analysis.get("company_size", "Unknown")
                },
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "provider": self.llm.provider.value,
                    "model": self.llm.model
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "problem_analysis": problem_analysis
            }
    
    def generate_from_problem(
        self,
        problem_description: str,
        num_options: int = 3,
        industry: Optional[str] = None,
        company_size: Optional[str] = None,
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate strategies directly from problem description.
        
        Args:
            problem_description: Description of the business problem
            num_options: Number of strategic options
            industry: Industry sector
            company_size: Company size
            focus_areas: Optional focus areas
            
        Returns:
            Dictionary containing strategic options
        """
        from problem_analyzer import ProblemAnalyzer
        
        # First analyze the problem
        analyzer = ProblemAnalyzer()
        problem_analysis = analyzer.analyze(
            problem_description=problem_description,
            industry=industry,
            company_size=company_size
        )
        
        # Then generate strategies
        return self.generate(
            problem_analysis=problem_analysis,
            num_options=num_options,
            focus_areas=focus_areas
        )
    
    def export_strategy_report(
        self,
        strategies: Dict[str, Any],
        format: str = "pdf",
        filename: Optional[str] = None
    ) -> str:
        """
        Export strategy report in specified format.
        
        Args:
            strategies: Strategy data from generate()
            format: Export format (pdf, pptx, docx, json)
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            filename = f"strategy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare report content
        report_content = {
            "title": "Strategic Recommendations Report",
            "executive_summary": self._create_executive_summary(strategies),
            "sections": self._create_report_sections(strategies),
            "recommendations": self._extract_recommendations(strategies)
        }
        
        return self.exporter.export(report_content, filename, format)
    
    def _create_executive_summary(self, strategies: Dict[str, Any]) -> str:
        """Create executive summary from strategies."""
        num_strategies = strategies.get("num_options", 0)
        problem = strategies.get("problem_analysis_summary", {}).get("problem", "business challenge")
        
        summary = f"This report presents {num_strategies} strategic options to address: {problem}. "
        summary += "Each option has been evaluated for feasibility, impact, and resource requirements. "
        summary += "Recommendations are prioritized based on expected outcomes and implementation complexity."
        
        return summary
    
    def _create_report_sections(self, strategies: Dict[str, Any]) -> List[Dict[str, str]]:
        """Create report sections from strategies."""
        sections = []
        strategy_list = strategies.get("strategies", [])
        
        for i, strategy in enumerate(strategy_list, 1):
            if isinstance(strategy, dict):
                title = strategy.get("name", f"Strategy Option {i}")
                content = strategy.get("description", "")
                if "roadmap" in strategy:
                    content += f"\n\nImplementation Roadmap:\n{strategy['roadmap']}"
                if "expected_outcomes" in strategy:
                    content += f"\n\nExpected Outcomes:\n{strategy['expected_outcomes']}"
            else:
                title = f"Strategy Option {i}"
                content = str(strategy)
            
            sections.append({
                "title": title,
                "content": content
            })
        
        return sections
    
    def _extract_recommendations(self, strategies: Dict[str, Any]) -> List[str]:
        """Extract recommendations from strategies."""
        recommendations = []
        strategy_list = strategies.get("strategies", [])
        
        for strategy in strategy_list:
            if isinstance(strategy, dict):
                name = strategy.get("name", "Strategy")
                key_objectives = strategy.get("key_objectives", [])
                if key_objectives:
                    if isinstance(key_objectives, list):
                        for obj in key_objectives:
                            recommendations.append(f"{name}: {obj}")
                    else:
                        recommendations.append(f"{name}: {key_objectives}")
        
        return recommendations if recommendations else ["Review all strategic options for detailed recommendations."]


def main():
    """CLI interface for strategy generator."""
    parser = argparse.ArgumentParser(description="Generate strategic recommendations")
    parser.add_argument(
        "--problem-id",
        type=str,
        help="Problem analysis ID or path to problem analysis JSON file"
    )
    parser.add_argument(
        "--problem",
        type=str,
        help="Problem description (alternative to --problem-id)"
    )
    parser.add_argument(
        "--options",
        type=int,
        default=3,
        help="Number of strategic options to generate (default: 3)"
    )
    parser.add_argument(
        "--industry",
        type=str,
        help="Industry sector"
    )
    parser.add_argument(
        "--company-size",
        type=str,
        help="Company size"
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
    
    if not args.problem_id and not args.problem:
        print("Error: Either --problem-id or --problem is required")
        return
    
    # Initialize generator
    generator = StrategyGenerator(llm_provider=args.provider)
    
    # Load or analyze problem
    if args.problem_id:
        if os.path.isfile(args.problem_id):
            with open(args.problem_id, 'r') as f:
                problem_analysis = json.load(f)
        else:
            print(f"Error: Problem analysis file not found: {args.problem_id}")
            return
    else:
        # Generate from problem description
        result = generator.generate_from_problem(
            problem_description=args.problem,
            num_options=args.options,
            industry=args.industry,
            company_size=args.company_size
        )
        
        # Output results
        if args.export:
            export_path = generator.export_strategy_report(result, format=args.export)
            print(f"Report exported to {export_path}")
        elif args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Strategies saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, default=str))
        return
    
    # Generate strategies
    result = generator.generate(
        problem_analysis=problem_analysis,
        num_options=args.options
    )
    
    # Output results
    if args.export:
        export_path = generator.export_strategy_report(result, format=args.export)
        print(f"Report exported to {export_path}")
    elif args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Strategies saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

