"""
Assignment 2.2 — Şablon Mühərriki (Template Engine)
Week 3, Day 2
"""

templates = {
    "report": """
    <h1>{{title}}</h1>
    <p>Tarix: {{date}}</p>
    {% if show_summary %}
    <div class="summary">
        <p>Ümumi: {{total}} element</p>
        <p>Status: {{status}}</p>
    </div>
    {% endif %}
    <ul>
    {% for item in items %}
        <li>{{item.name}} - {{item.value}} AZN</li>
    {% endfor %}
    </ul>
    """,
    "email": """
    Hörmətli {{name}},
    {{message}}
    {% if has_attachment %}
    Əlavə: {{attachment_name}}
    {% endif %}
    Hörmətlə, {{sender}}
    """,
}

contexts = {
    "report": {
        "title": "Aylıq Hesabat",
        "date": "2026-03-17",
        "show_summary": True,
        "total": 15,
        "status": "Tamamlandı",
        "items": [
            {"name": "Server xərcləri", "value": 450},
            {"name": "Lisenziya", "value": 200},
            {"name": "Əmək haqqı", "value": 8500},
        ]
    },
    "email": {
        "name": "Əli Həsənov",
        "message": "Layihə uğurla tamamlandı.",
        "has_attachment": True,
        "attachment_name": "report.pdf",
        "sender": "Admin"
    }
}
