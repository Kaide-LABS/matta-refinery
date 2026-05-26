import hmac
import hashlib
import time

import pytest

from packages.adapters.slack.signature import SlackSignatureError, verify


def test_unsigned_request_raises():
    with pytest.raises(SlackSignatureError, match="missing"):
        verify(headers={}, body=b"{}", signing_secret="secret")


def test_missing_signature_header_raises():
    with pytest.raises(SlackSignatureError, match="missing X-Slack-Signature"):
        verify(
            headers={"X-Slack-Request-Timestamp": str(int(time.time()))},
            body=b"{}",
            signing_secret="secret",
        )


def test_invalid_signature_raises():
    with pytest.raises(SlackSignatureError, match="HMAC"):
        verify(
            headers={
                "X-Slack-Request-Timestamp": str(int(time.time())),
                "X-Slack-Signature": "v0=invalid",
            },
            body=b"{}",
            signing_secret="secret",
        )


def test_old_timestamp_raises():
    with pytest.raises(SlackSignatureError, match="window"):
        verify(
            headers={
                "X-Slack-Request-Timestamp": "1",
                "X-Slack-Signature": "v0=anything",
            },
            body=b"{}",
            signing_secret="secret",
            window_seconds=300,
        )


def test_invalid_timestamp_format_raises():
    with pytest.raises(SlackSignatureError, match="invalid timestamp"):
        verify(
            headers={
                "X-Slack-Request-Timestamp": "not-a-number",
                "X-Slack-Signature": "v0=anything",
            },
            body=b"{}",
            signing_secret="secret",
        )


def test_valid_signature_returns_true():
    secret = "shhh"
    ts = str(int(time.time()))
    body = b'{"hello":"world"}'
    base = f"v0:{ts}:".encode("utf-8") + body
    sig = "v0=" + hmac.new(secret.encode("utf-8"), base, hashlib.sha256).hexdigest()
    assert verify(
        headers={"X-Slack-Request-Timestamp": ts, "X-Slack-Signature": sig},
        body=body,
        signing_secret=secret,
    ) is True
