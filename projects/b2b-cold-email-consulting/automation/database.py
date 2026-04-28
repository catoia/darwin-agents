#!/usr/bin/env python3
"""
Database for tracking prospect email campaigns.
Uses SQLite for simplicity (no external dependencies).
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class CampaignDB:
    def __init__(self, db_path='automation/campaign.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def _init_schema(self):
        """Create tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Prospects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prospects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                company TEXT,
                title TEXT,
                product TEXT,
                website TEXT,
                source TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        """)
        
        # Emails table (tracks sent emails)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prospect_id INTEGER NOT NULL,
                email_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                sent_at TIMESTAMP,
                opened_at TIMESTAMP,
                clicked_at TIMESTAMP,
                replied_at TIMESTAMP,
                bounced_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                sendgrid_message_id TEXT,
                FOREIGN KEY (prospect_id) REFERENCES prospects (id)
            )
        """)
        
        # Replies table (tracks responses)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prospect_id INTEGER NOT NULL,
                email_id INTEGER,
                reply_text TEXT,
                sentiment TEXT,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prospect_id) REFERENCES prospects (id),
                FOREIGN KEY (email_id) REFERENCES emails (id)
            )
        """)
        
        self.conn.commit()
    
    def add_prospect(self, prospect: Dict) -> int:
        """Add a new prospect. Returns prospect_id."""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO prospects (name, email, company, title, product, website, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                prospect.get('name'),
                prospect.get('email'),
                prospect.get('company'),
                prospect.get('title'),
                prospect.get('product'),
                prospect.get('website'),
                prospect.get('source')
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Email already exists
            cursor.execute("SELECT id FROM prospects WHERE email = ?", (prospect.get('email'),))
            row = cursor.fetchone()
            return row['id'] if row else None
    
    def add_email(self, prospect_id: int, email_type: str, subject: str, body: str) -> int:
        """Log an email to be sent. Returns email_id."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO emails (prospect_id, email_type, subject, body, status)
            VALUES (?, ?, ?, ?, 'pending')
        """, (prospect_id, email_type, subject, body))
        self.conn.commit()
        return cursor.lastrowid
    
    def mark_email_sent(self, email_id: int, sendgrid_message_id: str = None):
        """Mark email as sent."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE emails
            SET status = 'sent', sent_at = ?, sendgrid_message_id = ?
            WHERE id = ?
        """, (datetime.now(), sendgrid_message_id, email_id))
        self.conn.commit()
    
    def mark_email_opened(self, email_id: int):
        """Mark email as opened (from SendGrid webhook)."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE emails
            SET opened_at = ?
            WHERE id = ?
        """, (datetime.now(), email_id))
        self.conn.commit()
    
    def mark_email_clicked(self, email_id: int):
        """Mark email as clicked (from SendGrid webhook)."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE emails
            SET clicked_at = ?
            WHERE id = ?
        """, (datetime.now(), email_id))
        self.conn.commit()
    
    def mark_email_replied(self, email_id: int, reply_text: str = None):
        """Mark email as replied."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE emails
            SET replied_at = ?, status = 'replied'
            WHERE id = ?
        """, (datetime.now(), email_id))
        
        # Also log the reply
        if reply_text:
            prospect_id = self.get_email(email_id)['prospect_id']
            cursor.execute("""
                INSERT INTO replies (prospect_id, email_id, reply_text)
                VALUES (?, ?, ?)
            """, (prospect_id, email_id, reply_text))
        
        self.conn.commit()
    
    def mark_email_bounced(self, email_id: int):
        """Mark email as bounced."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE emails
            SET bounced_at = ?, status = 'bounced'
            WHERE id = ?
        """, (datetime.now(), email_id))
        self.conn.commit()
    
    def get_prospects_due_for_followup(self, follow_up_number: int, days_since_last: int) -> List[Dict]:
        """
        Get prospects who need a follow-up email.
        
        Args:
            follow_up_number: 1, 2, or 3
            days_since_last: Days since their last email
        
        Returns:
            List of prospects with their info
        """
        cursor = self.conn.cursor()
        
        email_type_map = {
            1: 'follow_up_1',
            2: 'follow_up_2',
            3: 'follow_up_3'
        }
        
        # Get prospects who:
        # - Haven't replied
        # - Haven't bounced
        # - Last email was N days ago
        # - Haven't received this follow-up yet
        
        query = """
            SELECT DISTINCT p.*, 
                   MAX(e.sent_at) as last_sent_at,
                   (julianday('now') - julianday(MAX(e.sent_at))) as days_since_last
            FROM prospects p
            INNER JOIN emails e ON p.id = e.prospect_id
            WHERE p.status = 'active'
              AND e.status NOT IN ('replied', 'bounced')
              AND p.id NOT IN (
                  SELECT prospect_id FROM emails WHERE email_type = ?
              )
            GROUP BY p.id
            HAVING days_since_last >= ?
        """
        
        cursor.execute(query, (email_type_map[follow_up_number], days_since_last))
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_email(self, email_id: int) -> Optional[Dict]:
        """Get email by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM emails WHERE id = ?", (email_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_prospect(self, prospect_id: int) -> Optional[Dict]:
        """Get prospect by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM prospects WHERE id = ?", (prospect_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_campaign_stats(self) -> Dict:
        """Get overall campaign statistics."""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total prospects
        cursor.execute("SELECT COUNT(*) as count FROM prospects WHERE status = 'active'")
        stats['total_prospects'] = cursor.fetchone()['count']
        
        # Emails sent
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE status = 'sent'")
        stats['emails_sent'] = cursor.fetchone()['count']
        
        # Opens
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE opened_at IS NOT NULL")
        stats['emails_opened'] = cursor.fetchone()['count']
        
        # Clicks
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE clicked_at IS NOT NULL")
        stats['emails_clicked'] = cursor.fetchone()['count']
        
        # Replies
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE replied_at IS NOT NULL")
        stats['emails_replied'] = cursor.fetchone()['count']
        
        # Bounces
        cursor.execute("SELECT COUNT(*) as count FROM emails WHERE bounced_at IS NOT NULL")
        stats['emails_bounced'] = cursor.fetchone()['count']
        
        # Calculate rates
        if stats['emails_sent'] > 0:
            stats['open_rate'] = round(stats['emails_opened'] / stats['emails_sent'] * 100, 1)
            stats['click_rate'] = round(stats['emails_clicked'] / stats['emails_sent'] * 100, 1)
            stats['reply_rate'] = round(stats['emails_replied'] / stats['emails_sent'] * 100, 1)
            stats['bounce_rate'] = round(stats['emails_bounced'] / stats['emails_sent'] * 100, 1)
        
        return stats
    
    def close(self):
        """Close database connection."""
        self.conn.close()

if __name__ == '__main__':
    # Test the database
    db = CampaignDB()
    
    # Add a test prospect
    prospect = {
        'name': 'Test Founder',
        'email': 'test@example.com',
        'company': 'TestCo',
        'title': 'CEO',
        'product': 'B2B SaaS product',
        'website': 'https://example.com',
        'source': 'Test'
    }
    
    prospect_id = db.add_prospect(prospect)
    print(f"Added prospect with ID: {prospect_id}")
    
    # Add a test email
    email_id = db.add_email(prospect_id, 'initial', 'Test Subject', 'Test body')
    print(f"Added email with ID: {email_id}")
    
    # Get stats
    stats = db.get_campaign_stats()
    print(f"\nCampaign stats:")
    print(json.dumps(stats, indent=2))
    
    db.close()
