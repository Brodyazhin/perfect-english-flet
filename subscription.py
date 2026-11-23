# subscription.py
import json
import os
import random
from datetime import date, datetime, timedelta
import flet as ft

BASE_DIR = os.getenv("FLET_APP_STORAGE_DATA", ".")
LICENSE_FILE = os.path.join(BASE_DIR, "license.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

TIERS = {
    "free": {"name": "Бесплатный", "icon": "🆓", "price": 0, "limit": 30},
    "plus": {"name": "Плюс", "icon": "⭐", "price": 199, "limit": 500},
    "premium": {"name": "Премиум", "icon": "👑", "price": 499, "limit": None},
}


def _load(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            base = dict(default)
            base.update(data)
            return base
    except Exception:
        return default


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class AppState:
    def __init__(self):
        self.progress = _load(PROGRESS_FILE, {
            "seen": [], "known": [], "favorites": [],
            "streak": 0, "last_active": None, "theme_mode": "light",
            "quiz_history": [], "transactions": [],
            "last_section": None, "last_subsection": None,
        })
        self.license = _load(LICENSE_FILE, {
            "tier": "free",
            "expires": (date.today() + timedelta(days=7)).isoformat(),
            "trial": True,
            "daily_seen": {},
        })
        self._check_expiration()

    def _check_expiration(self):
        if self.license.get("tier") != "free":
            try:
                exp = date.fromisoformat(self.license["expires"])
                if exp < date.today():
                    self.license["tier"] = "free"
                    self.save_license()
            except Exception:
                pass

    def save_progress(self):
        self.progress["seen"] = list(set(self.progress["seen"]))
        self.progress["known"] = list(set(self.progress["known"]))
        self.progress["favorites"] = list(set(self.progress["favorites"]))
        self.progress.setdefault("quiz_history", [])
        self.progress.setdefault("transactions", [])
        _save(PROGRESS_FILE, self.progress)

    def save_license(self):
        _save(LICENSE_FILE, self.license)

    def record_activity(self):
        """Вызывается при открытии приложения. Обновляет streak."""
        today = date.today()
        last = self.progress.get("last_active")
        if last:
            try:
                last_date = date.fromisoformat(last)
            except Exception:
                last_date = None
        else:
            last_date = None

        if last_date == today:
            return
        if last_date and (today - last_date).days == 1:
            self.progress["streak"] = self.progress.get("streak", 0) + 1
        else:
            self.progress["streak"] = 1
        self.progress["last_active"] = today.isoformat()
        self.save_progress()

    def set_theme(self, mode: str):
        self.progress["theme_mode"] = mode
        self.save_progress()

    def set_last_opened(self, section: str, subsection: str):
        self.progress["last_section"] = section
        self.progress["last_subsection"] = subsection
        self.save_progress()

    def can_see_more(self):
        limit = TIERS[self.license["tier"]]["limit"]
        if limit is None:
            return True
        today = date.today().isoformat()
        seen_today = self.license.get("daily_seen", {}).get(today, 0)
        return seen_today < limit

    def add_seen(self):
        today = date.today().isoformat()
        self.license.setdefault("daily_seen", {})
        self.license["daily_seen"][today] = self.license["daily_seen"].get(today, 0) + 1
        self.save_license()

    def add_transaction(self, amount, tier, method, status="success", promo=None):
        txn = {
            "date": datetime.now().isoformat(timespec="seconds"),
            "amount": amount,
            "tier": tier,
            "method": method,
            "status": status,
            "promo": promo,
            "txn_id": f"TX{random.randint(100000, 999999)}",
        }
        self.progress.setdefault("transactions", [])
        self.progress["transactions"].append(txn)
        self.progress["transactions"] = self.progress["transactions"][-50:]
        self.save_progress()
        return txn


state = AppState()
