"""
Assignment 2.3 — Asinxron Event-Driven Sistem
Week 4, Day 2
"""

events_stream = [
    {"type": "order.created", "data": {"id": "ORD-501", "customer": "Əli", "total": 250.00, "items": ["Laptop çantası", "USB hub"]}},
    {"type": "payment.received", "data": {"order_id": "ORD-501", "amount": 250.00, "method": "card"}},
    {"type": "order.shipped", "data": {"id": "ORD-501", "carrier": "AzPost", "tracking": "AZ123456"}},
    {"type": "user.registered", "data": {"id": "U-100", "name": "Nigar", "email": "nigar@mail.az"}},
    {"type": "order.created", "data": {"id": "ORD-502", "customer": "Tural", "total": 15000.00, "items": ["Gaming PC"]}},
    {"type": "payment.failed", "data": {"order_id": "ORD-502", "reason": "insufficient_funds"}},
    {"type": "order.cancelled", "data": {"id": "ORD-502", "reason": "payment_failed"}},
    {"type": "order.created", "data": {"id": "ORD-503", "customer": "Leyla", "total": 89.99, "items": ["Qulaqlıq"]}},
    {"type": "payment.received", "data": {"order_id": "ORD-503", "amount": 89.99, "method": "cash"}},
    {"type": "user.login", "data": {"id": "U-100", "ip": "10.0.0.55", "attempts": 7}},
    {"type": "order.delivered", "data": {"id": "ORD-501", "signed_by": "Əli Həsənov"}},
    {"type": "order.returned", "data": {"id": "ORD-503", "reason": "defective", "refund": 89.99}},
]
