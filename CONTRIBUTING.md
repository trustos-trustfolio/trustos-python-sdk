# Contributing

Thank you for your interest in contributing to the Trust OS Python SDK.

## Development Setup

```bash
git clone https://github.com/trustos-trustfolio/trustos-python-sdk.git
cd trustos-python-sdk
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

- Follow PEP 8.
- Keep the client minimal — do not add dependencies beyond `requests`.
- All public methods must have docstrings.
- Tests must not call the real API. Use the `responses` library for mocking.

## Pull Requests

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Add tests for new behavior.
4. Run `pytest` and ensure all tests pass.
5. Open a pull request against `main`.

## Reporting Issues

Use the GitHub Issue templates:
- **Bug Report** — for unexpected behavior.
- **Feature Request** — for new functionality proposals.
