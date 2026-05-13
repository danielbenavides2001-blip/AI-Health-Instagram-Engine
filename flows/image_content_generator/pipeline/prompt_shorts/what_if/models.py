from typing import List, Optional
from pydantic import Field
from flows.image_content_generator.pipeline.prompt_base.models import (
    BaseIdea,
    CategoryHandler,
)
from flows.image_content_generator.pipeline.prompt_shorts.what_if import (
    constants as what_if_constants,
)

class WhatIfIdea(BaseIdea):
    """Specific model for the 'What If' niche."""
    IDEA_PROMPT = what_if_constants.IDEA_PROMPT_MINDSET
    scientific_explanation: str = Field(..., description="The sequence of biological events.")
    practical_benefit: str = Field(..., description="A real-world lesson or survival tip.")

class WhatIfHandler(CategoryHandler):
    """Handler for the 'What If' (Curiosidad Brutal) niche."""
    
    idea_variants = [WhatIfIdea]

    @classmethod
    def get_full_script_prompt(cls, idea: WhatIfIdea) -> str:
        # Use custom prompt for this niche
        return f"""{what_if_constants.SCRIPT_PROMPT}

# CONTEXTO DE LA IDEA SELECCIONADA:
- **Escenario:** {idea.title}
- **Gancho:** {idea.hook}
- **Explicación Científica:** {idea.scientific_explanation}
- **Lección Final:** {idea.practical_benefit}

Genera el guion completo (10 escenas) en formato JSON que cumpla con los esquemas de VideoScript.
"""
