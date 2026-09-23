"""Этап 5: диалог через локальную модель Ollama."""
import re

import ollama

MODEL_NAME = "qwen3.5:2b"

SYSTEM_PROMPT = (
    "Ты голосовой ассистент по имени Джарвис. "
    "Отвечай по-русски, коротко и по делу, 1-3 предложения, "
    "без рассуждений вслух, потому что ответ будет озвучен."
)


def ask(text: str) -> str:
    response = ollama.chat(model=MODEL_NAME, messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ])
    content = response["message"]["content"]
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
    if not content:
        print("  (модель вернула пустой ответ, сырой текст:", repr(response["message"]["content"]), ")")
        content = "Извините, не могу сейчас сформулировать ответ. Повторите вопрос иначе."
    return content
