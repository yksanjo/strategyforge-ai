"""
Prompt templates for various analysis and generation tasks.
"""

PROBLEM_ANALYSIS_SYSTEM_PROMPT = """You are an expert business consultant with decades of experience analyzing complex business problems. Your role is to thoroughly analyze business problems, identify root causes, and provide structured insights."""

PROBLEM_ANALYSIS_PROMPT = """Analyze the following business problem:

Problem Description: {problem_description}

Additional Context:
- Industry: {industry}
- Company Size: {company_size}
- Additional Information: {additional_context}

Please provide a comprehensive analysis including:
1. Problem Statement (clear, concise summary)
2. Root Causes (identify 3-5 primary root causes)
3. Stakeholders (who is affected and who needs to be involved)
4. Constraints (budget, time, resources, regulatory)
5. Current State Assessment
6. Desired State Definition
7. Gap Analysis (what needs to change)

Format your response as structured JSON with these sections."""

STRATEGY_GENERATION_SYSTEM_PROMPT = """You are a senior strategy consultant specializing in developing actionable business strategies. You create multi-option strategic recommendations with detailed implementation roadmaps."""

STRATEGY_GENERATION_PROMPT = """Based on the following problem analysis, generate {num_options} strategic options:

Problem Analysis:
{problem_analysis}

For each strategic option, provide:
1. Strategy Name and Description
2. Key Objectives
3. Implementation Roadmap (phases with timelines)
4. Required Resources (budget, team, technology)
5. Expected Outcomes and KPIs
6. Risks and Mitigation Strategies
7. Success Criteria

Format as JSON with an array of strategy options."""

TRANSFORMATION_PLANNING_SYSTEM_PROMPT = """You are a cloud and digital transformation expert. You help organizations plan and execute technology transformations, cloud migrations, and digital modernization initiatives."""

TRANSFORMATION_PLANNING_PROMPT = """Create a comprehensive transformation plan for the following scenario:

Current State:
- Company Size: {company_size}
- Current Technology Stack: {current_stack}
- Industry: {industry}
- Transformation Goals: {goals}
- Budget: {budget}
- Timeline: {timeline}

Provide a detailed transformation plan including:
1. Current State Assessment
2. Target State Vision
3. Transformation Roadmap (phases, milestones, timelines)
4. Technology Recommendations
5. Migration Strategy
6. Resource Requirements
7. Risk Assessment
8. Success Metrics
9. Cost-Benefit Analysis

Format as structured JSON."""

OPERATIONS_OPTIMIZATION_SYSTEM_PROMPT = """You are an operations excellence consultant specializing in process optimization, resource allocation, and operational efficiency improvements."""

OPERATIONS_OPTIMIZATION_PROMPT = """Analyze and optimize the following operations:

Operations Data Summary:
{operations_summary}

Key Metrics:
{metrics}

Current Challenges:
{challenges}

Provide optimization recommendations including:
1. Current State Analysis
2. Identified Inefficiencies
3. Optimization Opportunities (prioritized)
4. Recommended Process Improvements
5. Resource Reallocation Suggestions
6. Performance Metrics and KPIs
7. Implementation Plan
8. Expected Improvements (quantified)

Format as structured JSON."""

AI_STRATEGY_ADVISOR_SYSTEM_PROMPT = """You are an AI strategy advisor helping organizations identify, prioritize, and implement AI initiatives. You understand AI capabilities, ROI calculations, and change management."""

AI_STRATEGY_ADVISOR_PROMPT = """Develop an AI adoption strategy for:

Industry: {industry}
Company Size: {company_size}
Budget: {budget}
Current AI Maturity: {ai_maturity}
Key Business Challenges: {challenges}

Provide a comprehensive AI strategy including:
1. AI Maturity Assessment
2. High-Value Use Cases (prioritized with ROI estimates)
3. AI Adoption Roadmap (phases, timelines)
4. Technology Stack Recommendations
5. Resource Requirements (skills, tools, infrastructure)
6. ROI Analysis for Each Use Case
7. Risk Assessment and Mitigation
8. Change Management Plan
9. Success Metrics

Format as structured JSON."""

REPORT_GENERATION_SYSTEM_PROMPT = """You are a professional report writer specializing in creating executive-level business reports, presentations, and strategic documents."""

REPORT_GENERATION_PROMPT = """Create a professional executive report based on the following analysis:

Analysis Results:
{analysis_results}

Include:
1. Executive Summary (2-3 paragraphs)
2. Key Findings
3. Detailed Analysis
4. Recommendations (prioritized)
5. Implementation Roadmap
6. Risk Assessment
7. Expected Outcomes

Format as a well-structured report suitable for executive presentation."""

