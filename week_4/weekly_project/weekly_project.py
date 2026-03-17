"""
Assignment weekly — Weekly Project
Week 4, Day 3
"""

sources_config = {
    "hacker_news": {
        "type": "api",
        "base_url": "https://hacker-news.firebaseio.com/v0",
        "endpoints": {
            "top": "/topstories.json",
            "item": "/item/{id}.json"
        },
        "rate_limit": {"requests": 10, "per_seconds": 60},
        "refresh_interval": 300
    },
    "github_trending": {
        "type": "scraper",
        "url": "https://github.com/trending",
        "selectors": {
            "repo": "article.Box-row",
            "name": "h2 a",
            "description": "p.col-9",
            "language": "span[itemprop='programmingLanguage']",
            "stars": "a.Link--muted"
        },
        "refresh_interval": 600
    },
    "jsonplaceholder": {
        "type": "api",
        "base_url": "https://jsonplaceholder.typicode.com",
        "endpoints": {
            "posts": "/posts",
            "users": "/users"
        },
        "rate_limit": {"requests": 30, "per_seconds": 60},
        "refresh_interval": 120
    },
    "nasa_apod": {
        "type": "api",
        "base_url": "https://api.nasa.gov",
        "endpoints": {
            "apod": "/planetary/apod"
        },
        "params": {"api_key": "DEMO_KEY"},
        "rate_limit": {"requests": 30, "per_seconds": 3600},
        "refresh_interval": 86400
    }
}
