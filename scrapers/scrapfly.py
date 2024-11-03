import os
import base64
import urllib.parse
import requests
import time
import base64
from typing import Dict, Any
from .base import BaseScraper

class ScrapflyScraper(BaseScraper):
    """Scrapfly API implementation"""
    
    SCRAPFLY_API_ENDPOINT = "https://api.scrapfly.io/scrape"
    
    def __init__(self, timeout: float = 60):
        self.timeout = timeout
        self.screenshot_flags = []

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
                "default": "raw",
                "help": "Output format for the scraped content"
            },
            "screenshot": {
                "type": "boolean",
                "default": False,
                "help": "Take a screenshot of the rendered page"
            },
            "screenshot_full_page": {
                "type": "boolean",
                "default": False,
                "help": "Capture full page screenshot instead of viewport only"
            },
            "screenshot_load_images": {
                "type": "boolean",
                "default": True,
                "help": "Load images when taking screenshot"
            },
            "screenshot_dark_mode": {
                "type": "boolean",
                "default": False,
                "help": "Enable dark mode for screenshot"
            },
            "screenshot_block_banners": {
                "type": "boolean",
                "default": False,
                "help": "Block banner ads in screenshot"
            },
            "screenshot_high_quality": {
                "type": "boolean",
                "default": False,
                "help": "Take high quality screenshot"
            },
            "screenshot_print_media": {
                "type": "boolean",
                "default": False,
                "help": "Use print media format for screenshot"
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
            "cache_ttl": 60 * 60 * 12,  # 12 hr,
        }
        
        if options.get("country"):
            params["country"] = options["country"]
            
        # Handle screenshot parameters if screenshot is enabled
        if options.get("screenshot"):
            params["screenshots[all]"] = "fullpage" if options.get("screenshot_full_page") else "viewport"
            
            # Only add screenshot flags if screenshot is enabled
            screenshot_flags = []
            if options.get("screenshot_load_images"):
                screenshot_flags.append("load_images")
            if options.get("screenshot_dark_mode"):
                screenshot_flags.append("dark_mode")
            if options.get("screenshot_block_banners"):
                screenshot_flags.append("block_banners")
            if options.get("screenshot_high_quality"):
                screenshot_flags.append("high_quality")
            if options.get("screenshot_print_media"):
                screenshot_flags.append("print_media_format")
            
            if screenshot_flags:
                params["screenshot_flags"] = ",".join(screenshot_flags)

        # Combine all parameters
        url_params_str = urllib.parse.urlencode(params)

        print(
            f"{self.SCRAPFLY_API_ENDPOINT}?{url_params_str}"
        )
        resp = requests.get(
            f"{self.SCRAPFLY_API_ENDPOINT}?{url_params_str}",
            timeout=self.timeout,
        )
        resp.raise_for_status()
        result = resp.json()["result"]
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)

        content = result["content"]
        if options.get("screenshot") and "screenshots" in result:
            screenshot_url = result["screenshots"].get("all", {}).get("url")
            print(f"Found screenshot: {screenshot_url}")
            if screenshot_url:
                # Generate unique filename
                filename = f"screenshot_{hash(url)}_{int(time.time())}.png"
                filepath = os.path.join(screenshots_dir, filename)
                
                # Download the screenshot with API key
                screenshot_resp = requests.get(
                    screenshot_url,
                    params={"key": os.environ["SCRAPFLY_API_KEY"]}
                )
                screenshot_resp.raise_for_status()
                
                # Save to file
                with open(filepath, 'wb') as f:
                    f.write(screenshot_resp.content)
                
                # Embed screenshot image as base64 data URI in content
                with open(filepath, 'rb') as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                content += f"\n\n<img src='data:image/png;base64,{encoded_string}' alt='Screenshot' style='max-width:100%;'>"
        
        return content
