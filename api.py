"""
FastAPI backend for StrategyForge AI web interface.
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from problem_analyzer import ProblemAnalyzer
from strategy_generator import StrategyGenerator
from transformation_planner import TransformationPlanner
from operations_optimizer import OperationsOptimizer
from ai_strategy_advisor import AIStrategyAdvisor
from report_generator import ReportGenerator

load_dotenv()

app = FastAPI(title="StrategyForge AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request models
class ProblemAnalysisRequest(BaseModel):
    problem_description: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    additional_context: Optional[str] = None


class StrategyGenerationRequest(BaseModel):
    problem_analysis: Dict[str, Any]
    num_options: int = 3
    focus_areas: Optional[List[str]] = None


class TransformationPlanningRequest(BaseModel):
    company_size: str
    current_stack: str
    industry: Optional[str] = None
    goals: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None


class OperationsOptimizationRequest(BaseModel):
    operations_summary: str
    metrics: Optional[Dict[str, Any]] = None
    challenges: Optional[List[str]] = None


class AIStrategyRequest(BaseModel):
    industry: str
    company_size: str
    budget: Optional[str] = None
    ai_maturity: Optional[str] = None
    challenges: Optional[List[str]] = None


class ReportGenerationRequest(BaseModel):
    analysis_results: Dict[str, Any]
    report_type: str = "executive"
    title: Optional[str] = None


# Health check
@app.get("/")
async def root():
    return {"message": "StrategyForge AI API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Problem Analysis endpoints
@app.post("/api/analyze-problem")
async def analyze_problem(request: ProblemAnalysisRequest):
    """Analyze a business problem."""
    try:
        analyzer = ProblemAnalyzer()
        result = analyzer.analyze(
            problem_description=request.problem_description,
            industry=request.industry,
            company_size=request.company_size,
            additional_context=request.additional_context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-problem-from-file")
async def analyze_problem_from_file(file: UploadFile = File(...)):
    """Analyze problem from uploaded file."""
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        analyzer = ProblemAnalyzer()
        result = analyzer.analyze_from_file(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Strategy Generation endpoints
@app.post("/api/generate-strategy")
async def generate_strategy(request: StrategyGenerationRequest):
    """Generate strategic recommendations."""
    try:
        generator = StrategyGenerator()
        result = generator.generate(
            problem_analysis=request.problem_analysis,
            num_options=request.num_options,
            focus_areas=request.focus_areas
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Transformation Planning endpoints
@app.post("/api/plan-transformation")
async def plan_transformation(request: TransformationPlanningRequest):
    """Plan technology transformation."""
    try:
        planner = TransformationPlanner()
        result = planner.plan(
            company_size=request.company_size,
            current_stack=request.current_stack,
            industry=request.industry,
            goals=request.goals,
            budget=request.budget,
            timeline=request.timeline
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/plan-cloud-migration")
async def plan_cloud_migration(
    current_infrastructure: str,
    target_cloud: Optional[str] = None,
    company_size: str = "medium",
    industry: Optional[str] = None,
    budget: Optional[str] = None
):
    """Plan cloud migration."""
    try:
        planner = TransformationPlanner()
        result = planner.plan_cloud_migration(
            current_infrastructure=current_infrastructure,
            target_cloud=target_cloud,
            company_size=company_size,
            industry=industry,
            budget=budget
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Operations Optimization endpoints
@app.post("/api/optimize-operations")
async def optimize_operations(request: OperationsOptimizationRequest):
    """Optimize business operations."""
    try:
        optimizer = OperationsOptimizer()
        result = optimizer.optimize(
            operations_summary=request.operations_summary,
            metrics=request.metrics,
            challenges=request.challenges
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# AI Strategy endpoints
@app.post("/api/ai-strategy")
async def ai_strategy(request: AIStrategyRequest):
    """Generate AI adoption strategy."""
    try:
        advisor = AIStrategyAdvisor()
        result = advisor.advise(
            industry=request.industry,
            company_size=request.company_size,
            budget=request.budget,
            ai_maturity=request.ai_maturity,
            challenges=request.challenges
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/identify-ai-use-cases")
async def identify_ai_use_cases(
    industry: str,
    business_functions: Optional[List[str]] = None,
    priority: str = "high_impact"
):
    """Identify high-value AI use cases."""
    try:
        advisor = AIStrategyAdvisor()
        result = advisor.identify_use_cases(
            industry=industry,
            business_functions=business_functions,
            priority=priority
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Report Generation endpoints
@app.post("/api/generate-report")
async def generate_report(request: ReportGenerationRequest):
    """Generate professional report."""
    try:
        generator = ReportGenerator()
        result = generator.generate_report(
            analysis_results=request.analysis_results,
            report_type=request.report_type,
            title=request.title
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export-report")
async def export_report(
    analysis_results: Dict[str, Any],
    format: str = "pdf",
    report_type: str = "executive"
):
    """Export report in specified format."""
    try:
        generator = ReportGenerator()
        report = generator.generate_report(
            analysis_results=analysis_results,
            report_type=report_type
        )
        export_path = generator.export_report(report, format=format)
        return FileResponse(
            export_path,
            media_type="application/octet-stream",
            filename=os.path.basename(export_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

