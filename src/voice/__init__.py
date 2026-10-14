import os
import tempfile

from flask import Flask, request, jsonify
from faster_whisper import WhisperModel


# ============================================================
# SETTINGS
# ============================================================

HOST = "127.0.0.1"
PORT = 5001

MODEL_NAME = "base.en"

UPLOAD_FOLDER = os.path.join(
    tempfile.gettempdir(),
    "ai_knowledge_voice"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# LOAD WHISPER MODEL
# ============================================================

print("=" * 60)
print("WHISPER VOICE SERVICE")
print("=" * 60)

print("Loading Whisper model...")

model = WhisperModel(
    MODEL_NAME,
    device="cpu",
    compute_type="int8"
)

print("✅ Whisper model loaded successfully.")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "Whisper Speech-to-Text"
    })


# ============================================================
# TRANSCRIBE AUDIO
# ============================================================

@app.route("/transcribe", methods=["POST"])
def transcribe():

    uploaded_file = request.files.get("audio")

    if uploaded_file is None:
        return jsonify({
            "success": False,
            "error": "No audio file was uploaded."
        }), 400

    if not uploaded_file.filename:
        return jsonify({
            "success": False,
            "error": "Audio filename is missing."
        }), 400

    # Create a safe temporary filename
    extension = os.path.splitext(
        uploaded_file.filename
    )[1]

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension,
        dir=UPLOAD_FOLDER
    )

    temp_path = temp_file.name
    temp_file.close()

    try:

        # ----------------------------------------------------
        # SAVE AUDIO
        # ----------------------------------------------------

        uploaded_file.save(
            temp_path
        )

        print(
            f"🎤 Audio received: {temp_path}"
        )

        # ----------------------------------------------------
        # TRANSCRIBE
        # ----------------------------------------------------

        segments, info = model.transcribe(
            temp_path,
            language="en",
            beam_size=5,
            vad_filter=False,
            condition_on_previous_text=False,
            temperature=0.0
        )

        transcript_parts = []

        for segment in segments:

            text = segment.text.strip()

            if text:
                transcript_parts.append(text)

        transcript = " ".join(
            transcript_parts
        ).strip()

        print(
            "📝 Transcript:",
            transcript
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({
            "success": True,
            "transcript": transcript,
            "language": getattr(
                info,
                "language",
                "en"
            )
        })

    except Exception as error:

        print(
            "❌ Transcription error:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

    finally:

        # ----------------------------------------------------
        # DELETE TEMPORARY FILE
        # ----------------------------------------------------

        try:

            if os.path.exists(temp_path):
                os.remove(temp_path)

        except Exception:
            pass


# ============================================================
# START SERVICE
# ============================================================

if __name__ == "__main__":

    print()
    print(
        f"Voice service running at "
        f"http://{HOST}:{PORT}"
    )

    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )