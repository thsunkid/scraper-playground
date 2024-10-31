import os
import base64
import urllib.parse
import requests
from typing import Dict, Any
from .base import BaseScraper

class ScrapflyScraper(BaseScraper):
    """Scrapfly API implementation"""
    
    SCRAPFLY_API_ENDPOINT = "https://api.scrapfly.io/scrape"
    
    def __init__(self, timeout: float = 60):
        self.timeout = timeout

    def get_options_schema(self) -> Dict[str, Any]:
        return {
            "render_js": {
                "type": "boolean",
                "default": False,
                "help": "Enable browser rendering. Scrape the target with a browser and render the page"
            },
            "proxy_pool": {
                "type": "select",
                "options": ["datacenter", "residential"],
                "default": "datacenter",
                "help": "Select proxy pool type - datacenter (25x cheaper) or residential"
            },
            "country": {
                "type": "string",
                "default": "",
                "help": "Proxy country location (ISO 3166 alpha-2). Empty for random location"
            },
            "format": {
                "type": "select",
                "options": ["raw", "markdown", "clean_html", "json"],
                "default": "markdown",
                "help": "Output format for the scraped content"
            }
        }

    def fetch(self, url: str, **options) -> str:
        params = {
            "key": os.environ["SCRAPFLY_API_KEY"],
            "url": url,
            "render_js": "true" if options.get("render_js", False) else "false",
            "proxy_pool": "public_residential_pool" 
                if options.get("proxy_pool") == "residential"
                else "public_datacenter_pool",
            "timeout": self.timeout * 1000,
            "format": options.get("format", "markdown"),
            "retry": "false",
            "cache": "true",
            "cache_ttl": 60 * 60 * 12,  # 12 hr
        }
        
        if options.get("country"):
            params["country"] = options["country"]
            
        url_params_str = urllib.parse.urlencode(params)
        
        resp = requests.get(
            f"{self.SCRAPFLY_API_ENDPOINT}?{url_params_str}",
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["result"]["content"]
