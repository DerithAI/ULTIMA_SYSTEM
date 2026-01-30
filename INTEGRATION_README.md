# 🔗 ULTIMA_SYSTEM Integrations

**IMPULSE REBIRTH [ 2026 ]**

Unified AI Integration Platform - connecting Ollama, Dolphin, Gemini CLI, and Claude AI

---

## 📊 Current Status

### Integration Health

```
[Ollama]     [OK]     - Python package available
                      - Service needs to be started
                      - Models: Run `ollama serve` first

[Dolphin]    [OK]     - Project located
                      - Scripts available
                      - Path: E:\[ PROJECTS ]\[ LOCAL ]\[ CODEX ] PC\[ DOLPHIN ]

[Gemini CLI] [FAIL]   - CLI not in PATH
                      - Version: 0.27.0-nightly detected at npm location
                      - Fix: Add to PATH or use full path

[Claude AI]  [OK]     - Credentials loaded
                      - Subscription: Pro
                      - Token: Valid
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install ollama
```

### 2. Start Ollama Service

```bash
# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull llama2
```

### 3. Fix Gemini CLI PATH

```bash
# Add to PATH or create alias
# Location: C:\Users\SHAD\AppData\Roaming\npm\gemini
```

### 4. Use ULTIMA_SYSTEM

```python
from integrations import UltimaSystem

# Initialize system
system = UltimaSystem()

# Get status
status = system.status_report()
print(status)

# Generate text (auto-selects best available provider)
result = system.generate("Explain AI in simple terms")
print(result)
```

---

## 📖 Usage Examples

### Ollama Integration

```python
from integrations import OllamaIntegration

ollama = OllamaIntegration()

# List available models
models = ollama.list_models()
print(f"Available models: {models}")

# Generate text
response = ollama.generate(
    model="llama2",
    prompt="What is quantum computing?"
)
print(response)

# Chat
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "Tell me about AI"}
]
response = ollama.chat(model="llama2", messages=messages)
print(response)

# Async generation
import asyncio

async def async_example():
    result = await ollama.generate_async(
        model="llama2",
        prompt="Explain machine learning"
    )
    print(result)

asyncio.run(async_example())
```

### Dolphin Integration

```python
from integrations import DolphinIntegration

dolphin = DolphinIntegration()

# Run dolphin command
result = dolphin.dolphin_command("status")
print(result)

# Start agent watch
dolphin.agent_watch()

# Create new idea
idea = {
    "title": "New Feature Idea",
    "description": "Description of the idea",
    "tags": ["feature", "enhancement"]
}
result = dolphin.create_idea(idea)
print(result)

# Run custom script
result = dolphin.run_script("light-scan.mjs")
print(result)
```

### Gemini CLI Integration

```python
from integrations import GeminiIntegration

gemini = GeminiIntegration()

# Check version
version = gemini.get_version()
print(f"Gemini CLI version: {version}")

# Generate text
response = gemini.generate(
    prompt="Explain neural networks",
    model="gemini-2.0-flash-exp",
    temperature=0.7
)
print(response)

# Chat
response = gemini.chat("What is deep learning?")
print(response)
```

### Claude AI Integration

```python
from integrations import ClaudeIntegration

claude = ClaudeIntegration()

# Get access token
token = claude.get_access_token()
print(f"Token: {token[:20]}...")

# Check token validity
is_valid = claude.is_token_valid()
print(f"Token valid: {is_valid}")

# Get subscription
sub = claude.get_subscription_type()
print(f"Subscription: {sub}")
```

### Unified System

```python
from integrations import UltimaSystem

system = UltimaSystem()

# Auto-select best provider
result = system.generate(
    prompt="What is artificial intelligence?",
    provider="auto"  # Tries gemini -> ollama -> claude
)
print(result)

# Use specific provider
result = system.generate(
    prompt="Explain machine learning",
    provider="ollama",
    model="llama2"
)
print(result)

# Get comprehensive status
status = system.status_report()
print(json.dumps(status, indent=2))
```

---

## 🔧 Configuration

Edit `config.json` to customize settings:

```json
{
  "integrations": {
    "ollama": {
      "enabled": true,
      "base_url": "http://localhost:11434",
      "default_model": "llama2"
    },
    "dolphin": {
      "enabled": true,
      "path": "E:\\[ PROJECTS ]\\[ LOCAL ]\\[ CODEX ] PC\\[ DOLPHIN ]"
    },
    "gemini": {
      "enabled": true,
      "default_model": "gemini-2.0-flash-exp"
    },
    "claude": {
      "enabled": true,
      "credentials_path": "C:\\Users\\SHAD\\.claude\\.credentials.json"
    }
  }
}
```

---

## 🐛 Troubleshooting

### Ollama Not Running

**Error:** `Failed to connect to Ollama`

**Solution:**
```bash
# Start Ollama service
ollama serve

# Or on Windows, start Ollama from Start Menu
```

### Gemini CLI Not Found

**Error:** `Gemini CLI not available in PATH`

**Solution:**
```bash
# Option 1: Add to PATH
export PATH="$PATH:C:\Users\SHAD\AppData\Roaming\npm"

# Option 2: Use full path in code
gemini = GeminiIntegration()
# Modify CLI command in config.json
```

### Dolphin Scripts Not Found

**Error:** `Dolphin script not found`

**Solution:**
```bash
# Check Dolphin path
ls "E:\[ PROJECTS ]\[ LOCAL ]\[ CODEX ] PC\[ DOLPHIN ]\scripts"

# Update path in config.json if needed
```

### Claude Token Expired

**Error:** `Token: [EXPIRED]`

**Solution:**
- Log in to Claude Code CLI again
- Credentials will be refreshed automatically

---

## 📝 API Reference

### UltimaSystem

#### `__init__()`
Initialize all integrations

#### `generate(prompt, provider="auto", **kwargs)`
Generate text using specified provider

**Args:**
- `prompt` (str): Input prompt
- `provider` (str): "auto", "ollama", "gemini", or "claude"
- `**kwargs`: Provider-specific parameters

**Returns:**
- `str | None`: Generated text

#### `status_report()`
Get comprehensive status of all integrations

**Returns:**
- `dict`: Status report

### OllamaIntegration

#### `list_models()`
List available Ollama models

#### `generate(model, prompt, **kwargs)`
Generate text with Ollama

#### `generate_async(model, prompt, **kwargs)`
Async text generation

#### `chat(model, messages, **kwargs)`
Chat with Ollama model

### DolphinIntegration

#### `run_script(script_name, *args)`
Run Dolphin script

#### `dolphin_command(*args)`
Run main dolphin.mjs

#### `agent_watch()`
Start agent watch mode

#### `create_idea(idea_data)`
Create new idea

### GeminiIntegration

#### `get_version()`
Get Gemini CLI version

#### `generate(prompt, model, **kwargs)`
Generate text with Gemini

#### `chat(message, **kwargs)`
Chat with Gemini

### ClaudeIntegration

#### `get_access_token()`
Get Claude access token

#### `is_token_valid()`
Check token validity

#### `get_subscription_type()`
Get subscription type

---

## 🎯 Next Steps

### Immediate Fixes
1. Start Ollama service: `ollama serve`
2. Fix Gemini CLI PATH
3. Pull Ollama models: `ollama pull llama2`

### Enhancements
1. Add error recovery
2. Implement caching
3. Add logging
4. Create web interface
5. Add batch processing

---

## 📚 Related Files

- `integrations.py` - Main integration code
- `config.json` - Configuration
- `ROADMAP.md` - Future plans
- `TODO.md` - Task list

---

**Created:** 2026-01-30
**Version:** 1.0.0
**Status:** ✅ Operational (3/4 integrations working)
