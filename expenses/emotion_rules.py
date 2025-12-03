from datetime import time
from .models import Expense


FAST_FOOD_KEYWORDS = [
    'mcdonald', 'kfc', 'burger', 'pizza', 'subway',
    'донер', 'шаурма', 'фастфуд', 'кава', 'coffee', 'starbucks'
]

ONLINE_SHOPPING_KEYWORDS = [
    'aliexpress', 'amazon', 'ebay', 'rozetka', 'ozon',
    'steam', 'playstation', 'xbox', 'g2a'
]

ENTERTAINMENT_KEYWORDS = [
    'cinema', 'movie', 'netflix', 'spotify', 'concert',
    'pub', 'bar', 'club'
]


def _contains_any(text: str, keywords: list[str]) -> bool:
    text = text.lower()
    return any(k in text for k in keywords)


def analyze_emotional_expense(description: str, category: str, dt) -> tuple[bool, str]:
    desc = description.lower()

    if _contains_any(desc, FAST_FOOD_KEYWORDS):
        return True, 'fast_food'

    if _contains_any(desc, ONLINE_SHOPPING_KEYWORDS):
        return True, 'online_shopping'

    if _contains_any(desc, ENTERTAINMENT_KEYWORDS) or category == 'entertainment':
        if dt.time() >= time(20, 0) or dt.time() <= time(6, 0):
            return True, 'late_night'
        return True, 'entertainment'

    if category in ['food', 'shopping'] and (dt.time() >= time(21, 0) or dt.time() <= time(5, 0)):
        return True, 'late_night'

    return False, 'none'
