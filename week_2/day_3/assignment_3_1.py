"""
Assignment 3.1 — Multi-API Dashboard: NASA + GitHub + OpenRouter
Week 2, Day 3
"""

    payload = {
        "model": "google/gemma-3-4b-it:free",  # pulsuz model
        "messages": [
            {"role": "user", "content": f"Bu günün NASA APOD təsviri: {apod_description}. Bu hadisənin astronomik əhəmiyyətini 2-3 cümlə ilə izah et."}
        ]
    }
