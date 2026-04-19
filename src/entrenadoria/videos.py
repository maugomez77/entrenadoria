"""YouTube video resolution for exercise form demos.

Uses YouTube Data API v3 when YOUTUBE_API_KEY is set. Caches results
in the store to avoid repeated API calls for the same exercise name.

Free tier = 10k quota units/day; a search costs 100 units → ~100
unique exercises per day. Cache makes this plenty.
"""

from __future__ import annotations

import os
import urllib.parse
from typing import Literal

import httpx

from . import store

API_URL = "https://www.googleapis.com/youtube/v3/search"


def _cache_key(exercise: str, language: str) -> str:
    return f"{language}::{exercise.strip().lower()}"


def _load_cache() -> dict:
    state = store.load()
    return state.get("_video_cache", {})


def _save_cache(cache: dict) -> None:
    state = store.load()
    state["_video_cache"] = cache
    store.save(state)


def fallback_search_url(exercise: str, language: Literal["es", "en"] = "es") -> str:
    qualifier = "técnica correcta" if language == "es" else "proper form"
    q = urllib.parse.quote(f"{exercise} {qualifier}")
    return f"https://www.youtube.com/results?search_query={q}"


def resolve_video(
    exercise: str,
    language: Literal["es", "en"] = "es",
) -> dict:
    """Return {video_id, title, channel, url, embed_url} or a fallback.

    If no YOUTUBE_API_KEY, returns only the search URL (no embed)."""
    key = _cache_key(exercise, language)
    cache = _load_cache()
    if key in cache:
        return cache[key]

    api_key = os.environ.get("YOUTUBE_API_KEY")
    search_url = fallback_search_url(exercise, language)

    if not api_key:
        result = {"video_id": None, "title": exercise, "channel": "",
                  "url": search_url, "embed_url": None,
                  "search_url": search_url, "cached": False}
        return result

    qualifier = "técnica correcta ejercicio" if language == "es" else "proper form exercise"
    query = f"{exercise} {qualifier}"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": "1",
        "relevanceLanguage": language,
        "safeSearch": "strict",
        "videoEmbeddable": "true",
        "key": api_key,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(API_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
        items = data.get("items", [])
        if not items:
            result = {"video_id": None, "title": exercise, "channel": "",
                      "url": search_url, "embed_url": None,
                      "search_url": search_url, "cached": False}
        else:
            video_id = items[0]["id"]["videoId"]
            snippet = items[0]["snippet"]
            result = {
                "video_id": video_id,
                "title": snippet.get("title", exercise),
                "channel": snippet.get("channelTitle", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "embed_url": f"https://www.youtube.com/embed/{video_id}",
                "search_url": search_url,
                "cached": False,
            }
    except Exception:
        result = {"video_id": None, "title": exercise, "channel": "",
                  "url": search_url, "embed_url": None,
                  "search_url": search_url, "cached": False,
                  "error": "youtube_api_failed"}

    # cache success only
    if result.get("video_id"):
        cache[key] = {**result, "cached": True}
        _save_cache(cache)
    return result
