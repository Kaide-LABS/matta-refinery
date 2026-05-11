import hmac
import hashlib
import time

def verify(headers: dict, body: bytes, signing_secret: str, window_seconds: int = 300) -> bool:
    timestamp = headers.get("X-Slack-Request-Timestamp")
    slack_signature = headers.get("X-Slack-Signature")
    
    if not timestamp or not slack_signature:
        return False
        
    try:
        ts = int(timestamp)
    except ValueError:
        return False
        
    if abs(time.time() - ts) > window_seconds:
        return False
        
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    my_signature = "v0=" + hmac.new(
        signing_secret.encode('utf-8'),
        sig_basestring.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(my_signature, slack_signature)
