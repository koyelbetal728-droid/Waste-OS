# Local Deployment

```
cp .env.example .env
docker compose up --build
```

Services: postgres (with PostGIS), redis, api (:8000), worker, web (:3000).
Shared `storage` volume holds uploaded scan images so api and worker both
see them.

No production deployment target is configured — `.github/workflows/deploy.yml`
is a manual-trigger placeholder. Wire it to your actual infrastructure
before enabling.
