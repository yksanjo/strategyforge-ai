"""
AI Strategy Advisor - AI adoption roadmaps and use case identification.
Competes with Accenture's "AI Navigator for Enterprise".
"""

import os
import json
import argparse
from typing import Dict, Any, Optional, List
from datetime import datetime
from dotenv import load_dotenv

from utils.llm_client import get_llm_client
from utils.export_formats import ReportExporter
from config.prompts import AI_STRATEGY_ADVISOR_SYSTEM_PROMPT, AI_STRATEGY_ADVISOR_PROMPT

load_dotenv()


class AIStrategyAdvisor:
    """Provides AI adoption strategy and roadmap guidance."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.llm = get_llm_client(llm_provider)
        self.exporter = ReportExporter()
    
    def advise(
        self,
        industry: str,
        company_size: str,
        budget: Optional[str] = None,
        ai_maturity: Optional[str] = None,
        challenges: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI adoption strategy.
        
        Args:
            industry: Industry sector
            company_size: Company size (startup, small, medium, large, enterprise)
            budget: Budget range for AI initiatives
            ai_maturity: Current AI maturity level (beginner, intermediate, advanced)
            challenges: List of key business challenges
            
        Returns:
            Dictionary containing AI strategy and roadmap
        """
        # Prepare challenges text
        challenges_text = "\n".join(challenges) if challenges else "general business improvement"
        
        # Build prompt
        prompt = AI_STRATEGY_ADVISOR_PROMPT.format(
            industry=industry,
            company_size=company_size,
            budget=budget or "not specified",
            ai_maturity=ai_maturity or "beginner",
            challenges=challenges_text
        )
        
        try:
            # Generate AI strategy
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=AI_STRATEGY_ADVISOR_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=4000
            )
            
            # Try to parse as JSON
            try:
                strategy = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, create structured response
                strategy = {
                    "raw_strategy": response,
                    "industry": industry,
                    "company_size": company_size,
                    "budget": budget
                }
            
            # Add metadata
            strategy["metadata"] = {
                "advised_at": datetime.now().isoformat(),
                "provider": self.llm.provider.value,
                "model": self.llm.model
            }
            
            return strategy
            
        except Exception as e:
            return {
                "error": str(e),
                "industry": industry,
                "company_size": company_size
            }
    
    def identify_use_cases(
        self,
        industry: str,
        business_functions: Optional[List[str]] = None,
        priority: str = "high_impact"
    ) -> Dict[str, Any]:
        """
        Identify high-value AI use cases.
        
        Args:
            industry: Industry sector
            business_functions: List of business functions to focus on
            priority: Priority focus (high_impact, quick_wins, cost_savings)
            
        Returns:
            Dictionary containing prioritized use cases
        """
        functions_text = ", ".join(business_functions) if business_functions else "all functions"
        
        prompt = f"""Identify high-value AI use cases for {industry} industry.

Business Functions: {functions_text}
Priority Focus: {priority}

For each use case, provide:
1. Use Case Name and Description
2. Business Value (quantified where possible)
3. Implementation Complexity (low/medium/high)
4. Expected ROI
5. Required Resources
6. Implementation Timeline

Format as JSON with an array of use cases."""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=AI_STRATEGY_ADVISOR_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=3000
            )
            
            try:
                use_cases = json.loads(response)
            except json.JSONDecodeError:
                use_cases = {
                    "raw_use_cases": response,
                    "industry": industry,
                    "priority": priority
                }
            
            return use_cases
            
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_roi(
        self,
        use_case: str,
        current_cost: Optional[float] = None,
        expected_savings: Optional[float] = None,
        implementation_cost: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate ROI for an AI use case.
        
        Args:
            use_case: Description of the AI use case
            current_cost: Current cost of the process/problem
            expected_savings: Expected savings from AI implementation
            implementation_cost: Cost to implement AI solution
            
        Returns:
            Dictionary containing ROI analysis
        """
        prompt = f"""Calculate ROI for the following AI use case:

Use Case: {use_case}
Current Cost: ${current_cost:,.2f} per year (if provided)
Expected Savings: ${expected_savings:,.2f} per year (if provided)
Implementation Cost: ${implementation_cost:,.2f} (if provided)

Provide detailed ROI analysis including:
1. Payback Period
2. Net Present Value (NPV)
3. Return on Investment (ROI %)
4. Break-even Analysis
5. Risk-Adjusted ROI

Format as JSON."""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=AI_STRATEGY_ADVISOR_SYSTEM_PROMPT,
                temperature=0.5,
                max_tokens=2000
            )
            
            try:
                roi_analysis = json.loads(response)
            except json.JSONDecodeError:
                roi_analysis = {
                    "raw_analysis": response,
                    "use_case": use_case
                }
            
            return roi_analysis
            
        except Exception as e:
            return {"error": str(e)}
    
    def export_strategy_report(
        self,
        strategy: Dict[str, Any],
        format: str = "pdf",
        filename: Optional[str] = None
    ) -> str:
        """
        Export AI strategy report in specified format.
        
        Args:
            strategy: AI strategy data
            format: Export format (pdf, pptx, docx, json)
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            filename = f"ai_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare report content
        report_content = {
            "title": "AI Adoption Strategy Report",
            "executive_summary": self._create_executive_summary(strategy),
            "sections": self._create_report_sections(strategy),
            "recommendations": self._extract_recommendations(strategy)
        }
        
        return self.exporter.export(report_content, filename, format)
    
    def _create_executive_summary(self, strategy: Dict[str, Any]) -> str:
        """Create executive summary from strategy."""
        industry = strategy.get("industry", "organization")
        company_size = strategy.get("company_size", "company")
        
        summary = f"This AI adoption strategy provides a comprehensive roadmap for {company_size} in the {industry} industry. "
        summary += "The strategy includes prioritized use cases, implementation roadmaps, ROI analysis, and change management guidance."
        
        return summary
    
    def _create_report_sections(self, strategy: Dict[str, Any]) -> List[Dict[str, str]]:
        """Create report sections from strategy."""
        sections = []
        
        if "ai_maturity_assessment" in strategy:
            sections.append({
                "title": "AI Maturity Assessment",
                "content": str(strategy["ai_maturity_assessment"])
            })
        
        if "use_cases" in strategy:
            sections.append({
                "title": "High-Value Use Cases",
                "content": str(strategy["use_cases"])
            })
        
        if "ai_adoption_roadmap" in strategy:
            sections.append({
                "title": "AI Adoption Roadmap",
                "content": str(strategy["ai_adoption_roadmap"])
            })
        
        if "technology_stack" in strategy:
            sections.append({
                "title": "Technology Stack Recommendations",
                "content": str(strategy["technology_stack"])
            })
        
        if "roi_analysis" in strategy:
            sections.append({
                "title": "ROI Analysis",
                "content": str(strategy["roi_analysis"])
            })
        
        if "change_management_plan" in strategy:
            sections.append({
                "title": "Change Management Plan",
                "content": str(strategy["change_management_plan"])
            })
        
        return sections
    
    def _extract_recommendations(self, strategy: Dict[str, Any]) -> List[str]:
        """Extract recommendations from strategy."""
        recommendations = []
        
        if "recommendations" in strategy:
            recs = strategy["recommendations"]
            if isinstance(recs, list):
                recommendations.extend(recs)
            else:
                recommendations.append(str(recs))
        
        if "use_cases" in strategy:
            use_cases = strategy["use_cases"]
            if isinstance(use_cases, list):
                for uc in use_cases[:5]:  # Top 5
                    if isinstance(uc, dict):
                        name = uc.get("name", "Use Case")
                        recommendations.append(f"Prioritize: {name}")
                    else:
                        recommendations.append(f"Use Case: {uc}")
        
        return recommendations if recommendations else ["Review the full AI strategy for detailed recommendations."]


def main():
    """CLI interface for AI strategy advisor."""
    parser = argparse.ArgumentParser(description="Generate AI adoption strategy")
    parser.add_argument(
        "--industry",
        type=str,
        required=True,
        help="Industry sector"
    )
    parser.add_argument(
        "--company-size",
        type=str,
        required=True,
        choices=["startup", "small", "medium", "large", "enterprise"],
        help="Company size"
    )
    parser.add_argument(
        "--budget",
        type=str,
        help="Budget range for AI initiatives"
    )
    parser.add_argument(
        "--ai-maturity",
        type=str,
        choices=["beginner", "intermediate", "advanced"],
        help="Current AI maturity level"
    )
    parser.add_argument(
        "--challenges",
        type=str,
        nargs="+",
        help="List of key business challenges"
    )
    parser.add_argument(
        "--use-cases",
        action="store_true",
        help="Identify use cases only"
    )
    parser.add_argument(
        "--business-functions",
        type=str,
        nargs="+",
        help="Business functions to focus on (for use case identification)"
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
    
    # Initialize advisor
    advisor = AIStrategyAdvisor(llm_provider=args.provider)
    
    # Generate strategy or use cases
    if args.use_cases:
        result = advisor.identify_use_cases(
            industry=args.industry,
            business_functions=args.business_functions
        )
    else:
        result = advisor.advise(
            industry=args.industry,
            company_size=args.company_size,
            budget=args.budget,
            ai_maturity=args.ai_maturity,
            challenges=args.challenges
        )
    
    # Output results
    if args.export:
        export_path = advisor.export_strategy_report(result, format=args.export)
        print(f"Report exported to {export_path}")
    elif args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Strategy saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

