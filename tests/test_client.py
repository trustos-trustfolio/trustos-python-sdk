"""Tests for TrustOSClient."""

import os
import json

import pytest
import responses as resp_mock

from trustos import TrustOSClient, TrustOSError

_API_KEY = "test_api_key_abc123"
_BASE_URL = "https://api.trust-os.io"
_VERIFY_URL = f"{_BASE_URL}/v1/decision/verify"

_MOCK_RESPONSE = {
    "decision_id": "dec_example_001",
    "recommendation": "APPROVE",
    "risk_score": 0.18,
    "risk_level": "LOW",
    "policy": "Stablecoin Settlement Policy v1.0",
    "proof_hash": "SHA-256: 0x4a3f...9c2b",
    "verified": True,
    "latency_ms": 142,
}

_PAYLOAD = {"action": "stablecoin_transfer", "amount": 50000, "currency": "USDC"}


# ── constructor ───────────────────────────────────────────────────────────────


def test_raises_without_api_key(monkeypatch):
    """Client must raise ValueError when no key is available."""
    monkeypatch.delenv("TRUSTOS_API_KEY", raising=False)
    with pytest.raises(ValueError, match="No API key provided"):
        TrustOSClient()


def test_reads_api_key_from_env(monkeypatch):
    """Client reads API key from TRUSTOS_API_KEY env var."""
    monkeypatch.setenv("TRUSTOS_API_KEY", _API_KEY)
    client = TrustOSClient()
    assert client._api_key == _API_KEY


def test_explicit_api_key_takes_precedence(monkeypatch):
    """Explicit api_key= overrides the environment variable."""
    monkeypatch.setenv("TRUSTOS_API_KEY", "env_key")
    client = TrustOSClient(api_key="explicit_key")
    assert client._api_key == "explicit_key"


def test_trailing_slash_removed():
    """Trailing slashes are stripped from base_url."""
    client = TrustOSClient(api_key=_API_KEY, base_url="https://example.com///")
    assert client._base_url == "https://example.com"


def test_default_base_url():
    """Default base URL points to the production gateway."""
    client = TrustOSClient(api_key=_API_KEY)
    assert "api.trust-os.io" in client._base_url


# ── verify_decision ───────────────────────────────────────────────────────────


@resp_mock.activate
def test_verify_decision_posts_to_correct_url():
    """verify_decision sends a POST to /v1/decision/verify."""
    resp_mock.add(
        resp_mock.POST,
        _VERIFY_URL,
        json=_MOCK_RESPONSE,
        status=200,
    )
    client = TrustOSClient(api_key=_API_KEY)
    result = client.verify_decision(_PAYLOAD)
    assert result["decision_id"] == "dec_example_001"
    assert len(resp_mock.calls) == 1
    assert resp_mock.calls[0].request.method == "POST"
    assert "/v1/decision/verify" in resp_mock.calls[0].request.url


@resp_mock.activate
def test_x_api_key_header_is_set():
    """The x-api-key header is present on every request."""
    resp_mock.add(resp_mock.POST, _VERIFY_URL, json=_MOCK_RESPONSE, status=200)
    client = TrustOSClient(api_key=_API_KEY)
    client.verify_decision(_PAYLOAD)
    assert resp_mock.calls[0].request.headers.get("x-api-key") == _API_KEY


@resp_mock.activate
def test_verify_alias_calls_verify_decision():
    """verify() is a transparent alias for verify_decision()."""
    resp_mock.add(resp_mock.POST, _VERIFY_URL, json=_MOCK_RESPONSE, status=200)
    client = TrustOSClient(api_key=_API_KEY)
    result = client.verify(_PAYLOAD)
    assert result["recommendation"] == "APPROVE"
    assert len(resp_mock.calls) == 1


@resp_mock.activate
def test_non_2xx_raises_trustos_error():
    """Non-2xx responses raise TrustOSError with the status code."""
    resp_mock.add(
        resp_mock.POST,
        _VERIFY_URL,
        json={"error": "unauthorized", "message": "Invalid API key"},
        status=401,
    )
    client = TrustOSClient(api_key="bad_key")
    with pytest.raises(TrustOSError) as exc_info:
        client.verify_decision(_PAYLOAD)
    assert exc_info.value.status_code == 401
    assert "401" in str(exc_info.value)


@resp_mock.activate
def test_rate_limit_raises_trustos_error():
    """429 responses raise TrustOSError."""
    resp_mock.add(
        resp_mock.POST,
        _VERIFY_URL,
        json={"error": "rate_limit_exceeded", "message": "Too many requests"},
        status=429,
    )
    client = TrustOSClient(api_key=_API_KEY)
    with pytest.raises(TrustOSError) as exc_info:
        client.verify_decision(_PAYLOAD)
    assert exc_info.value.status_code == 429


@resp_mock.activate
def test_invalid_json_raises_trustos_error():
    """A non-JSON response body raises TrustOSError."""
    resp_mock.add(
        resp_mock.POST,
        _VERIFY_URL,
        body="not json at all",
        status=200,
        content_type="text/plain",
    )
    client = TrustOSClient(api_key=_API_KEY)
    with pytest.raises(TrustOSError, match="Invalid JSON"):
        client.verify_decision(_PAYLOAD)


@resp_mock.activate
def test_response_body_attached_on_error():
    """TrustOSError.response_body contains the raw error text."""
    error_body = json.dumps({"error": "internal_error", "message": "Internal server error"})
    resp_mock.add(
        resp_mock.POST,
        _VERIFY_URL,
        body=error_body,
        status=500,
        content_type="application/json",
    )
    client = TrustOSClient(api_key=_API_KEY)
    with pytest.raises(TrustOSError) as exc_info:
        client.verify_decision(_PAYLOAD)
    assert exc_info.value.response_body is not None
    assert "internal_error" in exc_info.value.response_body
