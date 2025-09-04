import time, json, redis
from app.config import settings
from app.pipeline import run_pipeline

r = redis.from_url(settings.redis_url)

def main():
    while True:
        try:
            item = r.brpop("jobs", timeout=5)
            if not item:
                continue
            _, payload = item
            data = json.loads(payload.decode("utf-8"))
            run_pipeline(int(data["job_id"]))
        except Exception as ex:
            print("Worker error:", ex)
        time.sleep(1)

if __name__ == "__main__":
    main()
