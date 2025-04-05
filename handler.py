import runpod
import os
import base64
import numpy as np
import soundfile as sf
from kokoro import KModel, KPipeline
import tempfile
import uuid
import tempfile
from pydub import AudioSegment
import io
import torch

# Mapping of supported language codes
LANGUAGE_MAP = {
    "en-us": "a",  # American English
    "en-gb": "b",  # British English
    "es": "e",     # Spanish
    "fr": "f",     # French
    "hi": "h",     # Hindi
    "it": "i",     # Italian
    "ja": "j",     # Japanese
    "pt-br": "p",  # Brazilian Portuguese
    "zh": "z"      # Chinese
}

# Store pipelines for different languages
pipelines = {}
REPO_ID = 'hexgrad/Kokoro-82M-v1.1-zh'


# Get or create language pipeline
def get_pipeline(lang_code):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = KModel(repo_id=REPO_ID).to(device).eval()
    code = LANGUAGE_MAP.get(lang_code, "a")  # Default fallback to American English
    pipelines[lang_code] = KPipeline(lang_code=code, repo_id="hexgrad/Kokoro-82M-v1.1-zh", model=model, device=device)
    return pipelines[lang_code]


def handler(job):
    """
    # RunPod handler function

    # Input parameters:
    - text: Text to convert (required)
    - voice: Voice ID to use (default: zf_xiaobei)
    - language: Language code (default: zh)
    - speed: Speech rate (default: 1.0)
    - split_sentences: Whether to split by sentence (default: true)

    # Returns:
    - audio_base64: Base64 encoded audio data
    - message: Processing status message
    """
    job_input = job["input"]

    # Get input parameters
    text = job_input.get("text")
    if not text:
        return {"error": "The 'text' parameter must be provided"}

    voice = job_input.get("voice", "af_heart")
    language = job_input.get("language", "en-us")
    speed = float(job_input.get("speed", 1.0))
    split_sentences = bool(job_input.get("split_sentences", True))

    try:
        # Check language support
        if language not in LANGUAGE_MAP:
            return {"error": f"Unsupported language: {language}"}

        # Get language pipeline
        pipeline = get_pipeline(language)

        # Set split mode
        split_pattern = r'\n+' if split_sentences else None

        # Generate audio
        all_audio = []
        generator = pipeline(
            text,
            voice=voice,
            speed=speed,
            split_pattern=split_pattern
        )

        for i, (gs, ps, audio) in enumerate(generator):
            all_audio.append(audio)

        # If there are multiple segments, merge them
        if len(all_audio) > 1:
            combined_audio = np.concatenate(all_audio)
        else:
            combined_audio = all_audio[0] if all_audio else None

        if combined_audio is None:
            return {"error": "Failed to generate audio"}

        # Create a temporary file to save audio
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
            sf.write(temp_path, combined_audio, 24000)

        # Convert WAV to MP3
        wav_audio = AudioSegment.from_wav(temp_path)
        mp3_io = io.BytesIO()
        wav_audio.export(mp3_io, format="mp3", bitrate="192k")
        mp3_data = mp3_io.getvalue()

        # Convert MP3 data to base64
        audio_base64 = base64.b64encode(mp3_data).decode("utf-8")

        # Delete temporary file
        os.unlink(temp_path)

        # Return result
        return {
            "audio_base64": audio_base64,
            "message": "Successfully generated speech"
        }

    except Exception as e:
        return {"error": f"Error processing request: {str(e)}"}


def adjust_concurrency(current_concurrency):
    return 20


# Start RunPod Serverless
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler, "concurrency_modifier": adjust_concurrency})
