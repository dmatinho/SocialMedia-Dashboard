#!/usr/bin/env python3
"""Fetch YouTube channel stats and update the DATA.youtube block in index.html.

Runs in GitHub Actions. Requires env var YT_API_KEY (repo secret).
Uses only the Python standard library.
"""
import json, os, re, sys, urllib.request
from datetime import date

CHANNEL_ID = "UCm4tG9_rSJYTgmHv9ThXPTg"
API = "https://www.googleapis.com/youtube/v3"
KEY = os.environ.get("YT_API_KEY", "").strip()
MAX_VIDEOS = 10

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    if "error" in data:
        sys.exit(f"YouTube API error: {data['error'].get('message')}")
    return data

def main():
    if not KEY:
        sys.exit("Missing YT_API_KEY environment variable (set it as a repo secret).")

    # Channel stats
    ch = get(f"{API}/channels?part=snippet,statistics&id={CHANNEL_ID}&key={KEY}")
    if not ch.get("items"):
        sys.exit("Channel not found — check CHANNEL_ID.")
    subs = int(ch["items"][0]["statistics"].get("subscriberCount", 0))

    # Recent videos
    search = get(f"{API}/search?part=snippet&channelId={CHANNEL_ID}&maxResults={MAX_VIDEOS}&order=date&type=video&key={KEY}")
    ids = ",".join(i["id"]["videoId"] for i in search.get("items", []))
    if not ids:
        sys.exit("No videos returned.")
    vids = get(f"{API}/videos?part=snippet,statistics&id={ids}&key={KEY}")

    videos = []
    for v in vids.get("items", []):
        videos.append({
            "title": v["snippet"]["title"],
            "date": v["snippet"]["publishedAt"][:10],
            "views": int(v["statistics"].get("viewCount", 0)),
            "likes": int(v["statistics"].get("likeCount", 0)),
            "comments": int(v["statistics"].get("commentCount", 0)),
            "url": f"https://youtube.com/watch?v={v['id']}",
        })
    videos.sort(key=lambda x: x["date"], reverse=True)

    block = (
        "youtube: {\n"
        f"    views: {sum(v['views'] for v in videos)},\n"
        f"    subscribers: {subs},\n"
        f"    likes: {sum(v['likes'] for v in videos)},\n"
        f"    comments: {sum(v['comments'] for v in videos)},\n"
        f"    videos: {json.dumps(videos, ensure_ascii=False)},\n"
        "  },"
    )

    with open("index.html", encoding="utf-8") as f:
        html = f.read()

    new_html = re.sub(r"youtube: \{.*?\n  \},", lambda m: block, html, count=1, flags=re.DOTALL)
    if new_html == html:
        print("No changes to YouTube data.")
        return
    new_html = re.sub(r"updatedAt: '[\d-]+'", f"updatedAt: '{date.today().isoformat()}'", new_html, count=1)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Updated: {subs} subscribers, {len(videos)} videos.")

if __name__ == "__main__":
    main()
