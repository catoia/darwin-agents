#!/usr/bin/env python3
"""
Automated email personalizer using local LLM via pi skill.
Generates highly personalized cold emails based on prospect data.
"""

import json
import os
import subprocess
from typing import Dict, List

class EmailPersonalizer:
    def __init__(self, config_path='automation/config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Get absolute path to skill file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        self.skill_path = os.path.join(project_dir, 'skills', 'email-personalizer', 'SKILL.md')
        
        # Verify skill exists
        if not os.path.exists(self.skill_path):
            print(f"⚠️  Email personalizer skill not found at {self.skill_path}")
            self.skill_path = None
    
    def _call_skill(self, prospect: Dict, email_type: str) -> Dict:
        """
        Call the email personalizer skill via pi subprocess.
        
        Args:
            prospect: Dict with prospect data
            email_type: Type of email to generate
        
        Returns:
            Dict with 'subject' and 'body' or None if failed
        """
        if not self.skill_path:
            return None
        
        # Prepare input JSON
        input_data = {
            'prospect': prospect,
            'email_type': email_type
        }
        
        try:
            # Call pi with the skill file as context
            result = subprocess.run(
                [
                    'pi',
                    '--no-session',
                    '--provider', 'github-copilot',
                    '--model', 'claude-sonnet-4.6',
                    '--context-files', self.skill_path,
                    '-p', f'Generate an email. Input: {json.dumps(input_data)}'
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"⚠️  Skill call failed: {result.stderr}")
                return None
            
            # Parse JSON output from stdout
            # Look for JSON block in the output
            output = result.stdout.strip()
            
            # Try to find JSON object in output
            start_idx = output.find('{')
            end_idx = output.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                print(f"⚠️  No JSON found in skill output")
                return None
            
            json_str = output[start_idx:end_idx]
            email_data = json.loads(json_str)
            
            # Validate structure
            if 'subject' not in email_data or 'body' not in email_data:
                print(f"⚠️  Invalid skill output format")
                return None
            
            return email_data
            
        except subprocess.TimeoutExpired:
            print("⚠️  Skill call timed out after 30 seconds")
            return None
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse skill output as JSON: {e}")
            return None
        except Exception as e:
            print(f"⚠️  Skill call error: {e}")
            return None
    
    def personalize_email(self, prospect: Dict, email_type='initial') -> Dict:
        """
        Generate a personalized email for a prospect.
        
        Args:
            prospect: Dict with keys: name, company, email, title, product, website
            email_type: 'initial', 'follow_up_1', 'follow_up_2', 'follow_up_3'
        
        Returns:
            Dict with 'subject' and 'body'
        """
        # Try to use local skill first
        email_data = self._call_skill(prospect, email_type)
        
        if email_data:
            return {
                'subject': email_data['subject'],
                'body': email_data['body'],
                'type': email_type
            }
        
        # Fall back to static templates if skill fails
        print("⚠️  Local skill failed. Using fallback templates.")
        return self._fallback_template(prospect, email_type)
    
    def _fallback_template(self, prospect: Dict, email_type: str) -> Dict:
        """Fallback templates when AI is unavailable."""
        
        name = prospect.get('name', 'there')
        company = prospect.get('company', 'your company')
        product = prospect.get('product', 'your product')
        
        templates = {
            'initial': {
                'subject': f"Quick cold email tip for {company}",
                'body': f"""Hi {name},

Saw {company} on Product Hunt - {product} looks sharp.

I help B2B SaaS founders write cold email sequences that actually get responses (20%+ vs the typical 3-5%).

Just took a quick look at your cold email approach and spotted 3 wins that could double your response rate.

Want a free 15-min teardown? I'll send you a quick video audit of your current sequences.

Just reply "yes" if interested.

Cheers,
Nuno"""
            },
            'follow_up_1': {
                'subject': f"Re: Cold email teardown for {company}",
                'body': f"""Hi {name},

Following up - still happy to do that free 15-min cold email teardown for {company}.

Quick tip for B2B SaaS: personalized first lines increase response rates 3x. Most founders skip this because it's time-consuming, but there's a workaround.

Just reply "yes" and I'll send the calendar link.

Nuno"""
            },
            'follow_up_2': {
                'subject': f"Last one: cold email resource for {company}",
                'body': f"""Hi {name},

I'll stop after this one - promise.

Here's a free tip: B2B cold emails need urgency + specificity in the CTA. "Let's chat" gets ignored. "15-min teardown this Thursday" gets booked.

If you want that free teardown, reply "yes". If not, all good - good luck with {company}!

Nuno"""
            },
            'follow_up_3': {
                'subject': f"Moving on (+ free resource)",
                'body': f"""Hi {name},

No worries on the cold email teardown - seems like timing isn't right.

Here's a free cold email template library I put together: [link]

If you ever need cold email help down the road, you know where to find me.

Best,
Nuno"""
            }
        }
        
        return templates.get(email_type, templates['initial'])
    
    def personalize_batch(self, prospects: List[Dict], email_type='initial') -> List[Dict]:
        """
        Personalize emails for a batch of prospects.
        
        Returns:
            List of dicts with prospect info + personalized email
        """
        print(f"\n✍️  Personalizing {email_type} emails for {len(prospects)} prospects...\n")
        
        personalized = []
        for i, prospect in enumerate(prospects, 1):
            print(f"[{i}/{len(prospects)}] Personalizing for {prospect.get('name')} at {prospect.get('company')}...")
            
            email = self.personalize_email(prospect, email_type)
            
            personalized.append({
                **prospect,
                'email_subject': email['subject'],
                'email_body': email['body'],
                'email_type': email_type
            })
        
        print(f"\n✅ Personalized {len(personalized)} emails\n")
        return personalized

if __name__ == '__main__':
    # Test with sample prospects
    with open('automation/prospects.json') as f:
        data = json.load(f)
        prospects = data['prospects'][:3]  # Test with first 3
    
    personalizer = EmailPersonalizer()
    personalized = personalizer.personalize_batch(prospects, email_type='initial')
    
    # Print examples
    for p in personalized:
        print(f"\n{'='*60}")
        print(f"TO: {p['name']} ({p['email']})")
        print(f"SUBJECT: {p['email_subject']}")
        print(f"\n{p['email_body']}")
        print(f"{'='*60}\n")
