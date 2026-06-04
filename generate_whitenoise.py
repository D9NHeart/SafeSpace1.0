"""
Gera um arquivo de ruído branco (white_noise.wav) na pasta do projeto.
Rode uma vez: python generate_whitenoise.py
assim não precisa de arquivo externo, espera essa porra gerar aí e não mexe...
"""

import wave
import struct
import random
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "white_noise.wav")

DURATION = 660  
SAMPLE_RATE = 22050
AMPLITUDE = 1500

print("Gerando ruído branco... aguarde...")

with wave.open(OUTPUT, "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SAMPLE_RATE)
    for _ in range(DURATION * SAMPLE_RATE):
        sample = random.randint(-AMPLITUDE, AMPLITUDE)
        f.writeframes(struct.pack("<h", sample))

print(f"✓ Arquivo gerado em: {OUTPUT}")