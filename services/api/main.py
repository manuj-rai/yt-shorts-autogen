from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import redis, json

from app.config import settings
from app.db import init_db, SessionLocal
from app.models import Job

app = FastAPI(title="YT Shorts Autogen API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

init_db()
r = redis.from_url(settings.redis_url)

class JobCreate(BaseModel):
    locale: str | None = None
    language: str | None = None
    topicHint: str | None = None
    scheduleAt: datetime | None = None
    approveToPublish: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"ok": True, "env": settings.env}

@app.post("/jobs")
def create_job(body: JobCreate, db=Depends(get_db)):
    job = Job(
        locale=body.locale or settings.default_locale,
        language=body.language or settings.default_lang,
        topic_hint=body.topicHint,
        schedule_at=body.scheduleAt,
        approve_to_publish=body.approveToPublish,
        status="queued"
    )
    db.add(job); db.commit(); db.refresh(job)
    r.lpush("jobs", json.dumps({"job_id": job.id}))
    return {"id": job.id, "status": job.status}

@app.get("/jobs/{job_id}")
def get_job(job_id: int, db=Depends(get_db)):
    job = db.get(Job, job_id)
    if not job: raise HTTPException(404, "Not found")
    return {
        "id": job.id, "status": job.status, "topicHint": job.topic_hint,
        "seo": job.seo, "renderPath": job.render_path, "captionsPath": job.captions_path,
        "ytVideoId": job.yt_video_id, "error": job.error
    }

@app.post("/jobs/{job_id}/approve")
def approve(job_id: int, db=Depends(get_db)):
    job = db.get(Job, job_id)
    if not job: raise HTTPException(404, "Not found")
    job.approve_to_publish = True
    db.commit()
    return {"ok": True}
