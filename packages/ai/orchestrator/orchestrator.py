"""Ties vision, domain rules, RAG and LLM together behind one call. The
LLM/RAG layer only ever produces explanatory text — the recyclability/
hazard decision always comes from packages/waste (deterministic), never
from the model."""
from packages.ai.orchestrator.context import AIContext
from packages.ai.orchestrator.router import route
from packages.ai.orchestrator.safety import sanitize_advisory
from packages.ai.multimodal.image import process_image
from packages.ai.multimodal.text import process_text
from packages.waste.recyclability import determine_recyclability
from packages.waste.hazard import screen_hazard


def handle_request(context: AIContext) -> dict:
    steps = route(context)
    result: dict = {"steps_run": steps}

    if "vision" in steps:
        vision_result = process_image(context.image_bytes)
        result["vision"] = vision_result
        if vision_result.get("status") == "ok":
            result["recyclability"] = determine_recyclability(
                vision_result["material"], vision_result["contamination_level"], vision_result["confidence"]
            ).value
            result["hazard"] = screen_hazard(vision_result["category"], vision_result["confidence"])

    if "rag" in steps or "llm" in steps:
        text_result = process_text(context.user_question)
        text_result["answer"] = sanitize_advisory(text_result["answer"])
        result["advisory"] = text_result

    return result
