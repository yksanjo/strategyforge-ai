# StrategyForge AI - Deployment Guide

## Quick Deployment with GPU APIs

StrategyForge AI is designed to be **plug-and-go** with corporate GPU infrastructure. It supports multiple GPU-accelerated LLM serving solutions.

## Supported GPU API Solutions

### 1. vLLM (Recommended)
High-performance LLM serving with PagedAttention.

### 2. TensorRT-LLM
NVIDIA-optimized LLM inference.

### 3. Any OpenAI-Compatible API
Works with any OpenAI-compatible endpoint (TGI, llama.cpp, etc.)

## Deployment Options

### Option 1: Docker Compose (Easiest)

1. **Configure GPU API endpoint** in `docker-compose.yml`:

```yaml
environment:
  # Point to your GPU API server
  - VLLM_BASE_URL=http://your-gpu-server:8000/v1
  - VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf
```

2. **Deploy**:

```bash
docker-compose up -d
```

3. **Access**: http://localhost:8000

### Option 2: Docker (Standalone)

```bash
# Build
docker build -t strategyforge-ai .

# Run with GPU API endpoint
docker run -d \
  -p 8000:8000 \
  -e VLLM_BASE_URL=http://your-gpu-server:8000/v1 \
  -e VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf \
  -v $(pwd)/outputs:/app/outputs \
  strategyforge-ai
```

### Option 3: Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: strategyforge-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: strategyforge-ai
  template:
    metadata:
      labels:
        app: strategyforge-ai
    spec:
      containers:
      - name: api
        image: strategyforge-ai:latest
        ports:
        - containerPort: 8000
        env:
        - name: VLLM_BASE_URL
          value: "http://vllm-service:8000/v1"
        - name: VLLM_MODEL
          value: "meta-llama/Llama-2-7b-chat-hf"
```

### Option 4: Direct Python Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export VLLM_BASE_URL=http://your-gpu-server:8000/v1
export VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf

# Run
uvicorn api:app --host 0.0.0.0 --port 8000
```

## GPU API Configuration

### vLLM Setup

If deploying vLLM server:

```bash
# Run vLLM server
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-2-7b-chat-hf \
  --api-key EMPTY
```

Then configure StrategyForge:
```bash
export VLLM_BASE_URL=http://localhost:8000/v1
export VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf
```

### TensorRT-LLM Setup

```bash
# Run TensorRT-LLM server
docker run --gpus all -p 8000:8000 \
  nvcr.io/nvidia/tensorrt-llm:latest \
  --model-dir /models/llama
```

Configure StrategyForge:
```bash
export TENSORRT_LLM_BASE_URL=http://localhost:8000/v1
export TENSORRT_LLM_MODEL=llama
```

### Custom OpenAI-Compatible API

For any OpenAI-compatible endpoint:

```bash
export CUSTOM_OPENAI_BASE_URL=http://your-gpu-api:8000/v1
export CUSTOM_OPENAI_MODEL=your-model-name
export CUSTOM_OPENAI_API_KEY=your-key-if-needed
```

## Environment Variables

### GPU API Configuration

```bash
# vLLM
VLLM_BASE_URL=http://vllm-server:8000/v1
VLLM_MODEL=meta-llama/Llama-2-7b-chat-hf
VLLM_API_KEY=EMPTY  # Usually not required

# TensorRT-LLM
TENSORRT_LLM_BASE_URL=http://tensorrt-llm-server:8000/v1
TENSORRT_LLM_MODEL=llama
TENSORRT_LLM_API_KEY=EMPTY

# Custom OpenAI-compatible
CUSTOM_OPENAI_BASE_URL=http://gpu-api:8000/v1
CUSTOM_OPENAI_MODEL=your-model
CUSTOM_OPENAI_API_KEY=your-key
```

### Application Configuration

```bash
DEBUG=False
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./strategyforge.db
OUTPUT_DIR=./outputs
```

## Corporate Deployment Checklist

- [ ] GPU infrastructure available (NVIDIA GPUs recommended)
- [ ] LLM serving solution deployed (vLLM, TensorRT-LLM, etc.)
- [ ] GPU API endpoint accessible from StrategyForge
- [ ] Environment variables configured
- [ ] Docker/Kubernetes deployment configured
- [ ] Network security rules configured
- [ ] Load balancer configured (for production)
- [ ] Monitoring/logging set up
- [ ] Backup strategy in place

## Production Considerations

### Security
- Use API keys for GPU API endpoints
- Enable HTTPS/TLS
- Implement rate limiting
- Add authentication middleware

### Performance
- Use load balancer for multiple API instances
- Configure connection pooling
- Enable response caching where appropriate
- Monitor GPU utilization

### Monitoring
- Set up health checks
- Monitor API response times
- Track GPU API availability
- Log all requests/responses

## Troubleshooting

### GPU API Connection Issues

```bash
# Test GPU API connectivity
curl http://your-gpu-server:8000/v1/models

# Check StrategyForge logs
docker logs strategyforge-api

# Verify environment variables
docker exec strategyforge-api env | grep VLLM
```

### Performance Issues

- Check GPU utilization: `nvidia-smi`
- Verify model is loaded: Check GPU API logs
- Monitor API response times
- Consider model quantization for faster inference

## Example: Complete Corporate Deployment

```bash
# 1. Deploy GPU API server (vLLM)
docker run -d --gpus all --name vllm-server \
  -p 8001:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-2-7b-chat-hf

# 2. Deploy StrategyForge AI
docker-compose up -d

# 3. Verify deployment
curl http://localhost:8000/health
curl http://localhost:8000/api/analyze-problem \
  -H "Content-Type: application/json" \
  -d '{"problem_description": "Test problem"}'
```

## Support

For deployment issues, check:
- GPU API server logs
- StrategyForge API logs
- Network connectivity
- Environment variable configuration

