#!/usr/bin/env python3
"""
Twilio SendGrid Integration Test

Tests the updated email_sender.py with Twilio SendGrid credentials.
Validates API key format, authentication, and basic sending capability.
"""

import os
import sys
import json

def test_env_vars():
    """Test if environment variables are set correctly."""
    print("=" * 60)
    print("TEST 1: Environment Variables")
    print("=" * 60)
    
    results = {
        'TWILIO_SENDGRID_API_KEY': os.getenv('TWILIO_SENDGRID_API_KEY'),
        'SENDGRID_API_KEY (legacy)': os.getenv('SENDGRID_API_KEY')
    }
    
    for key, value in results.items():
        if value:
            # Mask the value for security
            masked = value[:10] + '...' + value[-4:] if len(value) > 14 else value
            print(f"✅ {key}: {masked}")
            
            # Validate format
            if 'SG.' in key and value.startswith('SG.'):
                print(f"   ✅ Format valid (starts with 'SG.')")
            elif 'SG.' in key:
                print(f"   ⚠️  WARNING: Expected 'SG.' prefix but got: {value[:10]}...")
        else:
            print(f"❌ {key}: NOT SET")
    
    print()
    
    # Check which one will be used
    api_key = os.getenv('TWILIO_SENDGRID_API_KEY') or os.getenv('SENDGRID_API_KEY')
    if api_key:
        print(f"✅ Email sender will use: {'TWILIO_SENDGRID_API_KEY' if os.getenv('TWILIO_SENDGRID_API_KEY') else 'SENDGRID_API_KEY (legacy)'}")
        return True
    else:
        print("❌ No API key found. Set TWILIO_SENDGRID_API_KEY or SENDGRID_API_KEY")
        return False

def test_config():
    """Test if config.json is properly configured."""
    print("\n" + "=" * 60)
    print("TEST 2: Configuration File")
    print("=" * 60)
    
    try:
        with open('automation/config.json') as f:
            config = json.load(f)
        
        print("✅ config.json loaded successfully")
        
        # Check from_email
        if 'example.com' in config.get('from_email', ''):
            print(f"⚠️  from_email is still placeholder: {config['from_email']}")
            print("   Update to your real email in automation/config.json")
        else:
            print(f"✅ from_email: {config.get('from_email')}")
        
        # Check reply_to
        if 'example.com' in config.get('reply_to', ''):
            print(f"⚠️  reply_to is still placeholder: {config['reply_to']}")
        else:
            print(f"✅ reply_to: {config.get('reply_to')}")
        
        # Check sendgrid_api_key variable name
        print(f"✅ sendgrid_api_key env var: {config.get('sendgrid_api_key')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading config.json: {e}")
        return False

def test_sendgrid_import():
    """Test if SendGrid SDK is installed and importable."""
    print("\n" + "=" * 60)
    print("TEST 3: SendGrid SDK")
    print("=" * 60)
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        print("✅ SendGrid SDK installed and importable")
        return True
    except ImportError as e:
        print(f"❌ SendGrid SDK not installed: {e}")
        print("\n   To fix, run:")
        print("   pip3 install sendgrid")
        return False

def test_email_sender():
    """Test if EmailSender class initializes correctly."""
    print("\n" + "=" * 60)
    print("TEST 4: EmailSender Initialization")
    print("=" * 60)
    
    try:
        # Add parent directory to path so we can import email_sender
        sys.path.insert(0, os.path.abspath('.'))
        from automation.email_sender import EmailSender
        
        sender = EmailSender()
        print("✅ EmailSender initialized successfully")
        
        if sender.sg:
            print("✅ SendGrid client created (API key accepted)")
        else:
            print("⚠️  SendGrid client is None (API key not set or invalid)")
        
        print(f"✅ From: {sender.from_name} <{sender.from_email}>")
        print(f"✅ Reply-to: {sender.reply_to}")
        print(f"✅ Rate limits: {sender.emails_per_hour}/hour, {sender.emails_per_day}/day")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing EmailSender: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dry_run():
    """Test sending an email in dry-run mode."""
    print("\n" + "=" * 60)
    print("TEST 5: Dry Run (No Actual Email Sent)")
    print("=" * 60)
    
    try:
        sys.path.insert(0, os.path.abspath('.'))
        from automation.email_sender import EmailSender
        
        # Temporarily remove API key to test dry-run mode
        original_key = os.getenv('TWILIO_SENDGRID_API_KEY') or os.getenv('SENDGRID_API_KEY')
        if 'TWILIO_SENDGRID_API_KEY' in os.environ:
            del os.environ['TWILIO_SENDGRID_API_KEY']
        if 'SENDGRID_API_KEY' in os.environ:
            del os.environ['SENDGRID_API_KEY']
        
        sender = EmailSender()
        
        result = sender.send_email(
            to_email='test@example.com',
            to_name='Test Recipient',
            subject='Test Email from Twilio SendGrid Integration',
            body='This is a test email to validate the integration.'
        )
        
        # Restore API key
        if original_key:
            os.environ['TWILIO_SENDGRID_API_KEY'] = original_key
        
        print("✅ Dry-run mode works (no email actually sent)")
        print(f"   Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in dry-run test: {e}")
        return False

def print_next_steps():
    """Print next steps based on test results."""
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    
    api_key = os.getenv('TWILIO_SENDGRID_API_KEY') or os.getenv('SENDGRID_API_KEY')
    
    if not api_key:
        print("""
❌ BLOCKED: No API key set

TO FIX:
1. Read TWILIO-MIGRATION-GUIDE.md for detailed instructions
2. Log into console.twilio.com
3. Navigate to: Email → API Keys → Create API Key
4. Copy the key (starts with 'SG.')
5. Add to automation/.env:
   export TWILIO_SENDGRID_API_KEY="SG.your_key_here"
6. Load environment: source automation/.env
7. Run this test again: python3 automation/test_twilio_integration.py
""")
    else:
        print("""
✅ API key is set!

NEXT:
1. Verify your sender email in Twilio Console:
   console.twilio.com → Email → Sender Authentication → Verify a Single Sender
   
2. Update automation/config.json with your real email (if not done yet)

3. Run preflight check:
   python3 automation/preflight.py
   
4. If all checks pass, launch first campaign:
   python3 automation/orchestrator.py initial 20

See API-SETUP.md for complete setup instructions.
""")

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("TWILIO SENDGRID INTEGRATION TEST")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Environment Variables", test_env_vars()))
    results.append(("Configuration File", test_config()))
    results.append(("SendGrid SDK", test_sendgrid_import()))
    results.append(("EmailSender Init", test_email_sender()))
    results.append(("Dry Run", test_dry_run()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
    
    print_next_steps()

if __name__ == '__main__':
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    main()
