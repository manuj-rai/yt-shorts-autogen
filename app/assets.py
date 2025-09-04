import json, time, httpx
from pathlib import Path
from .config import settings
from .logging_conf import logger

PEXELS_VIDEO_SEARCH = "https://api.pexels.com/videos/search"

def _record_license(entry: dict):
    path = Path(settings.license_ledger)
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    arr.append(entry)
    path.write_text(json.dumps(arr, indent=2), encoding="utf-8")

def fetch_pexels_broll(query: str, out_dir: str, count: int = 1) -> list[str]:
    """Fetch vertical stock mp4 clips from Pexels (license-safe)."""
    if not settings.pexels_api_key:
        logger.warning("PEXELS_API_KEY missing; cannot fetch b-roll.")
        return []
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    headers = {"Authorization": settings.pexels_api_key}
    params = {"query": query, "orientation": "portrait", "per_page": 5}
    try:
        r = httpx.get(PEXELS_VIDEO_SEARCH, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        videos = r.json().get("videos", [])[:count]
        paths = []
        for vid in videos:
            vf = sorted(vid.get("video_files", []), key=lambda f: f.get("height", 0), reverse=True)[0]
            url = vf["link"]; dest = Path(out_dir) / f"pexels_{vid['id']}.mp4"
            with httpx.stream("GET", url, timeout=60) as resp:
                resp.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in resp.iter_bytes():
                        f.write(chunk)
            _record_license({
                "provider":"pexels","assetId":vid["id"],"url":vid["url"],
                "license":"Pexels License","downloadedAt":int(time.time()),"path":str(dest)
            })
            paths.append(str(dest))
        return paths
    except Exception as ex:
        logger.error(f"Pexels fetch error: {ex}")
        return []
