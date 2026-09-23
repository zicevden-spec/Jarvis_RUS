"""Этап 4-5: полный цикл — слово-активатор, распознавание, быстрая команда или Ollama, голос."""
import json
import queue

import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel

from quick_commands import try_handle
from brain import ask
from tts_test import speak

SAMPLE_RATE = 16000
MODEL_PATH = "models/vosk-model-small-ru-0.22"
WAKE_VARIANTS = ["джарвис", "жарвис", "дарвис", "гарвис", "жар вис"]

audio_q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_q.put(bytes(indata))


def listen_for_wake_word(model) -> None:
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    while True:
        data = audio_q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if any(w in text for w in WAKE_VARIANTS):
                return


def listen_for_command(model) -> str:
    rec = KaldiRecognizer(model, SAMPLE_RATE)
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
    print("Джарвис готов. Скажите «Джарвис», затем команду.")
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000,
                           dtype="int16", channels=1, callback=callback):
        while True:
            listen_for_wake_word(model)
            print("Слушаю!")
            command = listen_for_command(model)
            print("Команда:", command)
            if command.strip().lower() in {"выход", "стоп"}:
                break
            answer = try_handle(command)
            if answer is None:
                print("Думаю...")
                answer = ask(command)
            print("Ответ:", answer)
            speak(answer)
            while not audio_q.empty():
                audio_q.get_nowait()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")
