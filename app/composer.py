import subprocess, shlex
from .logging_conf import logger

FFMPEG_BIN = "ffmpeg"

def make_vertical_short(bg_video: str, voiceover_wav: str, music_wav: str | None, srt_file: str, out_mp4: str):
    """
    - Fit/crop to 1080x1920
    - Burn SRT
    - Mix VO + (optional) music with ducking + loudness
    """
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
    subs = f"subtitles={shlex.quote(srt_file)}:force_style='Fontsize=28,OutlineColour=&H80000000,BorderStyle=3,PrimaryColour=&HFFFFFF'"
    vfilters = f"{vf},{subs}"

    if music_wav:
        afilters = (
            "[1:a]loudnorm=I=-16:LRA=11:TP=-1.5[vo];"
            "[2:a]anull[bg];"
            "[bg][vo]sidechaincompress=threshold=0.04:ratio=8:attack=5:release=200:makeup=3[mix];"
            "[mix]loudnorm=I=-14:LRA=11:TP=-1.5"
        )
        inputs = ["-i", bg_video, "-i", voiceover_wav, "-i", music_wav]
    else:
        afilters = "[1:a]loudnorm=I=-14:LRA=11:TP=-1.5"
        inputs = ["-i", bg_video, "-i", voiceover_wav]

    cmd = [
        FFMPEG_BIN, "-y",
        *inputs,
        "-filter:v", vfilters,
        "-filter:a", afilters,
        "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        out_mp4,
    ]
    logger.info("FFmpeg: " + " ".join(cmd))
    subprocess.run(cmd, check=True)
    return out_mp4
