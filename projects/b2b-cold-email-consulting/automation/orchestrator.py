#!/usr/bin/env python3
"""
Main orchestrator for automated cold email campaigns.
Coordinates prospect finding, personalization, sending, and follow-ups.
"""

import json
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict

from prospect_finder import ProspectFinder
from email_personalizer import EmailPersonalizer
from email_sender import EmailSender
from database import CampaignDB

class CampaignOrchestrator:
    def __init__(self, config_path='automation/config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.db = CampaignDB()
        self.finder = ProspectFinder(config_path)
        self.personalizer = EmailPersonalizer(config_path)
        self.sender = EmailSender(config_path)
    
    def run_initial_campaign(self, target_prospects: int = 20):
        """
        Run the complete initial campaign:
        1. Find prospects
        2. Personalize emails
        3. Store in database
        4. Send initial emails
        """
        print("\n" + "="*60)
        print("🚀 STARTING AUTOMATED COLD EMAIL CAMPAIGN")
        print("="*60 + "\n")
        
        # Step 1: Find prospects
        print("STEP 1: Finding prospects...")
        prospects = self.finder.find_prospects(total_target=target_prospects)
        
        if not prospects:
            print("❌ No prospects found. Exiting.")
            return
        
        print(f"✅ Found {len(prospects)} prospects\n")
        
        # Step 2: Store prospects in database
        print("STEP 2: Storing prospects in database...")
        prospect_ids = []
        for prospect in prospects:
            prospect_id = self.db.add_prospect(prospect)
            prospect_ids.append(prospect_id)
            prospect['id'] = prospect_id
        
        print(f"✅ Stored {len(prospect_ids)} prospects\n")
        
        # Step 3: Personalize initial emails
        print("STEP 3: Personalizing initial emails...")
        personalized = self.personalizer.personalize_batch(prospects, email_type='initial')
        print(f"✅ Personalized {len(personalized)} emails\n")
        
        # Step 4: Store emails in database
        print("STEP 4: Preparing emails for sending...")
        emails_to_send = []
        for p in personalized:
            email_id = self.db.add_email(
                prospect_id=p['id'],
                email_type='initial',
                subject=p['email_subject'],
                body=p['email_body']
            )
            
            emails_to_send.append({
                'email_id': email_id,
                'to_email': p['email'],
                'to_name': p['name'],
                'subject': p['email_subject'],
                'body': p['email_body']
            })
        
        print(f"✅ Prepared {len(emails_to_send)} emails\n")
        
        # Step 5: Send emails
        print("STEP 5: Sending emails...")
        results = self.sender.send_batch(emails_to_send, delay_seconds=10)
        
        # Update database with send status
        for email in emails_to_send:
            if 'message_id' in email:
                self.db.mark_email_sent(email['email_id'], email.get('message_id'))
        
        print("\n" + "="*60)
        print("✅ INITIAL CAMPAIGN COMPLETE")
        print("="*60)
        print(f"Sent: {results['sent']}")
        print(f"Failed: {results['failed']}")
        print(f"\nNext: Run follow-up scheduler in 3 days")
        print("="*60 + "\n")
        
        # Save campaign summary
        self._save_campaign_summary(results)
    
    def run_follow_ups(self):
        """
        Check for prospects due for follow-up emails and send them.
        Should be run daily.
        """
        print("\n" + "="*60)
        print("📬 CHECKING FOR FOLLOW-UP EMAILS")
        print("="*60 + "\n")
        
        follow_up_schedule = [
            (1, self.config['email_sequence']['follow_up_1_delay_days']),
            (2, self.config['email_sequence']['follow_up_2_delay_days']),
            (3, self.config['email_sequence']['follow_up_3_delay_days'])
        ]
        
        total_sent = 0
        
        for follow_up_num, days_delay in follow_up_schedule:
            print(f"\nChecking for follow-up #{follow_up_num} (after {days_delay} days)...")
            
            # Get prospects due for this follow-up
            prospects_due = self.db.get_prospects_due_for_followup(follow_up_num, days_delay)
            
            if not prospects_due:
                print(f"  No prospects due for follow-up #{follow_up_num}")
                continue
            
            print(f"  Found {len(prospects_due)} prospects due for follow-up #{follow_up_num}")
            
            # Personalize emails
            email_type = f'follow_up_{follow_up_num}'
            personalized = self.personalizer.personalize_batch(prospects_due, email_type=email_type)
            
            # Prepare emails
            emails_to_send = []
            for p in personalized:
                email_id = self.db.add_email(
                    prospect_id=p['id'],
                    email_type=email_type,
                    subject=p['email_subject'],
                    body=p['email_body']
                )
                
                emails_to_send.append({
                    'email_id': email_id,
                    'to_email': p['email'],
                    'to_name': p['name'],
                    'subject': p['email_subject'],
                    'body': p['email_body']
                })
            
            # Send emails
            results = self.sender.send_batch(emails_to_send, delay_seconds=10)
            
            # Update database
            for email in emails_to_send:
                if 'message_id' in email:
                    self.db.mark_email_sent(email['email_id'], email.get('message_id'))
            
            total_sent += results['sent']
        
        print("\n" + "="*60)
        print(f"✅ FOLLOW-UP CHECK COMPLETE: {total_sent} emails sent")
        print("="*60 + "\n")
        
        # Print stats
        self.print_campaign_stats()
    
    def print_campaign_stats(self):
        """Print current campaign statistics."""
        stats = self.db.get_campaign_stats()
        
        print("\n📊 CAMPAIGN STATISTICS")
        print("="*60)
        print(f"Total Prospects: {stats.get('total_prospects', 0)}")
        print(f"Emails Sent: {stats.get('emails_sent', 0)}")
        print(f"Opens: {stats.get('emails_opened', 0)} ({stats.get('open_rate', 0)}%)")
        print(f"Clicks: {stats.get('emails_clicked', 0)} ({stats.get('click_rate', 0)}%)")
        print(f"Replies: {stats.get('emails_replied', 0)} ({stats.get('reply_rate', 0)}%)")
        print(f"Bounces: {stats.get('emails_bounced', 0)} ({stats.get('bounce_rate', 0)}%)")
        print("="*60 + "\n")
    
    def _save_campaign_summary(self, results: Dict):
        """Save campaign summary to file."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'sent': results['sent'],
            'failed': results['failed'],
            'errors': results.get('errors', [])
        }
        
        with open('automation/campaign-log.json', 'a') as f:
            f.write(json.dumps(summary) + '\n')
    
    def close(self):
        """Clean up resources."""
        self.db.close()

def main():
    """Main entry point for the orchestrator."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python orchestrator.py initial [num_prospects]  - Run initial campaign")
        print("  python orchestrator.py followups                - Check and send follow-ups")
        print("  python orchestrator.py stats                    - Print campaign stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    orchestrator = CampaignOrchestrator()
    
    try:
        if command == 'initial':
            target = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            orchestrator.run_initial_campaign(target_prospects=target)
        
        elif command == 'followups':
            orchestrator.run_follow_ups()
        
        elif command == 'stats':
            orchestrator.print_campaign_stats()
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    
    finally:
        orchestrator.close()

if __name__ == '__main__':
    main()
