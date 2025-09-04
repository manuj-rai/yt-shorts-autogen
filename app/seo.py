from slugify import slugify

def build_seo(topic: str, niche_csv: str):
    primary = topic.strip().title()[:90]
    title = f"{primary} (Do This Today) #shorts"
    desc = (
        f"{primary}\n"
        f"Quick {niche_csv.split(',')[0]} tips you can apply right now.\n"
        f"#shorts #{slugify(primary, separator='')}"
    )
    tags = [t.strip() for t in niche_csv.split(",") if t.strip()][:8]
    tags += [topic, "shorts", "reels", "tiktok"]
    hashtags = ["#shorts"] + [f"#{slugify(t, separator='')}" for t in tags[:5]]
    return {"title": title[:100], "description": desc[:5000], "tags": tags[:50], "hashtags": hashtags[:8]}
