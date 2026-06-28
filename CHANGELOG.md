# Changelog

All notable changes to the Trust OS Python SDK are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-06-28

### Added

- `TrustOSClient` with `verify_decision()` and `verify()` alias
- Reads API key from `TRUSTOS_API_KEY` environment variable
- Custom `TrustOSError` with `status_code` and `response_body` attributes
- Examples: basic, stablecoin payment, treasury approval, AI agent action
- Full pytest test suite with `responses` mocking
- `pyproject.toml` with modern packaging metadata
