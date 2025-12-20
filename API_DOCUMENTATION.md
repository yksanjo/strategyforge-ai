# StrategyForge AI - API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, implement API key authentication.

## Endpoints

### Health Check

**GET** `/health`

Returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00"
}
```

### Problem Analysis

**POST** `/api/analyze-problem`

Analyze a business problem and identify root causes.

**Request Body:**
```json
{
  "problem_description": "string (required)",
  "industry": "string (optional)",
  "company_size": "string (optional)",
  "additional_context": "string (optional)"
}
```

**Response:**
```json
{
  "problem_statement": "string",
  "root_causes": ["string"],
  "stakeholders": ["string"],
  "constraints": {},
  "metadata": {
    "analyzed_at": "ISO timestamp",
    "provider": "openai",
    "model": "gpt-4-turbo-preview"
  }
}
```

### Problem Analysis from File

**POST** `/api/analyze-problem-from-file`

Analyze problem from uploaded document (PDF, DOCX, TXT).

**Request:** Multipart form data with `file` field

**Response:** Same as `/api/analyze-problem`

### Strategy Generation

**POST** `/api/generate-strategy`

Generate strategic recommendations from problem analysis.

**Request Body:**
```json
{
  "problem_analysis": {
    "problem_statement": "string",
    ...
  },
  "num_options": 3,
  "focus_areas": ["string"] // optional
}
```

**Response:**
```json
{
  "strategies": [
    {
      "name": "string",
      "description": "string",
      "key_objectives": ["string"],
      "roadmap": {},
      "expected_outcomes": {},
      "risks": {}
    }
  ],
  "num_options": 3,
  "metadata": {}
}
```

### Transformation Planning

**POST** `/api/plan-transformation`

Plan technology transformation or cloud migration.

**Request Body:**
```json
{
  "company_size": "startup|small|medium|large|enterprise",
  "current_stack": "string",
  "industry": "string (optional)",
  "goals": "string (optional)",
  "budget": "string (optional)",
  "timeline": "string (optional)"
}
```

**Response:**
```json
{
  "current_state_assessment": {},
  "target_state_vision": {},
  "transformation_roadmap": {},
  "technology_recommendations": {},
  "cost_benefit_analysis": {},
  "metadata": {}
}
```

### Cloud Migration Planning

**POST** `/api/plan-cloud-migration`

Plan specific cloud migration.

**Query Parameters:**
- `current_infrastructure` (required)
- `target_cloud` (optional): AWS, Azure, GCP, multi-cloud
- `company_size` (optional, default: medium)
- `industry` (optional)
- `budget` (optional)

**Response:** Same as transformation planning

### Operations Optimization

**POST** `/api/optimize-operations`

Optimize business operations and processes.

**Request Body:**
```json
{
  "operations_summary": "string",
  "metrics": {
    "key": "value"
  },
  "challenges": ["string"]
}
```

**Response:**
```json
{
  "current_state_analysis": {},
  "identified_inefficiencies": {},
  "optimization_opportunities": {},
  "process_improvements": {},
  "expected_improvements": {},
  "metadata": {}
}
```

### AI Strategy

**POST** `/api/ai-strategy`

Generate AI adoption strategy.

**Request Body:**
```json
{
  "industry": "string",
  "company_size": "startup|small|medium|large|enterprise",
  "budget": "string (optional)",
  "ai_maturity": "beginner|intermediate|advanced (optional)",
  "challenges": ["string (optional)"]
}
```

**Response:**
```json
{
  "ai_maturity_assessment": {},
  "use_cases": [],
  "ai_adoption_roadmap": {},
  "technology_stack": {},
  "roi_analysis": {},
  "metadata": {}
}
```

### Identify AI Use Cases

**POST** `/api/identify-ai-use-cases`

Identify high-value AI use cases.

**Query Parameters:**
- `industry` (required)
- `business_functions` (optional, array)
- `priority` (optional, default: high_impact)

**Response:**
```json
{
  "use_cases": [
    {
      "name": "string",
      "description": "string",
      "business_value": "string",
      "implementation_complexity": "low|medium|high",
      "expected_roi": "string",
      "required_resources": {},
      "timeline": "string"
    }
  ]
}
```

### Generate Report

**POST** `/api/generate-report`

Generate professional report from analysis results.

**Request Body:**
```json
{
  "analysis_results": {},
  "report_type": "executive|detailed|presentation",
  "title": "string (optional)"
}
```

**Response:**
```json
{
  "title": "string",
  "report_type": "string",
  "executive_summary": "string",
  "sections": [
    {
      "title": "string",
      "content": "string"
    }
  ],
  "recommendations": ["string"],
  "metadata": {}
}
```

### Export Report

**POST** `/api/export-report`

Export report in specified format.

**Query Parameters:**
- `format` (required): pdf, pptx, docx, json
- `report_type` (optional, default: executive)

**Request Body:**
```json
{
  "analysis_results": {}
}
```

**Response:** File download (binary)

## Error Responses

All endpoints may return errors in the following format:

```json
{
  "detail": "Error message"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request
- `500` - Internal Server Error

## Rate Limiting

Currently no rate limiting. In production, implement rate limiting based on API keys.

## CORS

CORS is enabled for all origins in development. Restrict in production.

