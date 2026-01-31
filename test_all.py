"""
ULTIMA_SYSTEM - Comprehensive Integration Tests
Tests all 4 AI integrations
"""

import json
import sys
from integrations import (
    UltimaSystem,
    OllamaIntegration,
    DolphinIntegration,
    GeminiIntegration,
    ClaudeIntegration
)


def print_header(title):
    """Print test section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_result(test_name, passed, details=""):
    """Print test result"""
    status = "[PASS]" if passed else "[FAIL]"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {test_name}")
    if details:
        print(f"      {details}")


def test_ollama():
    """Test Ollama integration"""
    print_header("TEST 1: Ollama Integration")

    ollama = OllamaIntegration()

    # Test 1: Package available
    print_result("Ollama package import", ollama.available)

    if not ollama.available:
        print("      Skipping further Ollama tests (package not available)")
        return False

    # Test 2: List models (will fail if service not running)
    try:
        models = ollama.list_models()
        has_models = len(models) > 0
        print_result("List models", has_models, f"Found {len(models)} models" if has_models else "No models (service may not be running)")

        # Test 3: Generate (only if models available)
        if has_models:
            try:
                response = ollama.generate(
                    model=models[0],
                    prompt="Say 'test' in one word",
                    stream=False
                )
                generated = response is not None and len(str(response)) > 0
                print_result("Generate text", generated, f"Response: {str(response)[:50]}..." if generated else "No response")
            except Exception as e:
                print_result("Generate text", False, f"Error: {str(e)[:50]}")
        else:
            print("      Skipping generation test (no models)")

    except Exception as e:
        print_result("List models", False, f"Service not running: {str(e)[:50]}")

    return True


def test_dolphin():
    """Test Dolphin integration"""
    print_header("TEST 2: Dolphin Integration")

    dolphin = DolphinIntegration()

    # Test 1: Path exists
    print_result("Dolphin path exists", dolphin.available,
                 f"Path: {dolphin.dolphin_path}" if dolphin.available else "Path not found")

    if not dolphin.available:
        return False

    # Test 2: Scripts directory
    scripts_dir = dolphin.dolphin_path / "scripts"
    scripts_exist = scripts_dir.exists()
    print_result("Scripts directory", scripts_exist,
                 f"Location: {scripts_dir}" if scripts_exist else "Not found")

    # Test 3: List scripts
    if scripts_exist:
        scripts = list(scripts_dir.glob("*.mjs"))
        print_result("Found scripts", len(scripts) > 0,
                     f"Found {len(scripts)} scripts")

        # Show first 5 scripts
        if scripts:
            print("      Available scripts:")
            for script in scripts[:5]:
                print(f"        - {script.name}")

    # Test 4: Run dolphin help
    try:
        result = dolphin.dolphin_command("--help")
        help_works = result is not None and "Usage:" in result
        print_result("Dolphin command execution", help_works,
                     f"Output length: {len(result) if result else 0} chars")
    except Exception as e:
        print_result("Dolphin command execution", False, f"Error: {str(e)[:50]}")

    return True


def test_gemini():
    """Test Gemini CLI integration"""
    print_header("TEST 3: Gemini CLI Integration")

    gemini = GeminiIntegration()

    # Test 1: CLI available
    print_result("Gemini CLI in PATH", gemini.available,
                 "CLI found" if gemini.available else "Not in PATH")

    if not gemini.available:
        # Try direct path
        import subprocess
        try:
            result = subprocess.run(
                [r"C:\Users\SHAD\AppData\Roaming\npm\gemini", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print_result("Gemini CLI (direct path)", True,
                             f"Version: {result.stdout.strip()}")
                print("      Note: Add to PATH for full integration")
        except Exception as e:
            print_result("Gemini CLI (direct path)", False, str(e)[:50])
        return False

    # Test 2: Version check
    version = gemini.get_version()
    print_result("Get version", version is not None,
                 f"Version: {version}" if version else "Failed")

    # Test 3: Generate (may fail if API key not configured)
    print("      Note: Generation test requires API key configuration")

    return True


def test_claude():
    """Test Claude AI integration"""
    print_header("TEST 4: Claude AI Integration")

    claude = ClaudeIntegration()

    # Test 1: Credentials loaded
    print_result("Credentials loaded", claude.available,
                 "Found at: C:\\Users\\SHAD\\.claude\\.credentials.json" if claude.available else "Not found")

    if not claude.available:
        return False

    # Test 2: Access token
    token = claude.get_access_token()
    has_token = token is not None and len(token) > 0
    print_result("Access token", has_token,
                 f"Token: {token[:20]}..." if has_token else "No token")

    # Test 3: Token validity
    is_valid = claude.is_token_valid()
    print_result("Token valid", is_valid,
                 "Valid" if is_valid else "Expired")

    # Test 4: Subscription info
    sub = claude.get_subscription_type()
    print_result("Subscription type", sub is not None,
                 f"Type: {sub}" if sub else "Unknown")

    return True


def test_unified_system():
    """Test unified system"""
    print_header("TEST 5: Unified System")

    try:
        system = UltimaSystem()
        print_result("System initialization", True, "UltimaSystem created")
    except Exception as e:
        print_result("System initialization", False, str(e))
        return False

    # Test status report
    try:
        status = system.status_report()
        has_status = status is not None and 'integrations' in status
        print_result("Status report", has_status,
                     f"Found {len(status.get('integrations', {}))} integrations" if has_status else "Failed")

        if has_status:
            print("\n      Integration status:")
            for name, info in status['integrations'].items():
                available = info.get('available', False)
                status_str = "[OK]" if available else "[FAIL]"
                print(f"        {name}: {status_str}")
    except Exception as e:
        print_result("Status report", False, str(e)[:50])

    return True


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("  ULTIMA_SYSTEM - Comprehensive Integration Test Suite")
    print("="*70)
    print(f"  Testing 4 AI integrations + unified system")
    print("="*70)

    results = []

    # Run individual tests
    results.append(("Ollama", test_ollama()))
    results.append(("Dolphin", test_dolphin()))
    results.append(("Gemini CLI", test_gemini()))
    results.append(("Claude AI", test_claude()))
    results.append(("Unified System", test_unified_system()))

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nTests passed: {passed}/{total}")
    print("\nDetailed results:")
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")

    # Overall status
    print("\n" + "="*70)
    if passed == total:
        print("  Overall Status: ALL TESTS PASSED")
    else:
        print(f"  Overall Status: {passed}/{total} PASSED, {total-passed} FAILED")
    print("="*70)

    # Action items
    print("\nAction Items:")

    # Check Ollama
    if not any(name == "Ollama" and result for name, result in results):
        print("  [ ] Start Ollama service or install models")

    # Check Gemini
    if not any(name == "Gemini CLI" and result for name, result in results):
        print("  [ ] Add Gemini CLI to PATH")
        print("      Path: C:\\Users\\SHAD\\AppData\\Roaming\\npm")

    print("\n")
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
