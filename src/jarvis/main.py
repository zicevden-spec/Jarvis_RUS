"""Каркас конвейера Jarvis_RUS. Пока заглушки, реализуем по этапам из README."""


def wait_for_wake_word() -> None:
    input("[слово-активатор] пока заглушка, нажмите Enter...")


def listen() -> str:
    return input("[микрофон] пока вводите фразу вручную: ")


def think(text: str) -> str:
    return f"Вы сказали: {text}"


def speak(text: str) -> None:
    print(f"[Джарвис] {text}")


def main() -> None:
    while True:
        wait_for_wake_word()
        text = listen()
        if text.strip().lower() in {"выход", "стоп"}:
            break
        speak(think(text))


if __name__ == "__main__":
    main()
