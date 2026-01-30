"""
ULTIMA_SYSTEM - Usage Examples
IMPULSE REBIRTH [ 2026 ]

Practical examples of using the integrated AI systems
"""

import json
import asyncio
from integrations import UltimaSystem, OllamaIntegration, DolphinIntegration, GeminiIntegration, ClaudeIntegration


def example_1_status_check():
    """Example 1: Check integration status"""
    print("="*60)
    print("Example 1: Status Check")
    print("="*60)

    system = UltimaSystem()
    status = system.status_report()

    print("\nIntegration Summary:")
    for name, info in status['integrations'].items():
        available = info.get('available', False)
        print(f"  {name.capitalize()}: {'[OK]' if available else '[FAIL]'}")

    print("\nFull Report:")
    print(json.dumps(status, indent=2))


def example_2_ollama_basic():
    """Example 2: Basic Ollama usage"""
    print("\n" + "="*60)
    print("Example 2: Ollama Basic Usage")
    print("="*60)

    ollama = OllamaIntegration()

    if not ollama.available:
        print("[WARN] Ollama not available - skipping")
        return

    # List models
    print("\nAvailable models:")
    models = ollama.list_models()
    if models:
        for model in models:
            print(f"  - {model}")
    else:
        print("  No models found. Run: ollama pull llama2")
        return

    # Simple generation
    print("\nGenerating response...")
    response = ollama.generate(
        model=models[0],
        prompt="In one sentence, what is AI?"
    )

    if response:
        print(f"\nResponse: {response}")


async def example_3_ollama_async():
    """Example 3: Async Ollama generation"""
    print("\n" + "="*60)
    print("Example 3: Ollama Async Generation")
    print("="*60)

    ollama = OllamaIntegration()

    if not ollama.available:
        print("[WARN] Ollama not available - skipping")
        return

    models = ollama.list_models()
    if not models:
        print("[WARN] No models available - skipping")
        return

    print("\nGenerating async response...")
    response = await ollama.generate_async(
        model=models[0],
        prompt="Explain machine learning in one sentence."
    )

    if response:
        print(f"\nResponse: {response}")


def example_4_dolphin_scripts():
    """Example 4: Dolphin script execution"""
    print("\n" + "="*60)
    print("Example 4: Dolphin Script Execution")
    print("="*60)

    dolphin = DolphinIntegration()

    if not dolphin.available:
        print("[WARN] Dolphin not available - skipping")
        return

    print(f"\nDolphin path: {dolphin.dolphin_path}")

    # List available scripts
    scripts_dir = dolphin.dolphin_path / "scripts"
    if scripts_dir.exists():
        print("\nAvailable scripts:")
        scripts = list(scripts_dir.glob("*.mjs"))
        for script in scripts[:5]:  # Show first 5
            print(f"  - {script.name}")

    # Example: Run dolphin command
    print("\nRunning dolphin command...")
    result = dolphin.dolphin_command("--help")
    if result:
        print(result[:200])  # Show first 200 chars


def example_5_gemini_generation():
    """Example 5: Gemini CLI text generation"""
    print("\n" + "="*60)
    print("Example 5: Gemini CLI Generation")
    print("="*60)

    gemini = GeminiIntegration()

    if not gemini.available:
        print("[WARN] Gemini CLI not available")
        print("Fix: Add C:\\Users\\SHAD\\AppData\\Roaming\\npm to PATH")
        return

    # Get version
    version = gemini.get_version()
    print(f"\nGemini CLI version: {version}")

    # Generate text
    print("\nGenerating response...")
    response = gemini.generate(
        prompt="What is quantum computing?",
        model="gemini-2.0-flash-exp",
        temperature=0.7
    )

    if response:
        print(f"\nResponse:\n{response}")


def example_6_claude_status():
    """Example 6: Claude AI status"""
    print("\n" + "="*60)
    print("Example 6: Claude AI Status")
    print("="*60)

    claude = ClaudeIntegration()

    if not claude.available:
        print("[WARN] Claude credentials not found")
        return

    # Show status
    print(f"\nSubscription: {claude.get_subscription_type()}")
    print(f"Token valid: {claude.is_token_valid()}")

    token = claude.get_access_token()
    if token:
        print(f"Token (first 20 chars): {token[:20]}...")


def example_7_unified_system():
    """Example 7: Unified system auto-selection"""
    print("\n" + "="*60)
    print("Example 7: Unified System (Auto Provider)")
    print("="*60)

    system = UltimaSystem()

    # Auto-select best provider
    prompt = "What is deep learning?"
    print(f"\nPrompt: {prompt}")
    print("Auto-selecting best available provider...")

    result = system.generate(prompt, provider="auto")

    if result:
        print(f"\nResponse:\n{result}")
    else:
        print("\n[WARN] No providers available for generation")


def example_8_ollama_chat():
    """Example 8: Ollama chat mode"""
    print("\n" + "="*60)
    print("Example 8: Ollama Chat Mode")
    print("="*60)

    ollama = OllamaIntegration()

    if not ollama.available:
        print("[WARN] Ollama not available - skipping")
        return

    models = ollama.list_models()
    if not models:
        print("[WARN] No models available - skipping")
        return

    # Chat conversation
    messages = [
        {"role": "user", "content": "What is AI?"},
        {"role": "assistant", "content": "AI is artificial intelligence."},
        {"role": "user", "content": "Give me one real-world example."}
    ]

    print("\nChat conversation:")
    for msg in messages:
        print(f"  {msg['role']}: {msg['content']}")

    print("\nGenerating assistant response...")
    response = ollama.chat(model=models[0], messages=messages)

    if response:
        print(f"\nAssistant: {response}")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*80)
    print(" "*20 + "ULTIMA_SYSTEM - Examples")
    print("="*80)

    # Synchronous examples
    example_1_status_check()
    example_2_ollama_basic()
    example_4_dolphin_scripts()
    example_5_gemini_generation()
    example_6_claude_status()
    example_7_unified_system()
    example_8_ollama_chat()

    # Async example
    print("\n" + "="*60)
    print("Running async example...")
    print("="*60)
    asyncio.run(example_3_ollama_async())

    print("\n" + "="*80)
    print("All examples completed!")
    print("="*80)


if __name__ == "__main__":
    # Run specific example
    # example_1_status_check()

    # Or run all examples
    run_all_examples()
