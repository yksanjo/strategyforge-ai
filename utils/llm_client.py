"""
LLM Client for interacting with various AI providers.
Supports OpenAI, Anthropic, and local Ollama models.
"""

import os
from typing import Optional, Dict, Any, List
from enum import Enum
import openai
from anthropic import Anthropic
import httpx


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    VLLM = "vllm"  # vLLM GPU server
    TENSORRT_LLM = "tensorrt_llm"  # TensorRT-LLM
    CUSTOM_OPENAI = "custom_openai"  # Any OpenAI-compatible API


class LLMClient:
    """Unified client for multiple LLM providers."""
    
    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI):
        self.provider = provider
        self._setup_client()
    
    def _setup_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == LLMProvider.OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            openai.api_key = api_key
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
            self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            
        elif self.provider == LLMProvider.ANTHROPIC:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            self.client = Anthropic(api_key=api_key)
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
            
        elif self.provider == LLMProvider.OLLAMA:
            self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            self.model = os.getenv("OLLAMA_MODEL", "llama2")
            
        elif self.provider == LLMProvider.VLLM:
            # vLLM provides OpenAI-compatible API
            self.base_url = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
            self.model = os.getenv("VLLM_MODEL", "meta-llama/Llama-2-7b-chat-hf")
            self.api_key = os.getenv("VLLM_API_KEY", "EMPTY")  # vLLM often doesn't require auth
            
        elif self.provider == LLMProvider.TENSORRT_LLM:
            # TensorRT-LLM provides OpenAI-compatible API
            self.base_url = os.getenv("TENSORRT_LLM_BASE_URL", "http://localhost:8000/v1")
            self.model = os.getenv("TENSORRT_LLM_MODEL", "llama")
            self.api_key = os.getenv("TENSORRT_LLM_API_KEY", "EMPTY")
            
        elif self.provider == LLMProvider.CUSTOM_OPENAI:
            # Any OpenAI-compatible API endpoint
            self.base_url = os.getenv("CUSTOM_OPENAI_BASE_URL")
            if not self.base_url:
                raise ValueError("CUSTOM_OPENAI_BASE_URL not found in environment")
            self.model = os.getenv("CUSTOM_OPENAI_MODEL", "gpt-3.5-turbo")
            self.api_key = os.getenv("CUSTOM_OPENAI_API_KEY", "EMPTY")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
        """
        if self.provider == LLMProvider.OPENAI:
            return self._generate_openai(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider == LLMProvider.ANTHROPIC:
            return self._generate_anthropic(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider == LLMProvider.OLLAMA:
            return self._generate_ollama(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider in [LLMProvider.VLLM, LLMProvider.TENSORRT_LLM, LLMProvider.CUSTOM_OPENAI]:
            return self._generate_openai_compatible(prompt, system_prompt, temperature, max_tokens, **kwargs)
    
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Use OpenAI client with custom base URL if needed
        client = openai.OpenAI(
            api_key=openai.api_key,
            base_url=getattr(self, 'base_url', None)
        ) if hasattr(self, 'base_url') and self.base_url != "https://api.openai.com/v1" else openai
        
        response = client.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def _generate_openai_compatible(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using OpenAI-compatible API (vLLM, TensorRT-LLM, etc.)."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key and self.api_key != "EMPTY":
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        with httpx.Client(timeout=300.0) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Anthropic API."""
        messages = [{"role": "user", "content": prompt}]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=messages,
            **kwargs
        )
        
        return response.content[0].text
    
    def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Ollama API."""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            **kwargs
        }
        
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=300.0)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
    
    def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate structured output following a schema.
        
        Args:
            prompt: The user prompt
            schema: JSON schema for the expected output
            system_prompt: Optional system prompt
            **kwargs: Additional parameters
            
        Returns:
            Structured data matching the schema
        """
        structured_prompt = f"""{prompt}

Please respond in valid JSON format matching this schema:
{str(schema)}

Return only the JSON, no additional text."""
        
        response = self.generate(structured_prompt, system_prompt, **kwargs)
        
        # Try to extract JSON from response
        import json
        import re
        
        # Find JSON in response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Fallback: try parsing entire response
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse structured response", "raw": response}


def get_llm_client(provider: Optional[str] = None) -> LLMClient:
    """
    Factory function to get an LLM client.
    
    Args:
        provider: Provider name ('openai', 'anthropic', 'ollama', 'vllm', 'tensorrt_llm', 'custom_openai') 
                  or None for auto-detect
        
    Returns:
        LLMClient instance
    """
    if provider:
        provider_enum = LLMProvider(provider.lower())
    else:
        # Auto-detect based on available configuration
        if os.getenv("VLLM_BASE_URL"):
            provider_enum = LLMProvider.VLLM
        elif os.getenv("TENSORRT_LLM_BASE_URL"):
            provider_enum = LLMProvider.TENSORRT_LLM
        elif os.getenv("CUSTOM_OPENAI_BASE_URL"):
            provider_enum = LLMProvider.CUSTOM_OPENAI
        elif os.getenv("OPENAI_API_KEY"):
            provider_enum = LLMProvider.OPENAI
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider_enum = LLMProvider.ANTHROPIC
        else:
            provider_enum = LLMProvider.OLLAMA
    
    return LLMClient(provider_enum)

