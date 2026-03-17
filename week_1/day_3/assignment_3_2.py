def process_data(data):
    """Datanı emal edib nəticə qaytarır — bilərəkdən yavaş işləyir."""
    import time
    time.sleep(0.5)
    return [x ** 2 for x in data if x % 2 == 0]
