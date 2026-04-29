#!/usr/bin/env python3
"""
Automated email sender using Twilio SendGrid API.
Handles rate limiting, tracking, and webhooks.

NOTE: After Twilio acquired SendGrid, you need a SendGrid API key (SG.xxx...)
from your Twilio Console, NOT the Twilio Account SID + Auth Token.
See TWILIO-MIGRATION-GUIDE.md for details.
"""

import json
import os
import time
from typing import Dict, List
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking, OpenTracking, Bcc

class EmailSender:
    def __init__(self, config_path='automation/config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Try multiple environment variable names for flexibility
        api_key = (
            os.getenv('TWILIO_SENDGRID_API_KEY') or  # Preferred (clearer naming)
            os.getenv('SENDGRID_API_KEY') or          # Legacy/original
            os.getenv(self.config.get('sendgrid_api_key', 'SENDGRID_API_KEY'))
        )
        
        # Validate API key format
        if api_key and not api_key.startswith('SG.'):
            print("⚠️  WARNING: API key doesn't start with 'SG.' - is this a SendGrid API key?")
            print("   Twilio Account SID + Auth Token cannot be used directly for email.")
            print("   See TWILIO-MIGRATION-GUIDE.md for instructions.")
        
        self.sg = SendGridAPIClient(api_key) if api_key else None
        
        self.from_email = self.config['from_email']
        self.from_name = self.config['from_name']
        self.reply_to = self.config['reply_to']
        self.bcc_email = self.config.get('bcc_email', 'b2bemails@solvd.studio')
        
        # Rate limiting
        self.emails_per_hour = self.config['rate_limits']['emails_per_hour']
        self.emails_per_day = self.config['rate_limits']['emails_per_day']
        
        self.sent_this_hour = 0
        self.sent_today = 0
        self.last_reset_hour = datetime.now().hour
        self.last_reset_day = datetime.now().date()
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        now = datetime.now()
        
        # Reset hourly counter
        if now.hour != self.last_reset_hour:
            self.sent_this_hour = 0
            self.last_reset_hour = now.hour
        
        # Reset daily counter
        if now.date() != self.last_reset_day:
            self.sent_today = 0
            self.last_reset_day = now.date()
        
        # Check limits
        if self.sent_this_hour >= self.emails_per_hour:
            return False
        if self.sent_today >= self.emails_per_day:
            return False
        
        return True
    
    def _wait_for_rate_limit(self):
        """Wait until we're under rate limits."""
        while not self._check_rate_limit():
            print("⏸️  Rate limit reached. Waiting 60 seconds...")
            time.sleep(60)
    
    def send_email(self, to_email: str, to_name: str, subject: str, body: str) -> Dict:
        """
        Send a single email via SendGrid.
        
        Returns:
            Dict with 'success', 'message_id', and 'error' keys
        """
        if not self.sg:
            print("⚠️  Twilio SendGrid API key not set. Email would be sent to:")
            print(f"   TO: {to_name} <{to_email}>")
            print(f"   SUBJECT: {subject}")
            print(f"   BODY: {body[:100]}...")
            print("\n💡 To fix: Set TWILIO_SENDGRID_API_KEY environment variable")
            print("   Get key from: console.twilio.com → Email → API Keys")
            print("   See TWILIO-MIGRATION-GUIDE.md for full instructions\n")
            return {'success': False, 'error': 'Twilio SendGrid API key not configured'}
        
        # Check rate limit
        self._wait_for_rate_limit()
        
        try:
            # Create email
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=(to_email, to_name),
                subject=subject,
                plain_text_content=body
            )
            
            # Set reply-to
            message.reply_to = self.reply_to
            
            # Add BCC for campaign tracking
            message.add_bcc(self.bcc_email)
            
            # Enable tracking
            message.tracking_settings = TrackingSettings()
            message.tracking_settings.click_tracking = ClickTracking(enable=True, enable_text=False)
            message.tracking_settings.open_tracking = OpenTracking(enable=True)
            
            # Send
            response = self.sg.send(message)
            
            # Update counters
            self.sent_this_hour += 1
            self.sent_today += 1
            
            # Extract message ID from headers
            message_id = response.headers.get('X-Message-Id', '')
            
            print(f"✅ Sent to {to_name} ({to_email})")
            
            return {
                'success': True,
                'message_id': message_id,
                'status_code': response.status_code
            }
        
        except Exception as e:
            print(f"❌ Failed to send to {to_email}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_batch(self, emails: List[Dict], delay_seconds: int = 5) -> Dict:
        """
        Send a batch of emails with delays between each.
        
        Args:
            emails: List of dicts with keys: to_email, to_name, subject, body
            delay_seconds: Seconds to wait between emails (anti-spam)
        
        Returns:
            Dict with success count and errors
        """
        print(f"\n📧 Sending batch of {len(emails)} emails...\n")
        
        results = {
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        for i, email in enumerate(emails, 1):
            print(f"[{i}/{len(emails)}] ", end='')
            
            result = self.send_email(
                to_email=email['to_email'],
                to_name=email['to_name'],
                subject=email['subject'],
                body=email['body']
            )
            
            if result['success']:
                results['sent'] += 1
                email['message_id'] = result.get('message_id')
            else:
                results['failed'] += 1
                results['errors'].append({
                    'email': email['to_email'],
                    'error': result.get('error')
                })
            
            # Delay between emails (avoid spam filters)
            if i < len(emails):
                time.sleep(delay_seconds)
        
        print(f"\n✅ Batch complete: {results['sent']} sent, {results['failed']} failed\n")
        
        return results

if __name__ == '__main__':
    # Test email sender
    sender = EmailSender()
    
    test_email = {
        'to_email': 'test@example.com',
        'to_name': 'Test Recipient',
        'subject': 'Test Email',
        'body': 'This is a test email from the automation system.'
    }
    
    result = sender.send_email(**test_email)
    print(json.dumps(result, indent=2))
