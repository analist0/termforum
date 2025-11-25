"""Ollama API client for TermForum"""

import requests
import json
from typing import Optional, List, Dict, Iterator


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama client"""
        self.base_url = base_url
        self.api_url = f"{base_url}/api"

    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=2)
            return response.status_code == 200
        except (requests.RequestException, requests.Timeout):
            return False

    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception:
            return []

    def generate(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        stream: bool = False
    ) -> str:
        """
        Generate text from prompt

        Args:
            model: Model name (e.g., 'qwen2.5-coder:7b')
            prompt: User prompt
            system: System prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Max tokens to generate
            stream: Stream response

        Returns:
            Generated text
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=60,
                stream=stream
            )

            if response.status_code == 200:
                if stream:
                    # Stream mode - yield chunks
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            chunk = data.get("response", "")
                            full_response += chunk
                            if data.get("done"):
                                return full_response
                    return full_response
                else:
                    # Non-stream mode
                    data = response.json()
                    return data.get("response", "")
            else:
                return f"Error: Ollama returned status {response.status_code}"

        except requests.Timeout:
            return "Error: Ollama request timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Chat with model using conversation history

        Args:
            model: Model name
            messages: List of {"role": "user/assistant", "content": "..."}
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Generated response
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "")
            else:
                return f"Error: Ollama returned status {response.status_code}"

        except requests.Timeout:
            return "Error: Ollama request timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Iterator[str]:
        """
        Generate text with streaming

        Yields:
            Text chunks as they arrive
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=60,
                stream=True
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            yield chunk
                        if data.get("done"):
                            break
        except Exception as e:
            yield f"Error: {str(e)}"
