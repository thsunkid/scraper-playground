import os
import requests
from typing import Dict, Any
from .base import BaseScraper


class FirecrawlScraper(BaseScraper):
    """Firecrawl API implementation"""

    FIRECRAWL_API_ENDPOINT = "https://api.firecrawl.dev/v1/scrape"

    def __init__(self, timeout: float = 180.0):
        self.timeout = timeout

    def get_options_schema(self) -> Dict[str, Any]:
        return {
            "skipTlsVerification": {
                "type": "boolean",
                "default": False,
                "help": "Skip TLS certificate verification when making requests",
            },
            "formats": {
                "type": "select",
                "options": [
                    "markdown",
                    "html",
                    "rawHtml",
                    "links",
                    "screenshot",
                    "extract",
                    "screenshot@fullPage",
                ],
                "default": "markdown",
                "help": "Formats to include in the output",
            },
            "onlyMainContent": {
                "type": "boolean",
                "default": True,
                "help": "Only return the main content excluding headers, navs, footers, etc",
            },
            "waitFor": {
                "type": "number",
                "default": 0,
                "help": "Delay in milliseconds before fetching content",
            },
            "timeout": {
                "type": "number",
                "default": 30000,
                "help": "Timeout in milliseconds for the request",
            },
            "country": {
                "type": "string",
                "default": "US",
                "help": "ISO 3166-1 alpha-2 country code",
            },
            "languages": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["en-US"],
                "help": "Preferred languages for the request",
            },
        }

    def fetch(self, url: str, **options) -> str:
        payload = {
            "url": url,
            "skipTlsVerification": options.get("skipTlsVerification", False),
            "formats": [options.get("formats", "markdown")],
            "onlyMainContent": options.get("onlyMainContent", True),
            "waitFor": int(options.get("waitFor", 0)),
            "timeout": int(options.get("timeout", 30000)),
            "location": {
                "country": options.get("country", "US"),
                "languages": (
                    options.get("languages", ["en-US"])
                    if isinstance(options.get("languages"), list)
                    else ["en-US"]
                ),
            },
        }

        headers = {
            "Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}",
            "Content-Type": "application/json",
        }

        resp = requests.post(
            self.FIRECRAWL_API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )
        resp.raise_for_status()

        data = resp.json()["data"]

        # Return content based on selected format
        format = options.get("formats", "markdown")
        if format == "markdown":
            return data["markdown"]
        elif format == "html":
            return data["html"] or ""
        elif format == "rawHtml":
            return data["rawHtml"] or ""
        elif format == "links":
            return "\n".join(data["links"])
        else:
            return data["markdown"]  # Default to markdown
