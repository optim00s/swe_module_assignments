books = [
    {"isbn": "978-1-001", "title": "Python Proqramlaşdırma", "author": "A. Məmmədov", "genre": "Texnologiya", "year": 2023, "copies": 5, "available": 5},
    {"isbn": "978-1-002", "title": "Data Elmi Əsasları", "author": "L. Əliyeva", "genre": "Texnologiya", "year": 2024, "copies": 3, "available": 3},
    {"isbn": "978-1-003", "title": "Süni İntellekt", "author": "R. Hüseynov", "genre": "Texnologiya", "year": 2022, "copies": 4, "available": 2},
    {"isbn": "978-1-004", "title": "Azərbaycan Tarixi", "author": "T. Qasımov", "genre": "Tarix", "year": 2020, "copies": 6, "available": 6},
    {"isbn": "978-1-005", "title": "Modern Fizika", "author": "N. Babayev", "genre": "Elm", "year": 2021, "copies": 2, "available": 0},
    {"isbn": "978-1-006", "title": "Psixologiya Giriş", "author": "S. Vəliyeva", "genre": "Psixologiya", "year": 2023, "copies": 4, "available": 4},
    {"isbn": "978-1-007", "title": "Riyaziyyat Təhlili", "author": "K. Nəsirov", "genre": "Elm", "year": 2019, "copies": 3, "available": 1},
    {"isbn": "978-1-008", "title": "İqtisadiyyata Giriş", "author": "G. Əsgərova", "genre": "İqtisadiyyat", "year": 2022, "copies": 5, "available": 5},
    {"isbn": "978-1-009", "title": "Web Development", "author": "A. Məmmədov", "genre": "Texnologiya", "year": 2024, "copies": 2, "available": 2},
    {"isbn": "978-1-010", "title": "Dünya Ədəbiyyatı", "author": "F. Rəhimova", "genre": "Ədəbiyyat", "year": 2021, "copies": 7, "available": 5},
]

members = [
    {"id": "MEM-001", "name": "Əli Həsənov", "membership": "Premium", "borrowed": [], "history": []},
    {"id": "MEM-002", "name": "Leyla Məmmədova", "membership": "Standard", "borrowed": [], "history": []},
    {"id": "MEM-003", "name": "Tural Əliyev", "membership": "Premium", "borrowed": [], "history": []},
    {"id": "MEM-004", "name": "Nigar Hüseynova", "membership": "Standard", "borrowed": [], "history": []},
    {"id": "MEM-005", "name": "Rəşad Quliyev", "membership": "Premium", "borrowed": [], "history": []},
]

membership_rules = {
    "Premium": {"max_books": 5, "loan_days": 30, "can_reserve": True},
    "Standard": {"max_books": 3, "loan_days": 14, "can_reserve": False},
}

borrow_log = [
    ("MEM-001", "978-1-003", "2026-03-01"),
    ("MEM-001", "978-1-005", "2026-03-01"),
    ("MEM-003", "978-1-003", "2026-03-02"),
    ("MEM-002", "978-1-007", "2026-03-03"),
    ("MEM-004", "978-1-010", "2026-03-04"),
    ("MEM-005", "978-1-005", "2026-03-04"),
    ("MEM-004", "978-1-010", "2026-03-05"),
    ("MEM-001", "978-1-007", "2026-03-06"),
]
