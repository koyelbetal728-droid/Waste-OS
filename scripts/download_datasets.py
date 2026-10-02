"""No dataset download is bundled — this environment has no network access
to fetch TrashNet/TACO/etc. This script documents where to put data you
download yourself so the rest of the pipeline (dataset.py/train.py) picks
it up automatically:

    data/raw/waste/<category>/*.jpg   (e.g. data/raw/waste/plastic/*.jpg)

One folder per class, matching the TrashNet/TACO layout. Once populated,
run `python -m scripts.train_models`.
"""

if __name__ == "__main__":
    print(__doc__)
