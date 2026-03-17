"""
Assignment 1.1 — Asinxron Veb Scraper
Week 4, Day 1
"""

urls_to_scrape = [
    {"name": "JSONPlaceholder Posts", "url": "https://jsonplaceholder.typicode.com/posts", "type": "api"},
    {"name": "JSONPlaceholder Users", "url": "https://jsonplaceholder.typicode.com/users", "type": "api"},
    {"name": "JSONPlaceholder Comments", "url": "https://jsonplaceholder.typicode.com/comments?postId=1", "type": "api"},
    {"name": "HTTPBin Get", "url": "https://httpbin.org/get", "type": "api"},
    {"name": "HTTPBin IP", "url": "https://httpbin.org/ip", "type": "api"},
    {"name": "HTTPBin Headers", "url": "https://httpbin.org/headers", "type": "api"},
    {"name": "HTTPBin Delay 1s", "url": "https://httpbin.org/delay/1", "type": "slow"},
    {"name": "HTTPBin Delay 2s", "url": "https://httpbin.org/delay/2", "type": "slow"},
    {"name": "HTTPBin UUID", "url": "https://httpbin.org/uuid", "type": "api"},
    {"name": "GitHub API Zen", "url": "https://api.github.com/zen", "type": "api"},
]
