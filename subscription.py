# subscription.py
import json
import os
from datetime import date, datetime, timedelta
import flet as ft

# В Flet данные сохраняются в специальной папке
BASE_DIR = os.getenv("FLET_APP_STORAGE_DATA", ".")
LICENSE_FILE = os.path.join(BASE_DIR, "license.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

TIERS = {
    "free": {"name": "Бесплатный", "icon": "🆓", "price": 0, "limit": 30},
    "plus": {"name": "Плюс", "icon": "⭐", "price": 199, "limit": 500},
    "premium": {"name": "Премиум", "icon": "👑", "price": 499, "limit": None},
}

def _load(path, default):
    if not os.path.exists(path): return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            base = dict(default)
            base.update(data)
            return base
    except:
        return default

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class AppState:
    def __init__(self):
        self.progress = _load(PROGRESS_FILE, {"seen": [], "known": [], "favorites": [], "streak": 0})
        self.license = _load(LICENSE_FILE, {
            "tier": "free", "expires": (date.today() + timedelta(days=7)).isoformat(), 
            "trial": True, "daily_seen": {}
        })
        self._check_expiration()

    def _check_expiration(self):
        if self.license.get("tier") != "free":
            try:
                exp = date.fromisoformat(self.license["expires"])
                if exp < date.today():
                    self.license["tier"] = "free"
                    self.save_license()
            except: pass

    def save_progress(self):
        self.progress["seen"] = list(set(self.progress["seen"]))
        self.progress["known"] = list(set(self.progress["known"]))
        self.progress["favorites"] = list(set(self.progress["favorites"]))
        _save(PROGRESS_FILE, self.progress)

    def save_license(self):
        _save(LICENSE_FILE, self.license)

    def can_see_more(self):
        limit = TIERS[self.license["tier"]]["limit"]
        if limit is None: return True
        today = date.today().isoformat()
        seen_today = self.license.get("daily_seen", {}).get(today, 0)
        return seen_today < limit

    def add_seen(self):
        today = date.today().isoformat()
        self.license.setdefault("daily_seen", {})
        self.license["daily_seen"][today] = self.license["daily_seen"].get(today, 0) + 1
        self.save_license()

# Глобальный объект состояния
state = AppState()
