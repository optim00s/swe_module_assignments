"""
Assignment 3.1 — Log Faylı Analiz Sistemi
Week 1, Day 3
"""

raw_logs = [
    "2026-03-10 08:15:22 INFO  UserService Login successful user=eli.hasanov ip=192.168.1.10",
    "2026-03-10 08:15:45 ERROR DatabaseService Connection timeout db=main retry=3",
    "2026-03-10 08:16:01 WARN  AuthService Failed login attempt user=unknown ip=10.0.0.55",
    "2026-03-10 08:16:30 INFO  UserService Profile updated user=leyla.mammadova ip=192.168.1.22",
    "2026-03-10 08:17:05 ERROR PaymentService Transaction failed order=ORD-445 amount=150.00",
    "2026-03-10 08:17:20 INFO  UserService Login successful user=tural.aliyev ip=192.168.1.35",
    "2026-03-10 08:18:00 WARN  AuthService Suspicious activity ip=10.0.0.55 attempts=5",
    "2026-03-10 08:18:45 INFO  OrderService Order created order=ORD-446 user=eli.hasanov total=89.99",
    "2026-03-10 08:19:10 ERROR DatabaseService Query timeout db=analytics duration=30s",
    "2026-03-10 08:19:55 INFO  UserService Login successful user=nigar.huseynova ip=192.168.1.41",
    "2026-03-10 08:20:15 WARN  PaymentService Low balance user=tural.aliyev balance=12.50",
    "2026-03-10 08:20:40 ERROR AuthService Brute force detected ip=10.0.0.55 blocked=true",
    "2026-03-10 08:21:00 INFO  OrderService Order shipped order=ORD-440 carrier=AzPost",
    "2026-03-10 08:21:30 INFO  UserService Logout user=eli.hasanov session_duration=65min",
    "2026-03-10 08:22:00 ERROR PaymentService Refund failed order=ORD-430 reason=expired",
    "2026-03-10 08:22:45 INFO  UserService Login successful user=sabina.ismayilova ip=192.168.1.50",
    "2026-03-10 08:23:10 WARN  DatabaseService High load db=main connections=95/100",
    "2026-03-10 08:23:55 INFO  OrderService Order created order=ORD-447 user=nigar.huseynova total=245.00",
    "2026-03-10 08:24:20 ERROR DatabaseService Deadlock detected db=main table=orders",
    "2026-03-10 08:25:00 INFO  UserService Password changed user=leyla.mammadova ip=192.168.1.22",
]
