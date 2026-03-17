def test_generate_password_length():
    pwd = generate_password(length=16)
    assert len(pwd) == 16

def test_generate_password_has_uppercase():
    pwd = generate_password(length=20, uppercase=True)
    assert any(c.isupper() for c in pwd)
# ... daha çox test
