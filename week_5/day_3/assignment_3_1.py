"""
Assignment 3.1 — Bug Ovçusu: Buglı Kodu Düzəlt
Week 5, Day 3
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BankAccount:
    interest_rate = 0.05  # BUG 1: class variable — bütün hesablarda eyni dəyişir
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
        self.created = datetime.now()
        logger.info(f"Hesab yaradıldı: {owner}")
    
    def deposit(self, amount):
        logger.debug(f"Deposit cəhdi: {amount}")
        if amount < 0:  # BUG 2: 0 deposit-ə icazə verir, amma 0 mənasızdır
            raise ValueError("Məbləğ müsbət olmalıdır")
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount, "date": datetime.now()})
        return self.balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Məbləğ müsbət olmalıdır")
        if amount > self.balance:
            logger.warning(f"Kifayət qədər vəsait yoxdur: {self.balance} < {amount}")
            return False  # BUG 3: exception yerinə False qaytarır — xəta istifadəçiyə çatmır
        self.balance =- amount  # BUG 4: -= əvəzinə =- (unary minus assignment)
        self.transactions.append({"type": "withdraw", "amount": amount, "date": datetime.now()})
        return self.balance
    
    def transfer(self, other, amount):
        result = self.withdraw(amount)
        if result:  # BUG 5: withdraw 0 qaytarsa bu False olacaq (falsy), amma əməliyyat uğurlu ola bilər
            other.deposit(amount)
            logger.info(f"Transfer: {self.owner} -> {other.owner}: {amount}")
            return True
        return False
    
    def calculate_interest(self, months):
        interest = self.balance * self.interest_rate * months  # BUG 6: illik faizi aylığa çevirmir (/12)
        self.deposit(interest)
        return interest
    
    def get_statement(self, days=30):
        cutoff = datetime.now() - timedelta(days=days)
        # BUG 7: >= əvəzinə > istifadə edib, cutoff günündəki əməliyyatlar çıxmır
        recent = [t for t in self.transactions if t["date"] > cutoff]
        return recent
    
    def __str__(self):
        return f"Account({self.owner}, {self.balance})"  # BUG 8: balance formatlanmır, 2500.0000001 kimi görünə bilər
    
    def __eq__(self, other):
        return self.balance == other.balance  # BUG 9: owner yoxlamır, fərqli şəxslərin eyni balanslı hesabları "bərabər" olacaq


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.daily_limit = 10000
    
    def create_account(self, owner, initial_balance=0):
        # BUG 10: eyni adlı ikinci hesab açmağa cəhd etsə əvvəlkini əzir
        self.accounts[owner] = BankAccount(owner, initial_balance)
        return self.accounts[owner]
    
    def find_account(self, owner):
        return self.accounts[owner]  # BUG 11: KeyError atır, .get() istifadə etmir
    
    def total_deposits(self):
        total = 0
        for acc in self.accounts:  # BUG 12: accounts dict-dir, acc key olacaq (string), .values() lazımdır
            total += acc.balance
        return total
    
    def get_top_accounts(self, n=5):
        sorted_accs = sorted(self.accounts.values(), key=lambda a: a.balance)  # BUG 13: ascending sıralayır, descending lazımdır
        return sorted_accs[:n]
    
    def process_batch_transfers(self, transfers):
        results = []
        for t in transfers:
            sender = self.find_account(t["from"])
            receiver = self.find_account(t["to"])
            # BUG 14: daily limit yoxlanmır
            success = sender.transfer(receiver, t["amount"])
            results.append({"transfer": t, "success": success})
        return results
    
    def generate_report(self):
        report = {
            "bank": self.name,
            "total_accounts": len(self.accounts),
            "total_deposits": self.total_deposits(),
            "generated_at": datetime.now()  # BUG 15: datetime JSON-a serialize olmur, str lazımdır
        }
        return report
