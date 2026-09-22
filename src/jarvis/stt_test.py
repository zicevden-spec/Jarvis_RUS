"""Этап 1: слушаем микрофон и печатаем распознанную русскую речь (Vosk)."""
import json
import queue

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel

SAMPLE_RATE = 16000
audio_q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_q.put(bytes(indata))


def main():
    SetLogLevel(-1)
    print("Загружаю модель (при первом запуске скачается, около 50 МБ)...")
    model = Model("models/vosk-model-small-ru-0.22")
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    print("Говорите. Для выхода нажмите Ctrl+C.")
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000,
                           dtype="int16", channels=1, callback=callback):
        while True:
            data = audio_q.get()
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "")
                if text:
                    print("Вы сказали:", text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")
