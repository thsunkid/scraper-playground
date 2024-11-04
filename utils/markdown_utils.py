import re
from urllib.parse import urljoin
import requests


def get_redirected_url(url: str) -> str:
    """Follow redirects and get the final URL"""
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except Exception:
        return url


def resolve_relative_images(content: str, base_url: str) -> str:
    """Resolve relative image paths in markdown content to absolute URLs"""

    def replace_image_url(match):
        alt_text = match.group(1)
        image_url = match.group(2)
        if not image_url.startswith(("http://", "https://", "data:")):
            image_url = urljoin(base_url, image_url)
        return f"![{alt_text}]({image_url})"

    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.sub(pattern, replace_image_url, content)
