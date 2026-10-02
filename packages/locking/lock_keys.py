"""Centralized lock key names so two callers never accidentally use
different strings for what should be the same lock."""

HOTSPOT_DETECTION = "hotspot_detection"
MODEL_MONITORING = "model_monitoring"
ROUTE_REOPTIMIZATION = "route_reoptimization"
FORECAST_JOB = "forecast_job"
