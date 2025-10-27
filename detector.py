import re

class PhishingDetector:
    def __init__(self):
        # Initialize detection patterns
        self.patterns = {
            'urgency': {
                'weight': 15,
                'words': [
                    'urgent', 'immediate', 'now', 'verify', 'suspended', 'locked', 
                    'security', 'unusual', 'unauthorized', 'limited time'
                ]
            },
            'sensitive': {
                'weight': 20,
                'words': [
                    'password', 'credit card', 'social security', 'ssn', 'account',
                    'login', 'bank', 'verify', 'confirm', 'validate'
                ]
            },
            'financial': {
                'weight': 15,
                'words': [
                    'money', 'cash', 'payment', 'wire', 'transfer', 'transaction',
                    'bank', 'account', 'credit', 'debit', 'fund', 'dollar', '$'
                ]
            },
            'threat': {
                'weight': 20,
                'words': [
                    'suspended', 'terminated', 'deleted', 'blocked', 'limited',
                    'closed', 'reported', 'unauthorized', 'suspicious'
                ]
            },
            'prize': {
                'weight': 25,
                'words': [
                    'won', 'winner', 'prize', 'reward', 'congratulation', 'selected',
                    'lottery', 'claim'
                ]
            }
        }

    def analyze_email(self, email_text):
        """Analyze email for phishing indicators"""
        try:
            email_text = str(email_text).lower()
            risk_score = 0
            reasons = []
            
            # Check for URLs
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_text)
            if urls:
                reasons.append(f"⚠️ Contains {len(urls)} URL(s)")
                risk_score += len(urls) * 20
            
            # Check each pattern category
            for category, data in self.patterns.items():
                found_words = [word for word in data['words'] if word in email_text]
                if found_words:
                    score = len(found_words) * data['weight']
                    risk_score += score
                    
                    # Add emoji based on category
                    emoji = self.get_category_emoji(category)
                    reasons.append(f"{emoji} {category.title()}: {', '.join(found_words)}")
            
            # Normalize risk score to 100
            risk_score = min(100, risk_score)
            
            return {
                'is_phishing': risk_score >= 40,
                'risk_score': risk_score,
                'reasons': reasons
            }
            
        except Exception as e:
            return {
                'is_phishing': False,
                'risk_score': 0,
                'reasons': [f"Error analyzing email: {str(e)}"]
            }

    def get_category_emoji(self, category):
        """Return appropriate emoji for each category"""
        emoji_map = {
            'urgency': '⚡',
            'sensitive': '🔒',
            'financial': '💰',
            'threat': '⚠️',
            'prize': '🎁'
        }
        return emoji_map.get(category, '📌')