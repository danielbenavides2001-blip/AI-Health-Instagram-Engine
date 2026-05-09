import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from tools.common.messenger import Messenger
from tools.text_generation.gemini import GeminiTextGenerator

load_dotenv()

class DailyAutomator:
    def __init__(self):
        self.text_gen = GeminiTextGenerator()
        self.history_file = Path("flows/image_content_generator/out_short/automated_posts_history.csv")
        if not self.history_file.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self.history_file.write_text("date,type,topic\n")

    def get_recent_topics(self) -> str:
        import pandas as pd
        topics = []
        # 1. Get automated posts history
        if self.history_file.exists():
            try:
                df_auto = pd.read_csv(self.history_file)
                topics.extend(df_auto["topic"].tail(50).tolist())
            except Exception:
                pass
        
        # 2. Get video titles history
        video_csv = Path("flows/image_content_generator/out_short/ideas_tracking.csv")
        if video_csv.exists():
            try:
                df_video = pd.read_csv(video_csv)
                topics.extend(df_video["title"].tail(50).tolist())
            except Exception:
                pass
            
        if not topics:
            return ""
        
        # Deduplicate and format
        unique_topics = list(set([str(t).strip() for t in topics if str(t).strip()]))
        avoid_list = "\n- ".join(unique_topics[-40:]) # Last 40 unique topics
        return f"\n\n**CRÍTICO - REGLAS ANTI-REPETICIÓN (VERDADES BRUTALES):**\nESTÁ ESTRICTAMENTE PROHIBIDO repetir o inspirarse en los siguientes temas o títulos (YA HAN SIDO ATACADOS):\n- {avoid_list}\n\n**INSTRUCCIÓN OBLIGATORIA:** Rota entre los 4 PILARES (Físico, Mental, Rutina, Entorno). Si antes hablaste de dopamina barata (Mental), ahora ataca el trasnochar (Rutina) o los amigos mediocres (Entorno)."

    def sync_to_github(self):
        """
        Commits and pushes the history files back to GitHub to persist memory between runs.
        """
        Messenger.info("🔄 Syncing Instagram history and state to GitHub...")
        try:
            # Files to track
            files_to_sync = [
                str(self.history_file),
                "flows/image_content_generator/out_short/ideas_tracking.csv"
            ]
            
            # Check which files exist before adding
            existing_files = [f for f in files_to_sync if Path(f).exists()]
            
            if not existing_files:
                Messenger.warning("⚠️ No history files found to sync.")
                return

            # Git commands
            subprocess.run(["git", "config", "--global", "user.name", "Automated Bot"], check=True)
            subprocess.run(["git", "config", "--global", "user.email", "bot@automation.com"], check=True)
            
            for f in existing_files:
                subprocess.run(["git", "add", "-f", f], check=True)
            
            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
            if not status.strip():
                Messenger.info("✨ No changes in Instagram history to sync.")
                return

            subprocess.run(["git", "commit", "-m", "chore: update instagram post history [skip ci]"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            Messenger.success("✅ Instagram history successfully synced to GitHub!")
        except Exception as e:
            Messenger.error(f"❌ Failed to sync Instagram history to GitHub: {e}")

    def run_daily_mix(self):
        Messenger.info("🚀 Starting Daily Automated Content Picker (Instagram Reels Cycle)...")
        
        # In Instagram, we only want Video Reels (Choice 2)
        choice = 2
        Messenger.info("🔄 Forcing Video Reel generation for Instagram Growth (Cyber-Organic Style).")

        try:
            if choice == 2:
                # Video generation
                Messenger.info("🎬 GENERATING NEW INSTAGRAM REEL (Steps 1-8)...")
                avoid_msg = self.get_recent_topics()
                # We call the main pipeline module for short videos
                subprocess.run([sys.executable, "-m", "flows.image_content_generator.pipeline.main", "short", "all", "--avoid", avoid_msg], check=True)
            
        except Exception as e:
            Messenger.error(f"Error during automated task: {e}")
            sys.exit(1)

        Messenger.success("✅ Automated Instagram task execution completed!")
        self.sync_to_github()

if __name__ == "__main__":
    automator = DailyAutomator()
    automator.run_daily_mix()
