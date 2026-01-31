"""
Detailed Dolphin Integration Test
"""

from integrations import DolphinIntegration
import json

print("="*70)
print("  DOLPHIN INTEGRATION - Detailed Test")
print("="*70)

dolphin = DolphinIntegration()

if not dolphin.available:
    print("[FAIL] Dolphin not available")
    exit(1)

print(f"\n[OK] Dolphin path: {dolphin.dolphin_path}")

# List all scripts
scripts_dir = dolphin.dolphin_path / "scripts"
print(f"\n[OK] Scripts directory: {scripts_dir}")

if scripts_dir.exists():
    scripts = sorted(scripts_dir.glob("*.mjs"))
    print(f"\n[OK] Found {len(scripts)} scripts:\n")

    for i, script in enumerate(scripts, 1):
        print(f"  {i:2}. {script.name}")

# Test main dolphin command
print("\n" + "="*70)
print("  Testing: dolphin.mjs --help")
print("="*70)

result = dolphin.dolphin_command("--help")
if result:
    print("[OK] Command executed successfully")
    print(f"\nOutput:\n{result}")
else:
    print("[FAIL] Command failed")

# Check package.json
print("\n" + "="*70)
print("  Dolphin Project Info")
print("="*70)

package_json = dolphin.dolphin_path / "package.json"
if package_json.exists():
    with open(package_json, 'r') as f:
        pkg = json.load(f)

    print(f"\n[OK] Project: {pkg.get('name', 'Unknown')}")
    print(f"[OK] Version: {pkg.get('version', 'Unknown')}")

    scripts = pkg.get('scripts', {})
    print(f"\n[OK] Available npm scripts ({len(scripts)}):\n")

    for name, cmd in sorted(scripts.items()):
        print(f"  - {name:20} -> {cmd[:50]}")

print("\n" + "="*70)
print("  DOLPHIN TEST COMPLETE")
print("="*70)
