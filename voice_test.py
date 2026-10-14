import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


# ============================================================
# SETTINGS
# ============================================================

AUDIO_FILE = "voice_test.wav"

DEVICE_INDEX = 1

SAMPLE_RATE = 16000

DURATION = 8


# ============================================================
# RECORD AUDIO
# ============================================================

print("\n" + "=" * 60)
print("MICROPHONE TEST")
print("=" * 60)

print("Input device:", DEVICE_INDEX)
print("Sample rate:", SAMPLE_RATE)
print("Recording duration:", DURATION, "seconds")

print("\n🎤 Recording for 8 seconds...")
print("Speak clearly and continuously:")
print("👉 What is cloud computing?")

try:

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE_INDEX
    )

    sd.wait()

except Exception as error:

    print("\n❌ Recording failed:")
    print(error)
    raise SystemExit


# ============================================================
# AUDIO ANALYSIS
# ============================================================

audio = audio.flatten()

peak_before = float(
    np.max(
        np.abs(audio)
    )
)

rms_before = float(
    np.sqrt(
        np.mean(
            np.square(audio)
        )
    )
)

print("\n✅ Recording completed.")

print("Original peak:", peak_before)
print("Original RMS:", rms_before)


# ============================================================
# AUTOMATIC GAIN
# ============================================================

if peak_before <= 0.0001:

    print(
        "\n❌ No meaningful microphone signal detected."
    )

    raise SystemExit


# Target RMS for Whisper
TARGET_RMS = 0.03

if rms_before > 0:

    gain = TARGET_RMS / rms_before

else:

    gain = 1.0


# Limit amplification
gain = min(gain, 15.0)

print("Applied gain:", round(gain, 2))


audio = audio * gain


# ============================================================
# LIMIT AUDIO
# ============================================================

audio = np.clip(
    audio,
    -1.0,
    1.0
)


# ============================================================
# SAVE WAV
# ============================================================

audio_int16 = (
    audio * 32767
).astype(np.int16)


write(
    AUDIO_FILE,
    SAMPLE_RATE,
    audio_int16
)


print(
    "\n✅ Audio saved:"
)

print(
    os.path.abspath(
        AUDIO_FILE
    )
)


# ============================================================
# LOAD WHISPER
# ============================================================

print("\n" + "=" * 60)
print("WHISPER MODEL")
print("=" * 60)

print("Loading Whisper model...")

try:

    model = WhisperModel(
        "base.en",
        device="cpu",
        compute_type="int8"
    )

except Exception as error:

    print("\n❌ Whisper loading failed:")
    print(error)
    raise SystemExit


print("✅ Whisper model loaded.")


# ============================================================
# TRANSCRIBE
# ============================================================

print("\n" + "=" * 60)
print("TRANSCRIPTION")
print("=" * 60)

print("Transcribing...")

try:

    segments, info = model.transcribe(
        AUDIO_FILE,
        language="en",
        beam_size=5,

        # IMPORTANT:
        # Disable VAD because your microphone signal is quiet.
        vad_filter=False,

        condition_on_previous_text=False,

        temperature=0.0,

        # Help Whisper understand the expected topic.
        initial_prompt=(
            "What is cloud computing? "
            "This is a technical question."
        )
    )

    transcript_parts = []

    for segment in segments:

        text = segment.text.strip()

        if text:

            print(
                f"[{segment.start:.2f}s - "
                f"{segment.end:.2f}s] {text}"
            )

            transcript_parts.append(text)


    transcript = " ".join(
        transcript_parts
    ).strip()


except Exception as error:

    print("\n❌ Transcription failed:")
    print(error)
    raise SystemExit


# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 60)
print("TRANSCRIPTION RESULT")
print("=" * 60)

if transcript:

    print("✅ Speech detected!")

    print("\nYou said:")

    print(transcript)

else:

    print(
        "❌ No speech was detected."
    )

print("=" * 60)