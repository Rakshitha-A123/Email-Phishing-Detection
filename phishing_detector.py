import re
import json

class PhishingDetector:
    def __init__(self):
        # Initialize detection patterns with weights
        self.patterns = {
            'urgency': {
                'weight': 15,
                'words': [
                    'urgent', 'immediate', 'now', 'verify', 'suspended', 'locked', 
                    'security', 'unusual', 'unauthorized', 'limited time', 'warning',
                    'alert', 'attention', 'action required', 'expire', 'deadline'
                ]
            },
            'sensitive': {
                'weight': 20,
                'words': [
                    'password', 'credit card', 'social security', 'ssn', 'account',
                    'login', 'bank', 'verify', 'confirm', 'validate', 'credentials',
                    'sign in', 'username', 'pin', 'security question'
                ]
            },
            'financial': {
                'weight': 15,
                'words': [
                    'money', 'cash', 'payment', 'wire', 'transfer', 'transaction',
                    'bank', 'account', 'credit', 'debit', 'fund', 'dollar', '$',
                    'bitcoin', 'crypto', 'wallet', 'deposit', 'refund'
                ]
            },
            'threat': {
                'weight': 20,
                'words': [
                    'suspended', 'terminated', 'deleted', 'blocked', 'limited',
                    'closed', 'reported', 'unauthorized', 'suspicious', 'disabled',
                    'restricted', 'violation', 'security breach', 'compromised'
                ]
            },
            'prize': {
                'weight': 25,
                'words': [
                    'won', 'winner', 'prize', 'reward', 'congratulation', 'selected',
                    'lottery', 'claim', 'free', 'gift', 'bonus', 'exclusive offer'
                ]
            }
        }
        
        # URL detection patterns
        self.suspicious_domains = [
            'secure', 'account', 'banking', 'verify', 'update', 'login',
            'confirm', 'support', 'security', 'service'
        ]

    def check_urls(self, text):
        """Check for suspicious URLs in text"""
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        suspicious_urls = []
        
        for url in urls:
            if any(domain in url.lower() for domain in self.suspicious_domains):
                suspicious_urls.append(url)
        
        return suspicious_urls

    def analyze_email(self, email_text):
        """
        Analyze email for phishing indicators
        Returns dict with analysis results
        """
        if not email_text:
            return {
                'is_phishing': False,
                'risk_score': 0,
                'reasons': ['No content to analyze'],
                'details': {}
            }

        email_text = str(email_text).lower()
        risk_score = 0
        reasons = []
        details = {}

        # Check for URLs
        suspicious_urls = self.check_urls(email_text)
        if suspicious_urls:
            url_score = len(suspicious_urls) * 20
            risk_score += url_score
            reasons.append(f"🔗 Found {len(suspicious_urls)} suspicious URL(s)")
            details['urls'] = {
                'found': suspicious_urls,
                'score': url_score
            }

        # Check each pattern category
        for category, data in self.patterns.items():
            found_words = [word for word in data['words'] if word in email_text]
            if found_words:
                category_score = len(found_words) * data['weight']
                risk_score += category_score
                
                # Add emoji based on category
                emoji = self.get_category_emoji(category)
                reasons.append(f"{emoji} {category.title()}: {', '.join(found_words)}")
                
                details[category] = {
                    'found_words': found_words,
                    'score': category_score
                }

        # Normalize risk score to 100
        risk_score = min(100, risk_score)

        # Determine risk level
        risk_level = self.get_risk_level(risk_score)

        return {
            'is_phishing': risk_score >= 40,  # Threshold for phishing classification
            'risk_score': risk_score,
            'risk_level': risk_level,
            'reasons': reasons,
            'details': details
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

    def get_risk_level(self, risk_score):
        """Determine risk level based on score"""
        if risk_score >= 75:
            return 'High'
        elif risk_score >= 40:
            return 'Medium'
        elif risk_score >= 20:
            return 'Low'
        else:
            return 'Safe'

    def get_status(self):
        """Get current detector status and pattern counts"""
        status = {
            'pattern_counts': {},
            'weights': {},
            'total_patterns': 0
        }
        
        for category, data in self.patterns.items():
            status['pattern_counts'][category] = len(data['words'])
            status['weights'][category] = data['weight']
            status['total_patterns'] += len(data['words'])
        
        status['suspicious_domains'] = len(self.suspicious_domains)
        
        return status

# Test the detector
detector = PhishingDetector()
test_email = """
URGENT: Your Account Security Alert
Dear Customer,
We detected unusual sign-in activity. Verify your account immediately:
http://secure-banking-verify.com/auth
Your account will be suspended if you don't act now.
"""

result = detector.analyze_email(test_email)
print(json.dumps(result, indent=2))
