io_tasks = [
    {"type": "api_call", "url": f"https://jsonplaceholder.typicode.com/posts/{i}"} for i in range(1, 11)
]
cpu_tasks = [
    {"type": "factorial", "n": 50000},
    {"type": "matrix_multiply", "size": 200},
    {"type": "hash_compute", "data": "benchmark_data", "iterations": 100000},
    {"type": "prime_check", "n": 999999937},
    {"type": "fibonacci", "n": 35},
]
