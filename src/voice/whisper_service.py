from flask import Flask, request, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel
import os
import tempfile

app = Flask(__name__)

# Allow the main Flask website to communicate with this service
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://127.0.0.1:5000",
                "http://localhost:5000"
            ]
        }
    }
)

# ---------------------------------------------------------
# WHISPER MODEL
# ---------------------------------------------------------
# base.en is a good balance between speed and accuracy for English.
print("Loading Whisper model...")

model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded successfully.")


# ---------------------------------------------------------
# HOME / SERVICE STATUS
# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Voice service is running",
        "service": "Whisper Speech-to-Text",
        "status": "ok"
    })


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "Whisper Speech-to-Text"
    })


# ---------------------------------------------------------
# TRANSCRIBE AUDIO
# ---------------------------------------------------------
@app.route("/transcribe", methods=["POST"])
def transcribe():

    temp_path = None

    try:
        # -------------------------------------------------
        # Accept common field names from frontend
        # -------------------------------------------------
        audio_file = (
            request.files.get("audio")
            or request.files.get("file")
            or request.files.get("audio_file")
        )

        if audio_file is None:
            return jsonify({
                "status": "error",
                "message": "No audio file received."
            }), 400

        # -------------------------------------------------
        # Determine file extension
        # -------------------------------------------------
        original_name = audio_file.filename or "recording.webm"

        _, extension = os.path.splitext(original_name)

        if not extension:
            extension = ".webm"

        # -------------------------------------------------
        # Save uploaded audio temporarily
        # -------------------------------------------------
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            audio_file.save(temp_file.name)
            temp_path = temp_file.name

        # -------------------------------------------------
        # Transcribe using Whisper
        # -------------------------------------------------
        segments, info = model.transcribe(
            temp_path,
            beam_size=5,
            vad_filter=True
        )

        # -------------------------------------------------
        # Combine all segments
        # -------------------------------------------------
        text_parts = []

        for segment in segments:
            text_parts.append(segment.text.strip())

        transcript = " ".join(text_parts).strip()

        # -------------------------------------------------
        # Empty transcription check
        # -------------------------------------------------
        if not transcript:
            return jsonify({
                "status": "error",
                "message": "No speech was detected.",
                "text": ""
            }), 200

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------
        return jsonify({
            "status": "ok",
            "text": transcript,
            "language": getattr(info, "language", "en"),
            "language_probability": getattr(
                info,
                "language_probability",
                None
            )
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e),
            "text": ""
        }), 500

    finally:

        # -------------------------------------------------
        # Delete temporary file
        # -------------------------------------------------
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------
if __name__ == "__main__":

    print("Starting Whisper Speech-to-Text service...")
    print("Voice service URL: http://127.0.0.1:5001/")
    print("Health URL: http://127.0.0.1:5001/health")
    print("Transcription URL: http://127.0.0.1:5001/transcribe")

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )