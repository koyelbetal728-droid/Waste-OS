# Staging

No staging environment is provisioned in this scaffold. When you have one:
point `DATABASE_URL`/`REDIS_URL` at managed instances, set `APP_ENV=staging`,
and build the same three Dockerfiles (infra/docker/) behind your CI/CD
pipeline (.github/workflows/deploy.yml is currently a manual-trigger
placeholder — wire it here).
