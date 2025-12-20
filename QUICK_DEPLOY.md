# Quick Deployment Guide - Plug and Go

## For Corporations with GPU Infrastructure

### Step 1: Point to Your GPU API

Edit `.env` file:

```bash
# If using vLLM
VLLM_BASE_URL=http://your-vllm-server:8000/v1
VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf

# OR if using TensorRT-LLM
TENSORRT_LLM_BASE_URL=http://your-tensorrt-server:8000/v1
TENSORRT_LLM_MODEL=llama

# OR if using any OpenAI-compatible API
CUSTOM_OPENAI_BASE_URL=http://your-gpu-api:8000/v1
CUSTOM_OPENAI_MODEL=your-model-name
```

### Step 2: Deploy

**Option A: Docker Compose (Recommended)**
```bash
docker-compose up -d
```

**Option B: Docker**
```bash
docker build -t strategyforge-ai .
docker run -d -p 8000:8000 --env-file .env strategyforge-ai
```

**Option C: Kubernetes**
```bash
kubectl apply -f kubernetes-deployment.yaml
```

**Option D: Direct Python**
```bash
pip install -r requirements.txt
source .env
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Step 3: Verify

```bash
curl http://localhost:8000/health
```

### Step 4: Use

```bash
# Test problem analysis
curl -X POST http://localhost:8000/api/analyze-problem \
  -H "Content-Type: application/json" \
  -d '{
    "problem_description": "We need to reduce costs by 30%",
    "industry": "financial-services",
    "company_size": "medium"
  }'
```

## That's It!

The platform automatically:
- ✅ Detects your GPU API configuration
- ✅ Connects to your LLM endpoint
- ✅ Handles all API communication
- ✅ Provides full functionality

## Supported GPU API Solutions

- ✅ **vLLM** - High-performance serving
- ✅ **TensorRT-LLM** - NVIDIA-optimized
- ✅ **TGI (Text Generation Inference)** - Hugging Face
- ✅ **llama.cpp** - CPU/GPU inference
- ✅ **Any OpenAI-compatible API** - Universal support

## No Additional Configuration Needed!

The platform works out-of-the-box with any OpenAI-compatible GPU API endpoint. Just point it to your server and go!

