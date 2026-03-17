"""
Assignment 2.3 — Integration Test Layihəsi
Week 5, Day 2
"""

# ecommerce.py
class Product:
    def __init__(self, sku, name, price, stock):
        self.sku, self.name, self.price, self.stock = sku, name, price, stock
    
    def is_available(self, qty=1): return self.stock >= qty
    def reduce_stock(self, qty):
        if qty > self.stock: raise ValueError("Stok kifayət etmir")
        self.stock -= qty
    def restock(self, qty): self.stock += qty

class Cart:
    def __init__(self):
        self.items = {}  # {sku: {"product": Product, "qty": int}}
    
    def add_item(self, product, qty=1):
        if not product.is_available(qty): raise ValueError(f"{product.name} stokda yoxdur")
        if product.sku in self.items: self.items[product.sku]["qty"] += qty
        else: self.items[product.sku] = {"product": product, "qty": qty}
    
    def remove_item(self, sku):
        if sku not in self.items: raise KeyError("Məhsul səbətdə yoxdur")
        del self.items[sku]
    
    def get_total(self):
        return sum(item["product"].price * item["qty"] for item in self.items.values())
    
    def clear(self): self.items.clear()

class Order:
    _counter = 0
    def __init__(self, cart, customer_name):
        Order._counter += 1
        self.order_id = f"ORD-{Order._counter:04d}"
        self.items = dict(cart.items)
        self.total = cart.get_total()
        self.customer = customer_name
        self.status = "pending"
    
    def process_payment(self, amount):
        if amount < self.total: raise ValueError("Ödəniş kifayət etmir")
        self.status = "paid"
        for item_data in self.items.values():
            item_data["product"].reduce_stock(item_data["qty"])
        self.change = amount - self.total
        return self.change
    
    def cancel(self):
        if self.status == "paid":
            for item_data in self.items.values():
                item_data["product"].restock(item_data["qty"])
        self.status = "cancelled"
    
    def ship(self):
        if self.status != "paid": raise ValueError("Ödənilməmiş sifariş göndərilə bilməz")
        self.status = "shipped"
