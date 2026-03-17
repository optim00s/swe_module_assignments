"""
Assignment 3.3 — API Müqayisə və Monitoring Aləti
Week 2, Day 3
"""

apis_to_test = {
    "NASA_APOD": {
        "url": "https://api.nasa.gov/planetary/apod",
        "params": {"api_key": "DEMO_KEY"},
        "method": "GET"
    },
    "GitHub_Users": {
        "url": "https://api.github.com/users/torvalds",
        "params": {},
        "method": "GET"
    },
    "GitHub_Repos": {
        "url": "https://api.github.com/users/python/repos",
        "params": {"sort": "stars", "per_page": 5},
        "method": "GET"
    },
    "OpenRouter_Models": {
        "url": "https://openrouter.ai/api/v1/models",
        "params": {},
        "method": "GET"
    },
    "JSONPlaceholder": {
        "url": "https://jsonplaceholder.typicode.com/posts",
        "params": {},
        "method": "GET"
    },
    "HTTPBin_Get": {
        "url": "https://httpbin.org/get",
        "params": {"test": "monitoring"},
        "method": "GET"
    }
}
