"""
Assignment 2.2 — Asinxron Rate Limiter və Retry Sistemi
Week 4, Day 2
"""

limiter = RateLimiter(tokens=5, refill_rate=2)
retry = RetryPolicy(max_retries=3, backoff_factor=2)
breaker = CircuitBreaker(failure_threshold=3, recovery_time=30)

async def safe_api_call(url):
    async with limiter:
        return await breaker.call(retry.execute, fetch, url)

test_urls = (
    [f"https://httpbin.org/get?id={i}" for i in range(15)] +         # uğurlu
    [f"https://httpbin.org/status/500" for _ in range(5)] +           # server xətası
    [f"https://httpbin.org/delay/10" for _ in range(3)] +             # timeout
    [f"https://httpbin.org/status/429" for _ in range(4)] +           # rate limited
    ["https://invalid-domain-xyz.com/api" for _ in range(3)]          # DNS xətası
)
