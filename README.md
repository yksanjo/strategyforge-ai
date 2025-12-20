# StrategyForge AI

> **AI-Powered Business Consulting Platform** - Automate strategic consulting, transformation planning, and operations optimization at a fraction of the cost of traditional consultants.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**StrategyForge AI** disrupts traditional consulting by delivering 80% of the value at 5% of the cost. Generate strategic recommendations, implementation roadmaps, and consulting-grade deliverables in minutes instead of weeks.

## Features

- 🎯 **Problem Analysis** - AI-powered analysis of business problems with root cause identification
- 📊 **Strategy Generation** - Multi-option strategic recommendations with detailed roadmaps
- ☁️ **Transformation Planning** - Cloud migration and digital transformation guidance
- ⚙️ **Operations Optimization** - Process analysis and resource allocation optimization
- 🤖 **AI Strategy Advisor** - AI adoption roadmaps and ROI calculations
- 📄 **Professional Reports** - Export presentations, executive summaries, and detailed plans

## Competitive Advantage

**vs. Accenture ($200-500/hour consultants):**
- **Cost**: $99/month vs $200-500/hour
- **Speed**: Minutes vs weeks
- **Consistency**: AI doesn't have bad days
- **Scalability**: Unlimited projects simultaneously

## Installation

### Quick Start (Docker - Recommended)

```bash
# Configure your GPU API endpoint in docker-compose.yml
docker-compose up -d
```

### Manual Installation

```bash
pip install -r requirements.txt
```

## Configuration

### For GPU APIs (Corporate Deployment)

Create a `.env` file:

```env
# GPU API Configuration (choose one)
VLLM_BASE_URL=http://your-gpu-server:8000/v1
VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf

# OR TensorRT-LLM
# TENSORRT_LLM_BASE_URL=http://tensorrt-server:8000/v1
# TENSORRT_LLM_MODEL=llama

# OR Custom OpenAI-compatible API
# CUSTOM_OPENAI_BASE_URL=http://gpu-api:8000/v1
# CUSTOM_OPENAI_MODEL=your-model
```

### For Cloud APIs (Alternative)

```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OLLAMA_BASE_URL=http://localhost:11434  # Optional, for local models
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Usage

### CLI Mode

```bash
# Analyze a business problem
python problem_analyzer.py --input "We need to reduce operational costs by 30%"

# Generate strategic recommendations
python strategy_generator.py --problem-id <id> --output strategy.json

# Plan cloud transformation
python transformation_planner.py --company-size medium --current-stack legacy

# Optimize operations
python operations_optimizer.py --input operations_data.csv

# Get AI adoption strategy
python ai_strategy_advisor.py --industry financial-services --budget 500000
```

### Python API

```python
from problem_analyzer import analyze_problem
from strategy_generator import generate_strategy

# Analyze problem
problem = analyze_problem(
    description="We need to reduce operational costs by 30%",
    industry="financial-services",
    company_size="medium"
)

# Generate strategy
strategy = generate_strategy(problem, options=3)
print(strategy)
```

### Web Interface

```bash
cd web
npm install
npm start
```

Then open http://localhost:3000 in your browser.

## Architecture

```
Problem Input → Analysis → Strategy Generation → Implementation Plan → Report Export
```

## Monetization

- **Freemium**: 1 project/month free
- **Pro**: $99/month - 10 projects
- **Enterprise**: $499/month - Unlimited + API access
- **White-label**: $2,999/month for consulting firms

## Documentation

- [Usage Guide](USAGE_GUIDE.md) - Comprehensive usage instructions
- [API Documentation](API_DOCUMENTATION.md) - Complete API reference

## Examples

### Complete Workflow

```bash
# 1. Analyze problem
python problem_analyzer.py \
    --input "We need to reduce costs by 30%" \
    --industry financial-services \
    --output problem.json

# 2. Generate strategies
python strategy_generator.py \
    --problem-id problem.json \
    --options 3 \
    --output strategies.json

# 3. Export professional report
python report_generator.py \
    --input strategies.json \
    --format pdf
```

## Architecture

```
┌─────────────┐
│   Problem   │
│  Analyzer   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Strategy   │
│  Generator  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Report    │
│  Generator  │
└─────────────┘
```

## Competitive Analysis

**vs. Accenture Consulting:**
- ✅ 95% cost reduction ($99/month vs $200-500/hour)
- ✅ 99% time reduction (minutes vs weeks)
- ✅ Unlimited scalability
- ✅ Consistent quality
- ✅ No human bias

## License

MIT License

