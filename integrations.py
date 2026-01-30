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
    """Integration with Gemini CLI"""

    def __init__(self):
        self.available = self._check_gemini_cli()

        if not self.available:
            print("[WARN]  Gemini CLI not available in PATH")

    def _check_gemini_cli(self) -> bool:
        """Check if Gemini CLI is available"""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def get_version(self) -> Optional[str]:
        """Get Gemini CLI version"""
        if not self.available:
            return None
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"[ERROR] Gemini version error: {e}")
            return None

    def generate(self, prompt: str, model: str = "gemini-2.0-flash-exp", **kwargs) -> Optional[str]:
        """Generate text using Gemini"""
        if not self.available:
            return None

        cmd = ["gemini", "generate", "--model", model]

        # Add optional parameters
        if "temperature" in kwargs:
            cmd.extend(["--temperature", str(kwargs["temperature"])])
        if "max_tokens" in kwargs:
            cmd.extend(["--max-tokens", str(kwargs["max_tokens"])])

        cmd.append(prompt)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            print(f"[ERROR] Gemini generation error: {e}")
            return None

    def chat(self, message: str, **kwargs) -> Optional[str]:
        """Interactive chat with Gemini"""
        if not self.available:
            return None

        try:
            result = subprocess.run(
                ["gemini", "chat", message],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            print(f"[ERROR] Gemini chat error: {e}")
            return None


class ClaudeIntegration:
    """Integration with Claude AI (via credentials)"""

    def __init__(self, credentials_path: str = r"C:\Users\SHAD\.claude\.credentials.json"):
        self.credentials_path = Path(credentials_path)
        self.credentials = self._load_credentials()
        self.available = self.credentials is not None

        if not self.available:
            print(f"[WARN]  Claude credentials not found at: {credentials_path}")

    def _load_credentials(self) -> Optional[Dict]:
        """Load Claude AI credentials"""
        if not self.credentials_path.exists():
            return None

        try:
            with open(self.credentials_path, 'r') as f:
                data = json.load(f)
                return data.get('claudeAiOauth')
        except Exception as e:
            print(f"[ERROR] Error loading Claude credentials: {e}")
            return None

    def get_access_token(self) -> Optional[str]:
        """Get Claude AI access token"""
        if not self.available:
            return None
        return self.credentials.get('accessToken')

    def is_token_valid(self) -> bool:
        """Check if access token is still valid"""
        if not self.available:
            return False

        import time
        expires_at = self.credentials.get('expiresAt', 0)
        current_time = int(time.time() * 1000)
        return current_time < expires_at

    def get_subscription_type(self) -> Optional[str]:
        """Get Claude subscription type"""
        if not self.available:
            return None
        return self.credentials.get('subscriptionType')


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

        print(f"[Gemini CLI] {'[OK]' if self.gemini.available else '[FAIL]'}")
        if self.gemini.available:
            version = self.gemini.get_version()
            print(f"   Version: {version}")

        print(f"[Claude AI]  {'[OK]' if self.claude.available else '[FAIL]'}")
        if self.claude.available:
            sub_type = self.claude.get_subscription_type()
            token_valid = self.claude.is_token_valid()
            print(f"   Subscription: {sub_type}")
            print(f"   Token: {'[VALID]' if token_valid else '[EXPIRED]'}")

        print("="*60 + "\n")

    def generate(self, prompt: str, provider: str = "auto", **kwargs) -> Optional[str]:
        """
        Generate text using specified provider

        Args:
            prompt: Input prompt
            provider: "ollama", "gemini", "auto" (default)
            **kwargs: Provider-specific parameters

        Returns:
            Generated text or None
        """
        if provider == "ollama" and self.ollama.available:
            model = kwargs.get('model', 'llama2')
            return self.ollama.generate(model, prompt, **kwargs)

        elif provider == "gemini" and self.gemini.available:
            return self.gemini.generate(prompt, **kwargs)

        elif provider == "auto":
            # Try Gemini first, then Ollama
            if self.gemini.available:
                result = self.gemini.generate(prompt, **kwargs)
                if result:
                    return result

            if self.ollama.available:
                model = kwargs.get('model', 'llama2')
                return self.ollama.generate(model, prompt, **kwargs)

        print(f"[ERROR] No available provider for: {provider}")
        return None

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
                    "version": self.gemini.get_version() if self.gemini.available else None
                },
                "claude": {
                    "available": self.claude.available,
                    "subscription": self.claude.get_subscription_type() if self.claude.available else None,
                    "token_valid": self.claude.is_token_valid() if self.claude.available else False
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
