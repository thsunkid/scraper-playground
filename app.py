import os
from flask import Flask, render_template, request, jsonify
from scrapers.scrapfly import ScrapflyScraper
from scrapers.firecrawl import FirecrawlScraper
import markdown

app = Flask(__name__)

# Initialize scrapers
SCRAPERS = {
    "scrapfly": ScrapflyScraper(),
    "firecrawl": FirecrawlScraper()
}

@app.route('/')
def index():
    """Render the main playground page"""
    # Get options schema for each scraper
    scraper_options = {
        name: scraper.get_options_schema()
        for name, scraper in SCRAPERS.items()
    }
    return render_template('index.html', 
                         scrapers=SCRAPERS.keys(),
                         scraper_options=scraper_options)

@app.route('/scrape', methods=['POST'])
def scrape():
    """Handle scraping requests"""
    try:
        data = request.json
        url = data.get('url')
        provider = data.get('provider')
        options = data.get('options', {})
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        if provider not in SCRAPERS:
            return jsonify({"error": "Invalid scraper provider"}), 400
            
        # Get content from selected scraper
        scraper = SCRAPERS[provider]
        content = scraper.fetch(url, **options)
        
        # Convert HTML to markdown if needed
        if content.strip().startswith('<'):
            from markdownify import markdownify
            content = markdownify(content)
            
        # Convert markdown to HTML for preview
        html_content = markdown.markdown(content)
        
        return jsonify({
            "raw": content,
            "html": html_content
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
