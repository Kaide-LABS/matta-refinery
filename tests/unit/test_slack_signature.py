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


def test_valid_signature_with_lowercase_header_keys():
    """Starlette canonicalises incoming HTTP header names to lowercase.
    verify() must accept either the mixed-case spec name or the
    lowercase Starlette form. This pins the case-insensitivity
    contract.
    """
    secret = "shhh"
    ts = str(int(time.time()))
    body = b'{"hello":"world"}'
    base = f"v0:{ts}:".encode("utf-8") + body
    sig = "v0=" + hmac.new(secret.encode("utf-8"), base, hashlib.sha256).hexdigest()

    class _CaseInsensitiveHeaders(dict):
        """Mimics Starlette's headers: lowercase keys, case-insensitive get."""
        def get(self, key, default=None):
            return super().get(key.lower(), default)

    headers = _CaseInsensitiveHeaders({
        "x-slack-request-timestamp": ts,
        "x-slack-signature": sig,
    })
    assert verify(
        headers=headers,
        body=body,
        signing_secret=secret,
    ) is True


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
