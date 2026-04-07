import re

def clean_price(price_text):
    """Очищает цену от лишних пробелов и переносов"""
    if not price_text:
        return "Цена не указана"
    # Убираем множественные пробелы и переносы
    price_text = re.sub(r'\s+', ' ', price_text)
    # Убираем лишние пробелы перед ₽
    price_text = re.sub(r'\s+₽', ' ₽', price_text)
    return price_text.strip()

def truncate_description(text, limit=200):
    """Обрезает описание до limit символов"""
    if not text:
        return ""
    if len(text) > limit:
        return text[:limit] + "..."
    return text
