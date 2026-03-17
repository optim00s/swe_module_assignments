import json, os, sys, time, random
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.file = "tasks.json"
        self.load()
    
    def load(self):
        try:
            f = open(self.file, "r")
            self.tasks = json.load(f)
            f.close()
        except:
            self.tasks = []
    
    def save(self):
        f = open(self.file, "w")
        json.dump(self.tasks, f)
        f.close()
    
    def add(self, title, desc="", pri=1, assign=None, due=None):
        id = len(self.tasks) + 1  # BUG: silindikdən sonra ID təkrarlana bilər
        task = {"id": id, "title": title, "description": desc, "priority": pri,
                "assignee": assign, "due_date": due, "status": "todo",
                "created": str(datetime.now()), "subtasks": [], "tags": []}
        self.tasks.append(task)
        self.save()
        return task
    
    def delete(self, id):
        for i in range(len(self.tasks)):
            if self.tasks[i]["id"] == id:
                del self.tasks[i]
                self.save()
                return True
        return False
    
    def update_status(self, id, status):
        # status validasiyası yoxdur
        for t in self.tasks:
            if t["id"] == id:
                t["status"] = status
                self.save()
                return True
        return False
    
    def search(self, keyword):
        results = []
        for t in self.tasks:
            if keyword.lower() in t["title"].lower() or keyword.lower() in t["description"].lower():
                results.append(t)
        return results
    
    def get_overdue(self):
        overdue = []
        for t in self.tasks:
            if t["due_date"] and t["status"] != "done":
                # String müqayisəsi — düzgün deyil
                if t["due_date"] < str(datetime.now()):
                    overdue.append(t)
        return overdue
    
    def get_stats(self):
        stats = {}
        stats["total"] = len(self.tasks)
        stats["todo"] = len([t for t in self.tasks if t["status"] == "todo"])
        stats["in_progress"] = len([t for t in self.tasks if t["status"] == "in_progress"])
        stats["done"] = len([t for t in self.tasks if t["status"] == "done"])
        stats["overdue"] = len(self.get_overdue())
        if len(self.tasks) > 0:
            stats["completion_rate"] = stats["done"] / stats["total"] * 100
        else:
            stats["completion_rate"] = 0
        return stats
    
    def assign_random(self, team):
        # Yük balanslaması olmadan təsadüfi təyin edir
        for t in self.tasks:
            if t["assignee"] is None:
                t["assignee"] = random.choice(team)
        self.save()
    
    def export_csv(self, filename):
        f = open(filename, "w")
        f.write("id,title,status,priority,assignee,due_date\n")
        for t in self.tasks:
            line = f"{t['id']},{t['title']},{t['status']},{t['priority']},{t['assignee']},{t['due_date']}\n"
            f.write(line)
        f.close()
    
    def bulk_update(self, ids, field, value):
        count = 0
        for t in self.tasks:
            if t["id"] in ids:
                t[field] = value  # Təhlükəsiz deyil — istənilən sahəni dəyişə bilər
                count += 1
        self.save()
        return count
