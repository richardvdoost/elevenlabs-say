import argparse
import hashlib
import logging
import os
import pickle
import random
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    CACHE_DIR = Path(
        os.path.join(os.getenv("XDG_CACHE_HOME", "~/.cache"), "elevenlabs")
    )
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_VOICE_NAME = os.getenv("DEFAULT_VOICE_NAME", "Sarah")

    client = ElevenLabs()
    voices = get_voices(client, CACHE_DIR)
    voice_names = [voice.name for voice in voices if type(voice.name) is str]

    args = parse_args(["Any", "Male", "Female", "All"] + voice_names)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug(f"Voices: {voice_names}")

    text = " ".join(args.text)
    model_id = get_latest_model(client, CACHE_DIR)

    if args.voice == "All":
        success = False
        for voice in voice_names:
            logger.debug(voice)
            success = say(client, text, voice, model_id, CACHE_DIR)

        return 0 if success else 1

    voice_choices = None
    if args.voice == "Any":
        voice_choices = voice_names

    if args.voice in {"Male", "Female"}:
        voice_choices = [
            v.name
            for v in voices
            if v.labels and v.labels.get("gender") == args.voice.lower()
        ]

    if voice_choices:
        voice = random.choice(voice_choices)
    else:
        voice = args.voice or DEFAULT_VOICE_NAME

    assert type(voice) is str

    success = say(client, text, voice, model_id, CACHE_DIR)

    return 0 if success else 1


def get_voices(client: ElevenLabs, cache_dir: Path):
    voices_path = Path(os.path.join(cache_dir, "voices.pickle"))

    if voices_path.is_file():
        logger.debug("Loading voices from cache")
        with open(voices_path, "rb") as fp:
            voices = pickle.load(fp)
    else:
        logger.debug("Fetching voices from API")
        voices = client.voices.get_all().voices
        with open(voices_path, "wb") as fp:
            pickle.dump(voices, fp)

    return voices


def parse_args(voice_names: list[str]):
    parser = argparse.ArgumentParser(
        "say", description="Convert text to audible speech"
    )
    parser.add_argument("text", nargs="+")
    parser.add_argument("-v", "--voice", type=str, choices=voice_names)
    parser.add_argument("-d", "--debug", action="store_true")

    return parser.parse_args()


def get_latest_model(client: ElevenLabs, cache_dir: Path):
    models_path = Path(os.path.join(cache_dir, "models.pickle"))

    if models_path.is_file():
        logger.debug("Loading models from cache")
        with open(models_path, "rb") as fp:
            models = pickle.load(fp)
    else:
        logger.debug("Fetching models from API")
        try:
            models = client.models.get_all()
        except:
            models = []
        with open(models_path, "wb") as fp:
            pickle.dump(models, fp)

    return models[0].model_id if len(models) else "eleven_monolingual_v1"


def say(client: ElevenLabs, text: str, voice: str, model_id: str, cache_dir: Path):
    logger.debug(f"Picking voice: {voice}")

    key = f"{voice}:{text}"
    hash = hashlib.sha256(key.encode()).hexdigest()

    filepath = cache_dir / "audio" / hash
    filepath = filepath.with_suffix(".mp3")

    if not filepath.is_file():
        logger.debug("Generating and playing audio")

        try:
            audio = client.generate(text=text, voice=voice, model=model_id)
            save(audio, str(filepath))

        except Exception:
            # logger.error("Failed to generate audio")
            # logger.exception(e)

            return False
    else:
        logger.debug(f"Playing audio from cache: {filepath}")

    try:
        with open(filepath, "rb") as fp:
            play(fp)

    except Exception:
        # logger.error("Failed to play audio")
        # logger.exception(e)
        # logger.debug("Removing cache audio file")
        filepath.unlink()

        return False

    return True


if __name__ == "__main__":
    exit(main())
