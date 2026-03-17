    payload = {
        "model": "google/gemma-3-4b-it:free",  # pulsuz model
        "messages": [
            {"role": "user", "content": f"Bu günün NASA APOD təsviri: {apod_description}. Bu hadisənin astronomik əhəmiyyətini 2-3 cümlə ilə izah et."}
        ]
    }
