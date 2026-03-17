"""
Assignment 3.3 — Şəkil Emal Pipeline (CPU-intensive)
Week 3, Day 3
"""

def generate_image(width, height):
    return [[random.randint(0, 255) for _ in range(width)] for _ in range(height)]

images = [generate_image(200, 200) for _ in range(10)]
