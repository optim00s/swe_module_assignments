servers_config = [
    {"id": "SRV-001", "name": "Web Server", "cpu_cores": 8, "ram_gb": 32, "storage_gb": 500, "role": "web"},
    {"id": "SRV-002", "name": "Database Server", "cpu_cores": 16, "ram_gb": 64, "storage_gb": 2000, "role": "database"},
    {"id": "SRV-003", "name": "Cache Server", "cpu_cores": 4, "ram_gb": 128, "storage_gb": 100, "role": "cache"},
    {"id": "SRV-004", "name": "Worker Node 1", "cpu_cores": 8, "ram_gb": 16, "storage_gb": 250, "role": "worker"},
    {"id": "SRV-005", "name": "Worker Node 2", "cpu_cores": 8, "ram_gb": 16, "storage_gb": 250, "role": "worker"},
]

simulated_metrics = [
    ("SRV-001", {"cpu": 75, "ram": 60, "disk": 45, "network_mbps": 850, "requests_per_sec": 1200}),
    ("SRV-002", {"cpu": 90, "ram": 85, "disk": 70, "network_mbps": 200, "queries_per_sec": 5000}),
    ("SRV-003", {"cpu": 30, "ram": 95, "disk": 15, "network_mbps": 500, "hit_rate": 0.92}),
    ("SRV-004", {"cpu": 95, "ram": 70, "disk": 40, "network_mbps": 100, "jobs_completed": 450}),
    ("SRV-005", {"cpu": 45, "ram": 35, "disk": 38, "network_mbps": 80, "jobs_completed": 380}),
]
