"""Этап 2: озвучиваем текст русским голосом (Piper)."""
import subprocess
import sys
import wave

from piper import PiperVoice

VOICE_PATH = "voices/ru_RU-ruslan-medium.onnx"


def speak(text: str, out_path: str = "out.wav") -> None:
    voice = PiperVoice.load(VOICE_PATH)
    with wave.open(out_path, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    # Проигрываем файл штатными средствами Windows
    subprocess.run([
        "powershell", "-c",
        f"(New-Object Media.SoundPlayer '{out_path}').PlaySync()"
    ])


if __name__ == "__main__":
    phrase = " ".join(sys.argv[1:]) or "Здравствуйте, я Джарвис. Проверка голоса."
    print(f"Озвучиваю: {phrase}")
    speak(phrase)
