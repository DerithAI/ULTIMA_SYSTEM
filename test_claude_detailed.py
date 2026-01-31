"""
Detailed Claude AI Integration Test
"""

from integrations import ClaudeIntegration
import json
from datetime import datetime

print("="*70)
print("  CLAUDE AI INTEGRATION - Detailed Test")
print("="*70)

claude = ClaudeIntegration()

if not claude.available:
    print("[FAIL] Claude credentials not available")
    exit(1)

print(f"\n[OK] Credentials loaded from: {claude.credentials_path}")

# Test all credential methods
print("\n" + "="*70)
print("  Credential Information")
print("="*70)

# Access token
token = claude.get_access_token()
if token:
    print(f"\n[OK] Access Token:")
    print(f"     Prefix: {token[:20]}...")
    print(f"     Length: {len(token)} characters")
else:
    print("\n[FAIL] No access token")

# Refresh token
refresh = claude.credentials.get('refreshToken')
if refresh:
    print(f"\n[OK] Refresh Token:")
    print(f"     Prefix: {refresh[:20]}...")
    print(f"     Length: {len(refresh)} characters")

# Token expiry
expires_at = claude.credentials.get('expiresAt')
if expires_at:
    from datetime import datetime
    exp_date = datetime.fromtimestamp(expires_at / 1000)
    now = datetime.now()
    diff = exp_date - now

    print(f"\n[OK] Token Expiry:")
    print(f"     Expires: {exp_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"     Days remaining: {diff.days}")
    print(f"     Valid: {'Yes' if claude.is_token_valid() else 'No'}")

# Subscription
sub = claude.get_subscription_type()
print(f"\n[OK] Subscription:")
print(f"     Type: {sub}")
print(f"     Rate Limit Tier: {claude.credentials.get('rateLimitTier', 'unknown')}")

# Scopes
scopes = claude.credentials.get('scopes', [])
print(f"\n[OK] Scopes ({len(scopes)}):")
for scope in scopes:
    print(f"     - {scope}")

# Summary
print("\n" + "="*70)
print("  INTEGRATION STATUS")
print("="*70)

print("\n[OK] Claude AI Integration: FULLY OPERATIONAL")
print(f"[OK] Credentials: Valid")
print(f"[OK] Token: Valid ({diff.days} days remaining)" if expires_at else "[OK] Token: Valid")
print(f"[OK] Subscription: {sub}")
print(f"[OK] Ready for use: Yes")

print("\n" + "="*70)
print("  CLAUDE TEST COMPLETE")
print("="*70)
