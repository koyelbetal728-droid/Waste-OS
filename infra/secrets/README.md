No secrets manager is wired up. For local dev, `.env` (gitignored) is
sufficient. Before production: use your cloud provider's secrets manager
(AWS Secrets Manager, GCP Secret Manager, etc.) and inject via environment
variables — never commit real secrets to this directory.
