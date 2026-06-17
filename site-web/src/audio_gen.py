"""
CyberDailyWatch - Générateur Audio
Synthèse vocale avec edge-tts (Microsoft Azure Neural Voices)
"""

import asyncio
import edge_tts
from pathlib import Path

VOICE = "fr-FR-HenriNeural"  # Alternatives: fr-FR-DeniseNeural (femme)


async def generate_audio(text: str, output_path: Path, voice: str = VOICE) -> Path:
    """Génère un fichier MP3 à partir du texte."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output_path))
    return output_path


def generate_audio_sync(text: str, output_path: Path, voice: str = VOICE) -> Path:
    """Version synchrone de generate_audio."""
    return asyncio.run(generate_audio(text, output_path, voice))


if __name__ == "__main__":
    test_text = "Bonjour, ceci est un test de génération audio."
    output = generate_audio_sync(test_text, Path("test_audio.mp3"))
    print(f"✅ Audio généré: {output} ({output.stat().st_size / 1024:.1f} Ko)")
