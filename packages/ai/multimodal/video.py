"""Video-modality entry point. Frame sampling only — never processes every
frame. Uses stdlib-only sampling (no OpenCV/ffmpeg dependency bundled), so
this returns a clear 'unsupported' status rather than silently doing
nothing; wire a real frame extractor (OpenCV) before enabling in production."""


def process_video(video_bytes: bytes, sample_every_n_seconds: int = 2) -> dict:
    return {
        "status": "unsupported",
        "reason": "No frame-extraction backend (OpenCV/ffmpeg) is installed in this "
                  "environment. Add opencv-python and implement frame sampling here "
                  "before enabling video scanning.",
    }
