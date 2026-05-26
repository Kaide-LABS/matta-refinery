import hmac
import hashlib
import time
from typing import Mapping


class SlackSignatureError(Exception):
    """Raised when a Slack request fails signature verification."""


def verify(
    headers: Mapping[str, str],
    body: bytes,
    signing_secret: str,
    window_seconds: int = 300,
) -> bool:
    """Verify a Slack request's signature.

    Raises SlackSignatureError on any failure mode (missing headers,
    expired timestamp, HMAC mismatch). Returns True on successful
    verification.
    """
    timestamp = headers.get("X-Slack-Request-Timestamp")
    slack_signature = headers.get("X-Slack-Signature")

    if not timestamp:
        raise SlackSignatureError("missing X-Slack-Request-Timestamp header")
    if not slack_signature:
        raise SlackSignatureError("missing X-Slack-Signature header")

    try:
        ts_int = int(timestamp)
    except ValueError:
        raise SlackSignatureError("invalid timestamp format")

    if abs(time.time() - ts_int) > window_seconds:
        raise SlackSignatureError(
            f"timestamp outside {window_seconds}s window"
        )

    base_string = f"v0:{timestamp}:".encode("utf-8") + body
    my_signature = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        base_string,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(my_signature, slack_signature):
        raise SlackSignatureError("HMAC signature mismatch")

    return True
