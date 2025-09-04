from pathlib import Path
import httpx
from .config import settings

def azure_tts(text: str, out_wav: str, voice="en-US-JennyNeural", rate="+0%", pitch="+0st"):
    """Neural TTS via Azure Cognitive Services."""
    if not (settings.azure_tts_key and settings.azure_tts_region):
        raise RuntimeError("Azure TTS not configured")
    ssml = f"""
<speak version="1.0" xml:lang="en-US">
  <voice name="{voice}">
    <prosody rate="{rate}" pitch="{pitch}">{text}</prosody>
  </voice>
</speak>""".strip()
    url = f"https://{settings.azure_tts_region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": settings.azure_tts_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
    }
    r = httpx.post(url, content=ssml.encode("utf-8"), headers=headers, timeout=60)
    r.raise_for_status()
    Path(out_wav).write_bytes(r.content)
    return out_wav
