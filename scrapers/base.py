from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseScraper(ABC):
    """Base class for web scrapers"""
    
    @abstractmethod
    def fetch(self, url: str, **options) -> str:
        """
        Fetch content from URL with given options
        
        Args:
            url: Target URL to scrape
            **options: Provider-specific scraping options
            
        Returns:
            str: Scraped content (markdown or HTML)
        """
        pass

    @abstractmethod
    def get_options_schema(self) -> Dict[str, Any]:
        """
        Get schema of supported options for this scraper
        
        Returns:
            Dict describing the available options and their metadata
        """
        pass
