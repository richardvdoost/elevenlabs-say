import argparse
import hashlib
import logging
import os
import pickle
import random
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import generate
from elevenlabs import play
from elevenlabs import save
from elevenlabs import stream
from elevenlabs import voices as elevenlabs_voices
from elevenlabs.api import Models

load_dotenv()

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main():
    CACHE_DIR = Path(
        os.path.join(os.getenv("XDG_CACHE_HOME", "~/.cache"), "elevenlabs")
    )
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    voices = get_voices(CACHE_DIR)
    voice_names = [voice.name for voice in voices]
    args = parse_args(voice_names + ["All", "Random"])

    text = " ".join(args.text)
    model_id = get_latest_model(CACHE_DIR)

    if args.voice == "All":
        for voice in voice_names:
            logger.debug(voice)
            say(text, voice, model_id, CACHE_DIR)

        return 0

    if args.voice is None:
        female_voices = [
            v.name for v in voices if v.labels and v.labels.get("gender") == "female"
        ]
        voice = random.choice(female_voices) if female_voices else "Rachel"
        logger.debug(f"Picking random female voice: {voice}")

    else:
        logger.debug(f"Using voice {args.voice}")
        voice = random.choice(voice_names) if args.voice == "Random" else args.voice

    say(text, voice, model_id, CACHE_DIR)

    return 0


def get_voices(cache_dir: Path):
    voices_path = Path(os.path.join(cache_dir, "voices.pickle"))

    if voices_path.is_file():
        logger.debug("Loading voices from cache")
        with open(voices_path, "rb") as fp:
            voices = pickle.load(fp)
    else:
        logger.debug("Fetching voices from API")
        voices = elevenlabs_voices()
        with open(voices_path, "wb") as fp:
            pickle.dump(voices, fp)

    return voices


def parse_args(voice_names: list[str]):
    parser = argparse.ArgumentParser(
        "say", description="Convert text to audible speech"
    )
    parser.add_argument("text", nargs="+")
    parser.add_argument("-v", "--voice", type=str, choices=voice_names)

    return parser.parse_args()


def get_latest_model(cache_dir: Path):
    models_path = Path(os.path.join(cache_dir, "models.pickle"))

    if models_path.is_file():
        logger.debug("Loading models from cache")
        with open(models_path, "rb") as fp:
            models = pickle.load(fp)
    else:
        logger.debug("Fetching models from API")
        try:
            models = Models.from_api()
        except:
            models = []
        with open(models_path, "wb") as fp:
            pickle.dump(models, fp)

    return models[0].model_id if len(models) else "eleven_monolingual_v1"


def say(text: str, voice: str, model_id: str, cache_dir: Path):
    key = f"{voice}:{text}"
    hash = hashlib.sha256(key.encode()).hexdigest()

    filepath = Path(os.path.join(cache_dir, hash))

    if filepath.is_file():
        logger.debug("Playing audio from cache")
        with open(filepath, "rb") as fp:
            stream(fp)
    else:
        logger.debug("Generating and playing audio")
        audio = generate(text, voice=voice, model=model_id)
        assert type(audio) is bytes
        save(audio, str(filepath))
        play(audio)


if __name__ == "__main__":
    exit(main())
