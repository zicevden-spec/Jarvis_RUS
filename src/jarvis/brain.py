"""Этап 5-6: диалог через локальную модель Ollama, с опциональным контекстом из веб-поиска."""
import ollama

MODEL_NAME = "qwen3.5:2b"

SYSTEM_PROMPT = (
    "Ты голосовой ассистент по имени Джарвис. "
    "Отвечай по-русски, коротко и по делу, 1-3 предложения. Если не уверен в фактах (даты, люди, сюжеты фильмов и сериалов), честно скажи, что не уверен, вместо того чтобы выдумывать."
)

SYSTEM_PROMPT_WITH_SEARCH = SYSTEM_PROMPT + (
    " Тебе дали результаты свежего веб-поиска. "
    "Используй их, чтобы ответить на вопрос кратко своими словами, не перечисляй источники."
)


def _clean(response) -> str:
    content = (response.message.content or "").strip()
    if not content:
        thinking = (response.message.thinking or "")
        print("  (пустой content, thinking):", repr(thinking[:300]))
        content = "Извините, не могу сейчас сформулировать ответ. Повторите вопрос иначе."
    return content


def ask(text: str) -> str:
    response = ollama.chat(model=MODEL_NAME, think=False, messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ])
    return _clean(response)


def ask_with_search(text: str, search_results: str) -> str:
    user_message = f"Вопрос: {text}\n\nРезультаты поиска:\n{search_results}"
    response = ollama.chat(model=MODEL_NAME, think=False, messages=[
        {"role": "system", "content": SYSTEM_PROMPT_WITH_SEARCH},
        {"role": "user", "content": user_message},
    ])
    return _clean(response)
