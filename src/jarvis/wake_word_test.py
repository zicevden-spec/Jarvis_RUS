"""Этап 3: слово-активатор «Джарвис» + запись команды (Vosk, отладочная версия)."""
import json
import queue

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel

SAMPLE_RATE = 16000
MODEL_PATH = "models/vosk-model-small-ru-0.22"
# Варианты того, как маленькая модель может услышать слово "Джарвис"
WAKE_VARIANTS = ["джарвис", "жарвис", "дарвис", "гарвис", "жар вис"]

audio_q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_q.put(bytes(indata))


def listen_for_wake_word(model) -> None:
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    print("Жду слово «Джарвис»... (показываю всё, что слышу, для отладки)")
    while True:
        data = audio_q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if text:
                print("  услышано:", text)
            if any(w in text for w in WAKE_VARIANTS):
                return


def listen_for_command(model) -> str:
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    print("Слушаю команду...")
    while not audio_q.empty():
        audio_q.get_nowait()
    while True:
        data = audio_q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if text:
                return text


def main():
    SetLogLevel(-1)
    model = Model(MODEL_PATH)
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000,
                           dtype="int16", channels=1, callback=callback):
        while True:
            listen_for_wake_word(model)
            print("Слушаю!")
            command = listen_for_command(model)
            print("Команда:", command)
            if command.strip().lower() in {"выход", "стоп"}:
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")
