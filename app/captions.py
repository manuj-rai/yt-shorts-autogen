from pathlib import Path

def write_srt(segments, srt_path: str):
    """segments = [{'start':0.0,'end':1.2,'text':'line'}, ...]"""
    def ts(t):
        h=int(t//3600); m=int((t%3600)//60); s=int(t%60); ms=int((t*1000)%1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(f"{i}\n{ts(seg['start'])} --> {ts(seg['end'])}\n{seg['text']}\n")
    Path(srt_path).write_text("\n".join(lines), encoding="utf-8")
    return srt_path

def naive_line_split(script: str, wpm=180):
    """Very basic line-based segmentation. For production, align TTS or ASR."""
    lines = [ln.strip() for ln in script.splitlines() if ln.strip()]
    segs, t = [], 0.0
    for ln in lines:
        words = max(1, len(ln.split()))
        dur = max(1.0, words / 3.0)  # ~3 w/s
        segs.append({"start": t, "end": t + dur, "text": ln})
        t += dur + 0.15
    return segs, t
