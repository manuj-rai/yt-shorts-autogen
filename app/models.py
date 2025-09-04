from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    status = Column(String(32), default="queued", index=True)
    locale = Column(String(8), default="US")
    language = Column(String(8), default="en")
    topic_hint = Column(String(256), nullable=True)
    schedule_at = Column(DateTime, nullable=True)
    approve_to_publish = Column(Boolean, default=False)

    script = Column(Text, nullable=True)
    seo = Column(JSON, nullable=True)
    render_path = Column(String(512), nullable=True)
    captions_path = Column(String(512), nullable=True)
    yt_video_id = Column(String(64), nullable=True)
    error = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assets = relationship("Asset", back_populates="job", cascade="all,delete")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    kind = Column(String(32))      # video, image, music, vo
    source = Column(String(64))    # pexels, azuretts, local
    path = Column(String(512))
    license_meta = Column(JSON, nullable=True)
    duration = Column(Float, nullable=True)
    job = relationship("Job", back_populates="assets")
