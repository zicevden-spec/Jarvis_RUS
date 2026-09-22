"""Этап 4: быстрые команды по правилам, без обращения к большой модели."""
import datetime


def try_handle(text: str) -> str | None:
    """Возвращает ответ, если команда распознана как быстрая, иначе None."""
    text = text.lower().strip()

    if any(w in text for w in ["сколько времени", "который час"]):
        now = datetime.datetime.now().strftime("%H:%M")
        return f"Сейчас {now}"

    if any(w in text for w in ["какое сегодня число", "какая сегодня дата"]):
        today = datetime.date.today().strftime("%d.%m.%Y")
        return f"Сегодня {today}"

    return None
