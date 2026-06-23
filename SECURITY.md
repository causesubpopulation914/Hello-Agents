# Security Policy

## Supported Versions

Hello-Agents is an educational tutorial repository. Security considerations apply primarily to the code examples provided.

| Version | Supported |
|---------|-----------|
| Latest (`main`) | ✅ |

## Reporting a Vulnerability

If you discover a security issue in the code examples or tutorial content (e.g., insecure patterns being taught, credentials accidentally committed, dependency with known CVE), please:

1. **Do not** open a public issue
2. **Email** the maintainers via GitHub's private vulnerability reporting feature
3. Include a description of the issue and steps to reproduce

We will respond within **7 business days** and work to fix it promptly.

## Security Best Practices in This Tutorial

The code examples in this tutorial follow these security practices:

- **No hardcoded secrets** — all API keys are loaded from environment variables via `.env` files
- **`.gitignore` configured** — `.env` files are never committed
- **Dependency pinning** — `requirements.txt` pins known-good versions

If you see any example in the tutorial that violates these practices, please report it.
