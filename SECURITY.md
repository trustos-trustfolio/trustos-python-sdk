# Security Policy

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Report security issues by email to: **founder@trust-os.io**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested remediation

We aim to acknowledge reports within 48 hours and provide a fix timeline within 5 business days.

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ |

## API Key Security

- Store API keys in environment variables (`TRUSTOS_API_KEY`), not in source code.
- Never commit `.env` files to version control.
- Rotate keys immediately if you suspect exposure.
- Use server-side environments only — never expose keys in browser JavaScript.
