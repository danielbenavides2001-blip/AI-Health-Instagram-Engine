from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler
from flows.image_content_generator.pipeline.prompt_shorts.health import (
    constants as health_constants,
)


class ScienceBiohackIdea(BaseIdea):
    """
    Molde para videos de ciencia, neuropsicología y biohacking.
    """
    IDEA_PROMPT = health_constants.IDEA_PROMPT_MINDSET
    hook: str
    category: str
    scientific_explanation: str
    practical_benefit: str


class HealthHandler(CategoryHandler):
    """
    Specialized handler for Science and Biohacking.
    """

    SCRIPT_PROMPT = health_constants.SCRIPT_PROMPT
    idea_variants = [
        ScienceBiohackIdea,
    ]
