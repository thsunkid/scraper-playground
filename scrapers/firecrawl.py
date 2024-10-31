import os
import requests
from typing import Dict, Any
from .base import BaseScraper

class FirecrawlScraper(BaseScraper):
    """Firecrawl API implementation"""
    
    FIRECRAWL_API_ENDPOINT = "https://api.firecrawl.io/scrape"
    
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    def get_options_schema(self) -> Dict[str, Any]:
        return {
            "js_enabled": {
                "type": "boolean",
                "default": True,
                "help": "Enable JavaScript rendering"
            },
            "proxy_type": {
                "type": "select", 
                "options": ["residential", "datacenter"],
                "default": "datacenter",
                "help": "Type of proxy to use for scraping"
            },
            "region": {
                "type": "string",
                "default": "us",
                "help": "Geographic region for proxy (e.g. us, eu, asia)"
            }
        }

    def fetch(self, url: str, **options) -> str:
        params = {
            "api_key": os.environ["FIRECRAWL_API_KEY"],
            "url": url,
            "js_enabled": options.get("js_enabled", True),
            "proxy_type": options.get("proxy_type", "datacenter"),
            "region": options.get("region", "us"),
            "timeout": int(self.timeout * 1000)
        }
        
        resp = requests.post(
            self.FIRECRAWL_API_ENDPOINT,
            json=params,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()["content"]
