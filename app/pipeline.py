from pathlib import Path
from .config import settings
from .db import SessionLocal
from .models import Job
from .trends import get_trending_topics
from .scriptgen import generate_script
from .assets import fetch_pexels_broll
from .tts import azure_tts
from .captions import naive_line_split, write_srt
from .composer import make_vertical_short
from .seo import build_seo
from .youtube import upload_video, upload_captions

def run_pipeline(job_id: int):
    db = SessionLocal()
    job = db.get(Job, job_id)
    if not job:
        return

    try:
        job.status = "running"; db.commit()

        # 1) Topic → 2) Script
        topic = job.topic_hint or (get_trending_topics(job.locale, settings.channel_niche, 10) or ["ideas"])[0]
        script = generate_script(topic, settings.channel_niche)
        job.script = script; db.commit()

        # 3) Assets
        broll_dir = Path(settings.media_dir) / f"job_{job.id}" / "broll"
        paths = fetch_pexels_broll(topic, str(broll_dir), count=1)
        if not paths: raise RuntimeError("No background b-roll (configure PEXELS_API_KEY)")
        bg = paths[0]

        # 4) TTS
        audio_dir = Path(settings.media_dir) / f"job_{job.id}" / "audio"; audio_dir.mkdir(parents=True, exist_ok=True)
        vo_wav = str(audio_dir / "vo.wav"); azure_tts(script, vo_wav)

        # 5) Captions
        cap_dir = Path(settings.media_dir) / f"job_{job.id}" / "captions"; cap_dir.mkdir(parents=True, exist_ok=True)
        segs, _ = naive_line_split(script)
        srt_path = str(cap_dir / "captions.srt"); write_srt(segs, srt_path)
        job.captions_path = srt_path; db.commit()

        # 6) Compose 9:16
        renders_dir = Path(settings.renders_dir); renders_dir.mkdir(parents=True, exist_ok=True)
        out_mp4 = str(renders_dir / f"short_job{job.id}.mp4")
        make_vertical_short(bg, vo_wav, None, srt_path, out_mp4)
        job.render_path = out_mp4; db.commit()

        # 7) SEO
        seo = build_seo(topic, settings.channel_niche); job.seo = seo; db.commit()

        # 8) Upload (+ optional schedule)
        schedule_iso = job.schedule_at.isoformat() if job.schedule_at else None
        vid = upload_video(out_mp4, seo, schedule_iso=schedule_iso, made_for_kids=False)
        job.yt_video_id = vid; db.commit()

        # 9) Caption track
        upload_captions(vid, srt_path, lang=job.language)

        job.status = "done"; db.commit()
    except Exception as ex:
        job.status = "failed"; job.error = str(ex); db.commit()
    finally:
        db.close()
