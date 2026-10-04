"""Kept for backwards compatibility. The real dataset fetcher is
scripts/fetch_datasets.py, which downloads the YOLO detection set from Roboflow
(or from any zip URL you pass it), verifies the split counts and class names,
and stages it onto local disk so training is not throttled by OneDrive.

    $env:ROBOFLOW_API_KEY="your-key"
    python -m scripts.fetch_datasets --all

Nothing under data/raw/ is committed, so a fresh clone must run this first.
"""

if __name__ == "__main__":
    print(__doc__)