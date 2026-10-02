# Security Policy

This is a scaffold/reference implementation, not an audited production
system. Before deploying with real user data:

- Rotate `JWT_SECRET` and never commit `.env`.
- Replace the in-memory rate limiter with a Redis-backed one for
  multi-replica deployments.
- Configure a real secrets manager (see `infra/secrets/README.md`).
- Review `packages/security/permissions.py` for every role before granting
  production access.

Report vulnerabilities by opening a private security advisory rather than
a public issue.
