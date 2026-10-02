# ADR 002: PostgreSQL + PostGIS

**Decision:** PostgreSQL as the single source of truth, PostGIS for spatial
queries (hotspots, facility proximity).
**Status:** Hotspots currently use plain lat/lon columns + pure-Python
haversine clustering (packages/geospatial/hotspot.py) rather than real
PostGIS geometry — see db/postgis/spatial_indexes.sql for the documented
migration path once query volume justifies it.
