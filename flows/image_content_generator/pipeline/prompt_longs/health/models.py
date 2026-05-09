from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler
from flows.image_content_generator.pipeline.prompt_longs.health import (
    constants as health_long_constants,
)


class MindsetHealthIdeaLong(BaseIdea):
    """
    Deep idea model for long-form health mindset transformation stories.
    """
    IDEA_PROMPT = health_long_constants.IDEA_PROMPT_MINDSET
    health_problem: str
    mindset_shift: str
    key_principle: str


class StrategyHealthIdeaLong(BaseIdea):
    """
    Deep idea model for long-form practical health strategy videos.
    """
    IDEA_PROMPT = health_long_constants.IDEA_PROMPT_ESTRATEGIA
    strategy_name: str
    common_mistake: str
    actionable_tip: str


class HealthHandlerLong(CategoryHandler):
    """
    Specialized handler for Long Health-themed videos.
    Encapsulates Mindset and Strategy health variants for 10-minute content.
    """

    SCRIPT_PROMPT = health_long_constants.SCRIPT_PROMPT
    idea_variants = [
        MindsetHealthIdeaLong,
        StrategyHealthIdeaLong,
    ]
