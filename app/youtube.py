from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from tenacity import retry, stop_after_attempt, wait_exponential
from .config import settings

def _creds():
    return Credentials.from_authorized_user_file(settings.youtube_token_json, scopes=[
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
    ])

def _client():
    return build("youtube", "v3", credentials=_creds())

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30))
def upload_video(path: str, seo: dict, schedule_iso: str | None, made_for_kids: bool = False) -> str:
    yt = _client()
    body = {
        "snippet": {
            "title": seo["title"],
            "description": seo["description"] + "\n\n" + " ".join(seo.get("hashtags", [])),
            "tags": seo.get("tags", []),
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "private" if schedule_iso else "public",
            **({"publishAt": schedule_iso} if schedule_iso else {}),
            "selfDeclaredMadeForKids": bool(made_for_kids)
        }
    }
    media = MediaFileUpload(path, chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = req.next_chunk()
    return response["id"]

def upload_captions(video_id: str, srt_path: str, lang="en"):
    yt = _client()
    body = {"snippet": {"videoId": video_id, "language": lang, "name": "English", "isDraft": False}}
    media = MediaFileUpload(srt_path, mimetype="application/octet-stream", resumable=False)
    yt.captions().insert(part="snippet", body=body, media_body=media).execute()
