"""Flag definitions — one place to see every toggle the platform has."""

DEFAULT_FLAGS = {
    "video_scanning": False,          # packages/ai/multimodal/video.py is unsupported without OpenCV
    "object_storage": False,          # no cloud credentials configured — local storage only
    "llm_advisory": True,             # degrades gracefully to deterministic fallback if Ollama is down
    "async_recycler_matching": True,  # worker task vs synchronous
}
