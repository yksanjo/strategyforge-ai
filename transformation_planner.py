"""
Transformation Planner - Cloud migration and technology transformation planning.
Competes with Accenture's myNav platform.
"""

import os
import json
import argparse
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from utils.llm_client import get_llm_client
from utils.export_formats import ReportExporter
from config.prompts import TRANSFORMATION_PLANNING_SYSTEM_PROMPT, TRANSFORMATION_PLANNING_PROMPT

load_dotenv()


class TransformationPlanner:
    """Plans cloud migrations and technology transformations."""
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.llm = get_llm_client(llm_provider)
        self.exporter = ReportExporter()
    
    def plan(
        self,
        company_size: str,
        current_stack: str,
        industry: Optional[str] = None,
        goals: Optional[str] = None,
        budget: Optional[str] = None,
        timeline: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a transformation plan.
        
        Args:
            company_size: Company size (startup, small, medium, large, enterprise)
            current_stack: Current technology stack description
            industry: Industry sector
            goals: Transformation goals
            budget: Budget range
            timeline: Desired timeline
            
        Returns:
            Dictionary containing transformation plan
        """
        # Build prompt
        prompt = TRANSFORMATION_PLANNING_PROMPT.format(
            company_size=company_size,
            current_stack=current_stack,
            industry=industry or "not specified",
            goals=goals or "modernize technology infrastructure",
            budget=budget or "not specified",
            timeline=timeline or "flexible"
        )
        
        try:
            # Generate transformation plan
            response = self.llm.generate(
                prompt=prompt,
                system_prompt=TRANSFORMATION_PLANNING_SYSTEM_PROMPT,
                temperature=0.7,
                max_tokens=4000
            )
            
            # Try to parse as JSON
            try:
                plan = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, create structured response
                plan = {
                    "raw_plan": response,
                    "company_size": company_size,
                    "current_stack": current_stack,
                    "goals": goals
                }
            
            # Add metadata
            plan["metadata"] = {
                "planned_at": datetime.now().isoformat(),
                "provider": self.llm.provider.value,
                "model": self.llm.model
            }
            
            return plan
            
        except Exception as e:
            return {
                "error": str(e),
                "company_size": company_size,
                "current_stack": current_stack
            }
    
    def plan_cloud_migration(
        self,
        current_infrastructure: str,
        target_cloud: Optional[str] = None,
        company_size: str = "medium",
        industry: Optional[str] = None,
        budget: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Plan a cloud migration.
        
        Args:
            current_infrastructure: Description of current infrastructure
            target_cloud: Target cloud provider (AWS, Azure, GCP, multi-cloud)
            company_size: Company size
            industry: Industry sector
            budget: Budget range
            
        Returns:
            Dictionary containing cloud migration plan
        """
        goals = f"Migrate to {target_cloud or 'cloud'}"
        current_stack = f"Current Infrastructure: {current_infrastructure}"
        
        return self.plan(
            company_size=company_size,
            current_stack=current_stack,
            industry=industry,
            goals=goals,
            budget=budget,
            timeline="6-12 months"
        )
    
    def plan_digital_transformation(
        self,
        current_state: str,
        target_state: str,
        company_size: str = "medium",
        industry: Optional[str] = None,
        budget: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Plan a digital transformation.
        
        Args:
            current_state: Current digital maturity state
            target_state: Desired digital state
            company_size: Company size
            industry: Industry sector
            budget: Budget range
            
        Returns:
            Dictionary containing digital transformation plan
        """
        goals = f"Transform from {current_state} to {target_state}"
        
        return self.plan(
            company_size=company_size,
            current_stack=current_state,
            industry=industry,
            goals=goals,
            budget=budget,
            timeline="12-24 months"
        )
    
    def export_plan(
        self,
        plan: Dict[str, Any],
        format: str = "pdf",
        filename: Optional[str] = None
    ) -> str:
        """
        Export transformation plan in specified format.
        
        Args:
            plan: Transformation plan data
            format: Export format (pdf, pptx, docx, json)
            filename: Optional filename (without extension)
            
        Returns:
            Path to exported file
        """
        if not filename:
            filename = f"transformation_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare report content
        report_content = {
            "title": "Transformation Plan",
            "executive_summary": self._create_executive_summary(plan),
            "sections": self._create_report_sections(plan),
            "recommendations": self._extract_recommendations(plan)
        }
        
        return self.exporter.export(report_content, filename, format)
    
    def _create_executive_summary(self, plan: Dict[str, Any]) -> str:
        """Create executive summary from plan."""
        goals = plan.get("goals", "technology transformation")
        company_size = plan.get("company_size", "organization")
        
        summary = f"This transformation plan outlines the strategy for {company_size} to achieve: {goals}. "
        summary += "The plan includes detailed phases, timelines, resource requirements, and risk mitigation strategies."
        
        return summary
    
    def _create_report_sections(self, plan: Dict[str, Any]) -> List[Dict[str, str]]:
        """Create report sections from plan."""
        sections = []
        
        if "current_state_assessment" in plan:
            sections.append({
                "title": "Current State Assessment",
                "content": str(plan["current_state_assessment"])
            })
        
        if "target_state_vision" in plan:
            sections.append({
                "title": "Target State Vision",
                "content": str(plan["target_state_vision"])
            })
        
        if "transformation_roadmap" in plan:
            sections.append({
                "title": "Transformation Roadmap",
                "content": str(plan["transformation_roadmap"])
            })
        
        if "technology_recommendations" in plan:
            sections.append({
                "title": "Technology Recommendations",
                "content": str(plan["technology_recommendations"])
            })
        
        if "cost_benefit_analysis" in plan:
            sections.append({
                "title": "Cost-Benefit Analysis",
                "content": str(plan["cost_benefit_analysis"])
            })
        
        return sections
    
    def _extract_recommendations(self, plan: Dict[str, Any]) -> List[str]:
        """Extract recommendations from plan."""
        recommendations = []
        
        if "recommendations" in plan:
            recs = plan["recommendations"]
            if isinstance(recs, list):
                recommendations.extend(recs)
            else:
                recommendations.append(str(recs))
        
        if "technology_recommendations" in plan:
            tech_recs = plan["technology_recommendations"]
            if isinstance(tech_recs, list):
                recommendations.extend([f"Technology: {r}" for r in tech_recs])
            else:
                recommendations.append(f"Technology: {tech_recs}")
        
        return recommendations if recommendations else ["Review the full transformation plan for detailed recommendations."]


def main():
    """CLI interface for transformation planner."""
    parser = argparse.ArgumentParser(description="Plan technology transformations")
    parser.add_argument(
        "--company-size",
        type=str,
        required=True,
        choices=["startup", "small", "medium", "large", "enterprise"],
        help="Company size"
    )
    parser.add_argument(
        "--current-stack",
        type=str,
        required=True,
        help="Current technology stack description"
    )
    parser.add_argument(
        "--industry",
        type=str,
        help="Industry sector"
    )
    parser.add_argument(
        "--goals",
        type=str,
        help="Transformation goals"
    )
    parser.add_argument(
        "--budget",
        type=str,
        help="Budget range"
    )
    parser.add_argument(
        "--timeline",
        type=str,
        help="Desired timeline"
    )
    parser.add_argument(
        "--cloud-migration",
        action="store_true",
        help="Plan cloud migration"
    )
    parser.add_argument(
        "--target-cloud",
        type=str,
        choices=["AWS", "Azure", "GCP", "multi-cloud"],
        help="Target cloud provider (for cloud migration)"
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
        help="Export format for plan"
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openai", "anthropic", "ollama"],
        help="LLM provider to use"
    )
    
    args = parser.parse_args()
    
    # Initialize planner
    planner = TransformationPlanner(llm_provider=args.provider)
    
    # Generate plan
    if args.cloud_migration:
        result = planner.plan_cloud_migration(
            current_infrastructure=args.current_stack,
            target_cloud=args.target_cloud,
            company_size=args.company_size,
            industry=args.industry,
            budget=args.budget
        )
    else:
        result = planner.plan(
            company_size=args.company_size,
            current_stack=args.current_stack,
            industry=args.industry,
            goals=args.goals,
            budget=args.budget,
            timeline=args.timeline
        )
    
    # Output results
    if args.export:
        export_path = planner.export_plan(result, format=args.export)
        print(f"Plan exported to {export_path}")
    elif args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Plan saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

