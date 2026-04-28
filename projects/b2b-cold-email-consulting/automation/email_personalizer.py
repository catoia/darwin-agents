#!/usr/bin/env python3
"""
Automated email personalizer using OpenAI/Claude API.
Generates highly personalized cold emails based on prospect data.
"""

import json
import os
from typing import Dict, List
from openai import OpenAI

class EmailPersonalizer:
    def __init__(self, config_path='automation/config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        api_key = os.getenv(self.config['openai_api_key'])
        self.client = OpenAI(api_key=api_key) if api_key else None
        
        self.templates = {
            'initial': self._get_initial_template(),
            'follow_up_1': self._get_follow_up_1_template(),
            'follow_up_2': self._get_follow_up_2_template(),
            'follow_up_3': self._get_follow_up_3_template()
        }
    
    def _get_initial_template(self) -> str:
        return """You are a cold email expert. Write a short, personalized cold email to a B2B SaaS founder.

Prospect info:
- Name: {name}
- Company: {company}
- Product: {product}
- Title: {title}

Email guidelines:
1. Subject line must be ultra-specific and intriguing (8-12 words max)
2. Opening: personalized observation about their product/company (1 sentence)
3. Value prop: "I help B2B SaaS founders write cold email sequences that get 20%+ response rates" (1 sentence)
4. Hook: "Quick example - I just reviewed your current cold email approach and spotted 3 quick wins that could double your response rate" (1-2 sentences)
5. CTA: "Want a free 15-min teardown of your cold email strategy? I'll send you a quick video audit" (1 sentence)
6. Sign off: Keep it casual and brief

Tone: Direct, confident, helpful. No fluff. No corporate speak. Like a friend who knows their shit.
Length: 80-120 words MAX.

Output format:
SUBJECT: [subject line]

BODY:
[email body]"""
    
    def _get_follow_up_1_template(self) -> str:
        return """Write a brief follow-up email (3 days after initial email).

Prospect: {name} at {company}

Guidelines:
1. Subject: Re: [original subject] or a new short subject referencing their pain point
2. Acknowledge they're busy
3. Add NEW value: share a specific insight about cold email that applies to their industry
4. Reiterate the free offer: 15-min teardown
5. Make it easy to say yes: "Just reply 'yes' and I'll send the calendar link"

Length: 60-80 words MAX.
Tone: Persistent but helpful, not pushy.

Output format:
SUBJECT: [subject line]

BODY:
[email body]"""
    
    def _get_follow_up_2_template(self) -> str:
        return """Write a second follow-up email (7 days after initial).

Prospect: {name} at {company}

Guidelines:
1. Subject: Different angle - "Last attempt: [specific benefit]"
2. Breakup pattern: "I'll stop bugging you after this"
3. Share a quick cold email tip relevant to B2B SaaS (1-2 sentences)
4. Final CTA: "If you're interested, reply 'yes'. If not, no worries - good luck with {company}!"

Length: 50-70 words MAX.
Tone: Respectful, giving them an out, but confident in value.

Output format:
SUBJECT: [subject line]

BODY:
[email body]"""
    
    def _get_follow_up_3_template(self) -> str:
        return """Write a final breakup email (14 days after initial).

Prospect: {name} at {company}

Guidelines:
1. Subject: "Moving on (+ free cold email resource)"
2. Acknowledge they're not interested right now
3. Offer a free resource (cold email template or guide) with no strings attached
4. Leave door open: "If you ever need cold email help, you know where to find me"

Length: 40-60 words MAX.
Tone: Gracious, generous, not needy.

Output format:
SUBJECT: [subject line]

BODY:
[email body]"""
    
    def personalize_email(self, prospect: Dict, email_type='initial') -> Dict:
        """
        Generate a personalized email for a prospect.
        
        Args:
            prospect: Dict with keys: name, company, email, title, product, website
            email_type: 'initial', 'follow_up_1', 'follow_up_2', 'follow_up_3'
        
        Returns:
            Dict with 'subject' and 'body'
        """
        if not self.client:
            print("⚠️  OpenAI API key not set. Using fallback templates.")
            return self._fallback_template(prospect, email_type)
        
        try:
            template = self.templates[email_type]
            prompt = template.format(**prospect)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert B2B cold email copywriter known for high response rates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse result
            parts = result.split('\n\n', 1)
            subject_line = parts[0].replace('SUBJECT:', '').strip()
            body = parts[1].replace('BODY:', '').strip() if len(parts) > 1 else ''
            
            return {
                'subject': subject_line,
                'body': body,
                'type': email_type
            }
        
        except Exception as e:
            print(f"⚠️  AI personalization error: {e}. Using fallback.")
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
