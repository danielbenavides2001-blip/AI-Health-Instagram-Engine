import argparse
from enum import Enum
from pathlib import Path

from flows.image_content_generator.pipeline.pipeline import Pipeline
from flows.image_content_generator.pipeline.schemas import VideoOrientation
from tools.common.messenger import Messenger

RESOURCE_BASE = Path("flows/image_content_generator/resource")
LONG_OUT_BASE = Path("flows/image_content_generator/out_long")
SHORT_OUT_BASE = Path("flows/image_content_generator/out_short")


class PipelineStep(str, Enum):
    ALL = "all"
    STEP1 = "step1"
    STEP2 = "step2"
    STEP3 = "step3"
    STEP4 = "step4"
    STEP5 = "step5"
    STEP6 = "step6"
    STEP7 = "step7"
    STEP8 = "step8"


def main():
    Messenger.info("🚀 Pipeline process started.")
    parser = argparse.ArgumentParser()
    parser.add_argument("orientation", type=VideoOrientation, choices=list(VideoOrientation))
    parser.add_argument("step", type=PipelineStep, choices=list(PipelineStep))
    parser.add_argument("--avoid", type=str, default="", help="List of topics to avoid")
    args = parser.parse_args()

    # Determine output base based on orientation
    out_base = SHORT_OUT_BASE if args.orientation == VideoOrientation.SHORT else LONG_OUT_BASE

    # Determine avoid list (prefer environment variable for length)
    import os
    avoid_msg = os.getenv("ENV_AVOID", args.avoid)

    pipeline = Pipeline(
        out_base=out_base,
        resource_base=RESOURCE_BASE,
        orientation=args.orientation
    )

    # Map Enum members to their corresponding pipeline methods
    # Note: step1 needs the avoid argument
    step_methods = {
        PipelineStep.STEP1: lambda: pipeline.step1_generate_story(extra_avoid=avoid_msg),
        PipelineStep.STEP2: pipeline.step2_generate_images,
        PipelineStep.STEP3: pipeline.step3_generate_audios,
        PipelineStep.STEP4: pipeline.step4_generate_videos,
        PipelineStep.STEP5: pipeline.step5_generate_subtitles,
        PipelineStep.STEP6: pipeline.step6_add_background_music,
        PipelineStep.STEP7: pipeline.step7_rename_final_video,
        PipelineStep.STEP8: pipeline.step8_upload_to_instagram,
    }

    # Define steps to execute (excluding 'all' itself)
    steps = [s for s in PipelineStep if s != PipelineStep.ALL]

    if args.step == PipelineStep.ALL:
        Messenger.info("--- Starting Full Pipeline Run (Steps 1-8) ---")
        for step in steps:
            step_methods[step]()
        Messenger.success("Full pipeline cycle completed successfully.")
    else:
        # Run specific step
        step_methods[args.step]()


if __name__ == "__main__":
    main()
