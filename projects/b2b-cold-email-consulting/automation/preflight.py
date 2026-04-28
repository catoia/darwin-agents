#!/usr/bin/env python3
"""
Pre-flight check: Validates API keys and configuration before launch.
Run this before your first campaign to catch issues early.
"""

import os
import sys
import json

def check_env_var(name):
    """Check if environment variable is set and not placeholder."""
    value = os.getenv(name)
    if not value:
        return False, "Not set"
    if "YOUR_" in value or "xxxxx" in value:
        return False, "Still using template value"
    return True, "✓ Set"

def check_sendgrid():
    """Test SendGrid API key."""
    try:
        import requests
        api_key = os.getenv('SENDGRID_API_KEY')
        if not api_key:
            return False, "API key not set"
        
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get('https://api.sendgrid.com/v3/scopes', headers=headers, timeout=5)
        
        if response.status_code == 200:
            return True, "✓ Valid (authenticated)"
        elif response.status_code == 401:
            return False, "Invalid API key"
        else:
            return False, f"Unexpected response: {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_openai():
    """Test OpenAI API key."""
    try:
        from openai import OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return False, "API key not set"
        
        client = OpenAI(api_key=api_key)
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return True, "✓ Valid (authenticated)"
    except Exception as e:
        if "incorrect" in str(e).lower() or "invalid" in str(e).lower():
            return False, "Invalid API key"
        return False, f"Error: {str(e)}"

def check_config():
    """Check config.json is properly configured."""
    try:
        with open('automation/config.json') as f:
            config = json.load(f)
        
        issues = []
        
        if config['from_email'] == 'nuno@example.com':
            issues.append("from_email still set to default")
        
        if not config['from_email'] or '@' not in config['from_email']:
            issues.append("from_email invalid")
        
        if not config['from_name']:
            issues.append("from_name not set")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, f"✓ Configured ({config['from_email']})"
    except Exception as e:
        return False, f"Error reading config: {str(e)}"

def check_dependencies():
    """Check Python dependencies are installed."""
    try:
        import requests
        import sendgrid
        import openai
        import sqlite3
        return True, "✓ All dependencies installed"
    except ImportError as e:
        return False, f"Missing: {str(e)}"

def main():
    print("\n" + "="*60)
    print("🚀 B2B COLD EMAIL AUTOMATION - PRE-FLIGHT CHECK")
    print("="*60 + "\n")
    
    checks = [
        ("Python Dependencies", check_dependencies),
        ("Configuration File", check_config),
        ("SENDGRID_API_KEY", lambda: check_env_var('SENDGRID_API_KEY')),
        ("OPENAI_API_KEY", lambda: check_env_var('OPENAI_API_KEY')),
        ("SendGrid Connection", check_sendgrid),
        ("OpenAI Connection", check_openai),
    ]
    
    optional_checks = [
        ("APOLLO_API_KEY (optional)", lambda: check_env_var('APOLLO_API_KEY')),
        ("HUNTER_API_KEY (optional)", lambda: check_env_var('HUNTER_API_KEY')),
    ]
    
    all_passed = True
    
    # Required checks
    print("Required Checks:")
    print("-" * 60)
    for name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✅" if passed else "❌"
            print(f"{status} {name:<30} {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {name:<30} Error: {str(e)}")
            all_passed = False
    
    print("\n")
    
    # Optional checks
    print("Optional Checks (improve prospect finding):")
    print("-" * 60)
    for name, check_func in optional_checks:
        try:
            passed, message = check_func()
            status = "✅" if passed else "⚠️ "
            print(f"{status} {name:<30} {message}")
        except Exception as e:
            print(f"⚠️  {name:<30} Error: {str(e)}")
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✅ ALL CHECKS PASSED - READY TO LAUNCH")
        print("="*60)
        print("\nNext step:")
        print("  python3 automation/orchestrator.py initial 20")
        print("\n")
        sys.exit(0)
    else:
        print("❌ SOME CHECKS FAILED - FIX ISSUES BEFORE LAUNCH")
        print("="*60)
        print("\nCommon fixes:")
        print("  • Make sure you've run: source automation/.env")
        print("  • Edit automation/.env with your actual API keys")
        print("  • Edit automation/config.json with your email/name")
        print("  • Run: pip install -r automation/requirements.txt")
        print("\nSee GETTING-STARTED.md for full setup instructions.")
        print("\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
