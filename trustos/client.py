"""Trust OS Python SDK — Decision Verification API client."""

from __future__ import annotations

import os
from typing import Any

import requests


DEFAULT_BASE_URL = "https://api.trust-os.io"
_VERIFY_PATH = "/v1/decision/verify"


class TrustOSError(Exception):
    """Raised when the Trust OS API returns a non-2xx response or an
    unexpected payload.

    Attributes:
        status_code: HTTP status code, or None for network/parse errors.
        response_body: Raw response text, or None when unavailable.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __repr__(self) -> str:
        return (
            f"TrustOSError(status_code={self.status_code!r}, "
            f"message={str(self)!r})"
        )


class TrustOSClient:
    """Client for the Trust OS Decision Verification API.

    Args:
        api_key: API key for authentication. If *None*, the value of the
            ``TRUSTOS_API_KEY`` environment variable is used instead.
        base_url: Override the API base URL. Trailing slashes are removed
            automatically. Defaults to the production gateway.
        timeout: Request timeout in seconds. Defaults to 10.0.

    Raises:
        ValueError: If no API key is provided and ``TRUSTOS_API_KEY`` is
            not set in the environment.

    Example::

        from trustos import TrustOSClient

        client = TrustOSClient(api_key="YOUR_API_KEY")
        result = client.verify_decision({"action": "stablecoin_transfer"})
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        resolved_key = api_key or os.environ.get("TRUSTOS_API_KEY")
        if not resolved_key:
            raise ValueError(
                "No API key provided. Pass api_key= to TrustOSClient() "
                "or set the TRUSTOS_API_KEY environment variable."
            )
        self._api_key = resolved_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "x-api-key": self._api_key,
            "User-Agent": "trustos-python-sdk/0.1.0",
        })

    def verify_decision(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit a decision payload for verification.

        Args:
            payload: Decision fields. ``action`` is the only required key.
                Optional keys: ``amount``, ``currency``, ``destination``,
                ``source``, ``priority``, ``metadata``.

        Returns:
            Parsed JSON response containing ``decision_id``,
            ``recommendation``, ``risk_score``, ``risk_level``, ``policy``,
            ``proof_hash``, ``verified``, and ``latency_ms``.

        Raises:
            TrustOSError: On non-2xx HTTP status or unparseable response.
        """
        url = f"{self._base_url}{_VERIFY_PATH}"
        try:
            response = self._session.post(url, json=payload, timeout=self._timeout)
        except requests.RequestException as exc:
            raise TrustOSError(f"Request failed: {exc}") from exc

        if not response.ok:
            try:
                body = response.text
            except Exception:
                body = None
            raise TrustOSError(
                f"API error {response.status_code}: {response.reason}",
                status_code=response.status_code,
                response_body=body,
            )

        try:
            return response.json()
        except ValueError as exc:
            raise TrustOSError(
                "Invalid JSON in API response",
                status_code=response.status_code,
                response_body=response.text,
            ) from exc

    def verify(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Alias for :meth:`verify_decision`."""
        return self.verify_decision(payload)
