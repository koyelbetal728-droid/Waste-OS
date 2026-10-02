"""Notification copy templates — kept out of the sending code so wording
changes don't require touching delivery logic."""

TEMPLATES = {
    "pickup_assigned": "Your pickup has been assigned to a collector.",
    "pickup_collected": "Your waste has been collected — check your Waste Passport.",
    "reward_earned": "You earned {points} Green Points for {reason}.",
    "listing_purchased": "Your listing for {material} was purchased.",
    "report_resolved": "Your report has been marked resolved.",
}


def render(template_key: str, **kwargs) -> str:
    template = TEMPLATES.get(template_key)
    if not template:
        return f"Notification: {template_key}"
    try:
        return template.format(**kwargs)
    except KeyError:
        return template
