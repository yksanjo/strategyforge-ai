# StrategyForge AI - Usage Guide

## Quick Start

### 1. Installation

```bash
cd strategyforge-ai
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here  # Optional
```

### 3. CLI Usage

#### Problem Analysis

```bash
python problem_analyzer.py \
    --input "We need to reduce operational costs by 30%" \
    --industry financial-services \
    --company-size medium \
    --output analysis.json
```

#### Strategy Generation

```bash
python strategy_generator.py \
    --problem-id analysis.json \
    --options 3 \
    --export pdf
```

#### Transformation Planning

```bash
python transformation_planner.py \
    --company-size medium \
    --current-stack "Legacy on-premise infrastructure" \
    --goals "Migrate to cloud" \
    --export pptx
```

#### Operations Optimization

```bash
python operations_optimizer.py \
    --input operations_data.csv \
    --export pdf
```

#### AI Strategy Advisor

```bash
python ai_strategy_advisor.py \
    --industry financial-services \
    --company-size large \
    --budget "500000" \
    --export pdf
```

### 4. Web Interface

#### Start Backend API

```bash
python api.py
# Or with uvicorn:
uvicorn api:app --reload
```

#### Start Frontend

```bash
cd web
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## API Endpoints

### Problem Analysis

**POST** `/api/analyze-problem`

```json
{
  "problem_description": "We need to reduce costs",
  "industry": "financial-services",
  "company_size": "medium"
}
```

### Strategy Generation

**POST** `/api/generate-strategy`

```json
{
  "problem_analysis": {...},
  "num_options": 3,
  "focus_areas": ["cost-reduction", "efficiency"]
}
```

### Transformation Planning

**POST** `/api/plan-transformation`

```json
{
  "company_size": "medium",
  "current_stack": "Legacy infrastructure",
  "goals": "Cloud migration",
  "budget": "500000"
}
```

### Operations Optimization

**POST** `/api/optimize-operations`

```json
{
  "operations_summary": "Current operations description",
  "metrics": {"efficiency": 0.7},
  "challenges": ["High costs", "Slow processes"]
}
```

### AI Strategy

**POST** `/api/ai-strategy`

```json
{
  "industry": "financial-services",
  "company_size": "large",
  "budget": "500000",
  "ai_maturity": "beginner"
}
```

### Report Generation

**POST** `/api/generate-report`

```json
{
  "analysis_results": {...},
  "report_type": "executive",
  "title": "Custom Report Title"
}
```

## Python API Usage

```python
from problem_analyzer import ProblemAnalyzer
from strategy_generator import StrategyGenerator

# Analyze problem
analyzer = ProblemAnalyzer()
problem = analyzer.analyze(
    problem_description="We need to reduce costs by 30%",
    industry="financial-services",
    company_size="medium"
)

# Generate strategy
generator = StrategyGenerator()
strategy = generator.generate(
    problem_analysis=problem,
    num_options=3
)

# Export report
generator.export_strategy_report(strategy, format="pdf")
```

## Export Formats

All modules support exporting to:
- **PDF** - Professional PDF reports
- **PPTX** - PowerPoint presentations
- **DOCX** - Word documents
- **JSON** - Raw data format

## Best Practices

1. **Start with Problem Analysis** - Always begin by analyzing the problem thoroughly
2. **Use Industry Context** - Provide industry and company size for better recommendations
3. **Iterate on Strategies** - Generate multiple options and refine based on feedback
4. **Export Reports** - Use professional export formats for stakeholder presentations
5. **Combine Modules** - Chain problem analysis → strategy → transformation planning for comprehensive solutions

## Troubleshooting

### API Key Issues

- Ensure `.env` file exists and contains valid API keys
- Check that environment variables are loaded correctly

### LLM Provider Issues

- Default provider is OpenAI
- Fallback to Anthropic or Ollama if OpenAI unavailable
- Set `--provider` flag to specify provider

### Export Issues

- Ensure output directory exists (default: `./outputs`)
- Check file permissions
- Verify required libraries are installed (python-pptx, reportlab, etc.)

## Examples

See the `examples/` directory for sample use cases and workflows.

