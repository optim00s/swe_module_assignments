"""
Assignment 3.1 — Paralel Fayl Emal Sistemi
Week 3, Day 3
"""

import random, string
def generate_test_files(directory, count=20):
    """Test faylları yarat: hər birində təsadüfi mətn, ədədlər, email ünvanları"""
    domains = ["gmail.com", "yahoo.com", "academy.az", "mail.ru", "outlook.com"]
    words = ["python", "data", "server", "network", "module", "thread", "process",
             "function", "class", "object", "variable", "loop", "condition", "error"]
    for i in range(count):
        lines = []
        for _ in range(random.randint(100, 500)):
            line_type = random.choice(["text", "number", "email", "mixed"])
            if line_type == "text":
                lines.append(" ".join(random.choices(words, k=random.randint(5, 15))))
            elif line_type == "number":
                lines.append(" ".join(str(random.randint(1, 10000)) for _ in range(random.randint(3, 10))))
            elif line_type == "email":
                name = "".join(random.choices(string.ascii_lowercase, k=8))
                lines.append(f"Contact: {name}@{random.choice(domains)} | ID: {random.randint(1000,9999)}")
            else:
                lines.append(f"{random.choice(words)}: {random.randint(1,100)} - {''.join(random.choices(string.ascii_letters, k=20))}")
        filepath = os.path.join(directory, f"data_{i:03d}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
