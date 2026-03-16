from django import template
import re

register = template.Library()


@register.filter
def youtube_embed(url):
    """
    YouTube video linkini embed linkine çevirir.
    Örnek: https://www.youtube.com/watch?v=abc123 -> https://www.youtube.com/embed/abc123
    """
    if not url:
        return ""

    match = re.search(r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"

    match = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"

    if "youtube.com/embed" in url:
        return url

    return ""

