test_urls = (
    [f"https://httpbin.org/get?id={i}" for i in range(15)] +         # uğurlu
    [f"https://httpbin.org/status/500" for _ in range(5)] +           # server xətası
    [f"https://httpbin.org/delay/10" for _ in range(3)] +             # timeout
    [f"https://httpbin.org/status/429" for _ in range(4)] +           # rate limited
    ["https://invalid-domain-xyz.com/api" for _ in range(3)]          # DNS xətası
)
