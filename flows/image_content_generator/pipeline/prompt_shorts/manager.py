import json
from pathlib import Path
from typing import Sequence, Tuple, Type

from flows.image_content_generator.pipeline.prompt_base.manager import BasePromptManager
from flows.image_content_generator.pipeline.prompt_base.models import (
    BaseIdea,
    CategoryHandler,
    VideoScript,
)
from flows.image_content_generator.pipeline.prompt_shorts.health import (
    constants as health_constants,
)
from flows.image_content_generator.pipeline.prompt_shorts.health.models import HealthHandler, ScienceBiohackIdea
from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator


class PromptManagerShorts(BasePromptManager):
    """Manager specific to Short videos (9:16), aggregating modular categories."""

    # Health voice & audio style
    AUDIO_PROMPT: str = health_constants.AUDIO_PROMPT

    CATEGORIES: Sequence[Type[CategoryHandler]] = [
        HealthHandler,
    ]

    def generate_full_story(
        self, content_gen: GeminiTextGenerator, titles_to_avoid: list[str] = [], extra_avoid: str = ""
    ) -> Tuple[BaseIdea, VideoScript, str]:
        """
        Executes the generation loop in 3 steps:
        1. Predefined Check: Use manual scripts if available.
        2. Random Selection: Pick a category config.
        3. Idea Generation: Prompt for initial idea.
        4. Script Generation: Build structured script from idea.
        """
        # 1. Predefined Check
        predefined_dir = Path(__file__).parent / "predefined"
        if predefined_dir.exists():
            files = sorted(list(predefined_dir.glob("*.json")))
            for f in files:
                try:
                    with open(f, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        title = data.get("idea", {}).get("title")
                        if title and title in titles_to_avoid:
                            continue
                        
                        Messenger.info(f"Using predefined script: {f.name}")
                        # Use model_construct to allow missing internal fields in manual scripts
                        idea_data = ScienceBiohackIdea.model_construct(**data["idea"])
                        if not idea_data.title: idea_data.title = title
                        if not idea_data.hook: idea_data.hook = data.get("idea", {}).get("hook", "")
                        
                        script = VideoScript(**data["script"])
                        return idea_data, script, "health"
                except Exception as e:
                    Messenger.error(f"Error loading predefined script {f.name}: {e}")

        # 2. Random Selection
        config = self.select_random_config()

        # 2. Idea Generation
        avoid_msg = ""
        if extra_avoid:
            avoid_msg = f"\n\n🚨 **REGLA CRÍTICA DE NO REPETICIÓN:** 🚨\n{extra_avoid}"
        elif titles_to_avoid:
            avoid_list_str = "\n- ".join(titles_to_avoid)
            avoid_msg = f"\n\n**REGLA CRÍTICA Y ESTRICTA: BAJO NINGÚN CONCEPTO repitas los hábitos o debilidades mediocres de los videos que ya creaste. Debes atacar una DEBILIDAD COMPLETAMENTE DISTINTA a estas:**\n- {avoid_list_str}\n\n**IMPORTANTE:** Rota entre los 4 PILARES (Físico, Mental, Rutina, Entorno). Destruye excusas nuevas en cada ejecución."

        idea_data = content_gen.generate_text(config.idea_prompt + avoid_msg, config.idea_model)

        # 3. Script Generation
        Messenger.info(f"\n--- Generating script for: {idea_data.title} ---")
        script_prompt = config.handler.get_full_script_prompt(idea_data)
        Messenger.info(script_prompt)
        script = content_gen.generate_text(script_prompt, VideoScript)

        return idea_data, script, config.category
