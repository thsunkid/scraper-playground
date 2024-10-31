# Web Scraping Service

A flexible web scraping service that supports multiple scraping providers including Firecrawl and Scrapfly.

![Architecture Diagram](assets/images/architecture.png)

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables for your preferred scraping provider:

For Firecrawl:
```bash
export FIRECRAWL_API_KEY=your_api_key
```

For Scrapfly:
```bash
export SCRAPFLY_API_KEY=your_api_key
```

3. Run the application:
```bash
python app.py
```

## Features

- Multiple scraping provider support
- Abstract base class for easy provider integration
- Simple REST API interface

## License

MIT
