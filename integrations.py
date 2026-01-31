"""
ULTIMA_SYSTEM - AI Integrations
IMPULSE REBIRTH [ 2026 ]

Unified interface for Ollama, Dolphin, Gemini CLI, and Claude AI
"""

import os
import json
import subprocess
import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path


class OllamaIntegration:
    """Integration with Ollama for local LLM inference"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        try:
            import ollama
            self.client = ollama.Client(host=base_url)
            self.async_client = ollama.AsyncClient(host=base_url)
            self.available = True
        except Exception as e:
            print(f"[WARN]  Ollama integration unavailable: {e}")
            self.available = False

    def list_models(self) -> List[str]:
        """List available Ollama models"""
        if not self.available:
            return []
        try:
            response = self.client.list()
            return [model['name'] for model in response.get('models', [])]
        except Exception as e:
            print(f"[ERROR] Error listing Ollama models: {e}")
            return []

    def generate(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text using Ollama"""
        if not self.available:
            return None
        try:
            response = self.client.generate(model=model, prompt=prompt, **kwargs)
            return response.get('response', '')
        except Exception as e:
            print(f"[ERROR] Ollama generation error: {e}")
            return None

    async def generate_async(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Async text generation using Ollama"""
        if not self.available:
            return None
        try:
            response = await self.async_client.generate(model=model, prompt=prompt, **kwargs)
            return response.get('response', '')
        except Exception as e:
            print(f"[ERROR] Ollama async generation error: {e}")
            return None

    def chat(self, model: str, messages: List[Dict], **kwargs) -> Optional[str]:
        """Chat with Ollama model"""
        if not self.available:
            return None
        try:
            response = self.client.chat(model=model, messages=messages, **kwargs)
            return response['message']['content']
        except Exception as e:
            print(f"[ERROR] Ollama chat error: {e}")
            return None


class DolphinIntegration:
    """Integration with Dolphin project"""

    def __init__(self, dolphin_path: str = r"E:\[ PROJECTS ]\[ LOCAL ]\[ CODEX ] PC\[ DOLPHIN ]"):
        self.dolphin_path = Path(dolphin_path)
        self.available = self.dolphin_path.exists()

        if not self.available:
            print(f"[WARN]  Dolphin not found at: {dolphin_path}")

    def run_script(self, script_name: str, *args) -> Optional[str]:
        """Run a Dolphin script"""
        if not self.available:
            return None

        script_path = self.dolphin_path / "scripts" / script_name
        if not script_path.exists():
            print(f"[ERROR] Dolphin script not found: {script_name}")
            return None

        try:
            result = subprocess.run(
                ["node", str(script_path)] + list(args),
                capture_output=True,
                text=True,
                cwd=str(self.dolphin_path)
            )
            return result.stdout
        except Exception as e:
            print(f"[ERROR] Dolphin script error: {e}")
            return None

    def dolphin_command(self, *args) -> Optional[str]:
        """Run main dolphin.mjs script"""
        return self.run_script("dolphin.mjs", *args)

    def agent_watch(self) -> Optional[str]:
        """Run Dolphin agent watch"""
        return self.run_script("agent.mjs", "watch")

    def create_idea(self, idea_data: Dict[str, Any]) -> Optional[str]:
        """Create a new idea in Dolphin"""
        # Save idea data to temp file
        temp_file = self.dolphin_path / "temp_idea.json"
        with open(temp_file, 'w') as f:
            json.dump(idea_data, f)

        result = self.run_script("create-idea.mjs", str(temp_file))

        # Cleanup
        if temp_file.exists():
            temp_file.unlink()

        return result


class GeminiIntegration:
    """Integration with Gemini via google-genai SDK"""

    def __init__(self, api_key: Optional[str] = None):
        self.available = False
        self.client = None
        self.model_name = "gemini-2.0-flash"

        try:
            import google.genai as genai

            key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not key:
                # Try to read from .env
                env_path = Path(r"C:\Users\SHAD\.env")
                if env_path.exists():
                    for line in env_path.read_text().splitlines():
                        if line.startswith("GEMINI_API_KEY=") or line.startswith("GOOGLE_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break

            if not key:
                print("[WARN]  Gemini: no API key found (set GEMINI_API_KEY env var)")
                return

            self.client = genai.Client(api_key=key)
            self.available = True
        except Exception as e:
            print(f"[WARN]  Gemini SDK unavailable: {e}")

    def generate(self, prompt: str, model: str = None, **kwargs) -> Optional[str]:
        """Generate text using Gemini SDK"""
        if not self.available:
            return None
        try:
            from google.genai import types
            config = types.GenerateContentConfig(
                temperature=kwargs.get("temperature", 0.7),
                max_output_tokens=kwargs.get("max_tokens", 2048)
            )
            response = self.client.models.generate_content(
                model=model or self.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            print(f"[ERROR] Gemini generation error: {e}")
            return None

    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Optional[str]:
        """Chat with Gemini using message history"""
        if not self.available:
            return None
        try:
            from google.genai import types
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

            config = types.GenerateContentConfig(
                temperature=kwargs.get("temperature", 0.7),
                max_output_tokens=kwargs.get("max_tokens", 2048)
            )
            response = self.client.models.generate_content(
                model=model or self.model_name,
                contents=contents,
                config=config
            )
            return response.text
        except Exception as e:
            print(f"[ERROR] Gemini chat error: {e}")
            return None


class ClaudeIntegration:
    """Integration with Claude AI via Anthropic SDK"""

    def __init__(self, api_key: Optional[str] = None, credentials_path: str = r"C:\Users\SHAD\.claude\.credentials.json"):
        self.credentials_path = Path(credentials_path)
        self.credentials = self._load_credentials()
        self.client = None
        self.available = False
        self.model_name = "claude-sonnet-4-5-20250929"

        try:
            import anthropic

            key = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not key:
                env_path = Path(r"C:\Users\SHAD\.env")
                if env_path.exists():
                    for line in env_path.read_text().splitlines():
                        if line.startswith("ANTHROPIC_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break

            if not key:
                print("[WARN]  Claude: no API key found (set ANTHROPIC_API_KEY env var)")
                return

            self.client = anthropic.Anthropic(api_key=key)
            self.available = True
        except Exception as e:
            print(f"[WARN]  Claude SDK unavailable: {e}")

    def _load_credentials(self) -> Optional[Dict]:
        """Load Claude AI OAuth credentials (for status info)"""
        if not self.credentials_path.exists():
            return None
        try:
            with open(self.credentials_path, 'r') as f:
                data = json.load(f)
                return data.get('claudeAiOauth')
        except Exception:
            return None

    def get_access_token(self) -> Optional[str]:
        if self.credentials:
            return self.credentials.get('accessToken')
        return None

    def is_token_valid(self) -> bool:
        if not self.credentials:
            return False
        import time
        expires_at = self.credentials.get('expiresAt', 0)
        return int(time.time() * 1000) < expires_at

    def get_subscription_type(self) -> Optional[str]:
        if self.credentials:
            return self.credentials.get('subscriptionType')
        return None

    def generate(self, prompt: str, model: str = None, **kwargs) -> Optional[str]:
        """Generate text using Claude API"""
        if not self.available:
            return None
        try:
            message = self.client.messages.create(
                model=model or self.model_name,
                max_tokens=kwargs.get("max_tokens", 2048),
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"[ERROR] Claude generation error: {e}")
            return None

    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Optional[str]:
        """Chat with Claude using message history"""
        if not self.available:
            return None
        try:
            message = self.client.messages.create(
                model=model or self.model_name,
                max_tokens=kwargs.get("max_tokens", 2048),
                messages=messages
            )
            return message.content[0].text
        except Exception as e:
            print(f"[ERROR] Claude chat error: {e}")
            return None


class OpenAIIntegration:
    """Integration with OpenAI (ChatGPT) via openai SDK"""

    def __init__(self, api_key: Optional[str] = None):
        self.available = False
        self.client = None
        self.model_name = "gpt-4o-mini"

        try:
            import openai

            key = api_key or os.environ.get("OPENAI_API_KEY")
            if not key:
                # Try api_key.txt
                key_file = Path(r"C:\Users\SHAD\api_key.txt")
                if key_file.exists():
                    key = key_file.read_text().strip()
                else:
                    # Try .env
                    env_path = Path(r"C:\Users\SHAD\.env")
                    if env_path.exists():
                        for line in env_path.read_text().splitlines():
                            if line.startswith("OPENAI_API_KEY="):
                                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                                break

            if not key:
                print("[WARN]  OpenAI: no API key found (set OPENAI_API_KEY env var)")
                return

            self.client = openai.OpenAI(api_key=key)
            self.available = True
        except Exception as e:
            print(f"[WARN]  OpenAI SDK unavailable: {e}")

    def generate(self, prompt: str, model: str = None, **kwargs) -> Optional[str]:
        """Generate text using OpenAI ChatGPT"""
        if not self.available:
            return None
        try:
            response = self.client.chat.completions.create(
                model=model or self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048)
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[ERROR] OpenAI generation error: {e}")
            return None

    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> Optional[str]:
        """Chat with OpenAI using message history"""
        if not self.available:
            return None
        try:
            response = self.client.chat.completions.create(
                model=model or self.model_name,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048)
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[ERROR] OpenAI chat error: {e}")
            return None


class UltimaSystem:
    """
    Unified AI Integration System

    Combines Ollama, Dolphin, Gemini CLI, and Claude AI into a single interface
    """

    def __init__(self):
        print(">>> Initializing ULTIMA_SYSTEM...")

        self.ollama = OllamaIntegration()
        self.dolphin = DolphinIntegration()
        self.gemini = GeminiIntegration()
        self.claude = ClaudeIntegration()
        self.openai = OpenAIIntegration()

        self._print_status()

    def _print_status(self):
        """Print integration status"""
        print("\n" + "="*60)
        print("ULTIMA_SYSTEM - Integration Status")
        print("="*60)

        print(f"[Ollama]     {'[OK]' if self.ollama.available else '[FAIL]'}")
        if self.ollama.available:
            models = self.ollama.list_models()
            if models:
                print(f"   Models: {', '.join(models[:3])}{' ...' if len(models) > 3 else ''}")

        print(f"[Dolphin]    {'[OK]' if self.dolphin.available else '[FAIL]'}")
        if self.dolphin.available:
            print(f"   Path: {self.dolphin.dolphin_path}")

        print(f"[Gemini]     {'[OK]' if self.gemini.available else '[FAIL]'}")
        if self.gemini.available:
            print(f"   Model: {self.gemini.model_name}")

        print(f"[Claude AI]  {'[OK]' if self.claude.available else '[FAIL]'}")
        if self.claude.available:
            print(f"   Model: {self.claude.model_name}")

        print(f"[OpenAI]     {'[OK]' if self.openai.available else '[FAIL]'}")
        if self.openai.available:
            print(f"   Model: {self.openai.model_name}")

        print("="*60 + "\n")

    def generate(self, prompt: str, provider: str = "auto", **kwargs) -> Optional[str]:
        """
        Generate text using specified provider

        Args:
            prompt: Input prompt
            provider: "ollama", "gemini", "claude", "openai", "auto"
            **kwargs: Provider-specific parameters (model, temperature, max_tokens)

        Returns:
            Generated text or None
        """
        providers = {
            "ollama": self._gen_ollama,
            "gemini": self._gen_gemini,
            "claude": self._gen_claude,
            "openai": self._gen_openai,
        }

        if provider != "auto":
            fn = providers.get(provider)
            if not fn:
                print(f"[ERROR] Unknown provider: {provider}")
                return None
            return fn(prompt, **kwargs)

        # auto: try in priority order from config
        for name in ["claude", "openai", "gemini", "ollama"]:
            result = providers[name](prompt, **kwargs)
            if result:
                return result

        print("[ERROR] No provider available for generation")
        return None

    def _gen_ollama(self, prompt: str, **kwargs) -> Optional[str]:
        if not self.ollama.available:
            return None
        return self.ollama.generate(kwargs.get('model', 'llama2'), prompt, **kwargs)

    def _gen_gemini(self, prompt: str, **kwargs) -> Optional[str]:
        if not self.gemini.available:
            return None
        return self.gemini.generate(prompt, **kwargs)

    def _gen_claude(self, prompt: str, **kwargs) -> Optional[str]:
        if not self.claude.available:
            return None
        return self.claude.generate(prompt, **kwargs)

    def _gen_openai(self, prompt: str, **kwargs) -> Optional[str]:
        if not self.openai.available:
            return None
        return self.openai.generate(prompt, **kwargs)

    def status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        return {
            "system": "ULTIMA_SYSTEM",
            "version": "1.0.0",
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "integrations": {
                "ollama": {
                    "available": self.ollama.available,
                    "models": self.ollama.list_models() if self.ollama.available else []
                },
                "dolphin": {
                    "available": self.dolphin.available,
                    "path": str(self.dolphin.dolphin_path) if self.dolphin.available else None
                },
                "gemini": {
                    "available": self.gemini.available,
                    "model": self.gemini.model_name if self.gemini.available else None
                },
                "claude": {
                    "available": self.claude.available,
                    "model": self.claude.model_name if self.claude.available else None
                },
                "openai": {
                    "available": self.openai.available,
                    "model": self.openai.model_name if self.openai.available else None
                }
            }
        }


# Example usage
if __name__ == "__main__":
    # Initialize system
    system = UltimaSystem()

    # Get status report
    status = system.status_report()
    print("\n>>> Status Report:")
    print(json.dumps(status, indent=2))
