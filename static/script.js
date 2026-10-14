let mediaRecorder = null;
let audioChunks = [];

async function startListening() {
    const status = document.getElementById("speechStatus");
    const questionInput = document.getElementById("questionInput");

    try {
        status.innerText = "🎤 Listening... Please speak.";

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        audioChunks = [];

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = function (event) {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async function () {
            stream.getTracks().forEach(track => track.stop());

            status.innerText = "⏳ Transcribing...";

            const audioBlob = new Blob(audioChunks, {
                type: "audio/webm"
            });

            const formData = new FormData();
            formData.append("audio", audioBlob, "recording.webm");

            try {
                const response = await fetch(
                    "http://127.0.0.1:5001/transcribe",
                    {
                        method: "POST",
                        body: formData
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "Whisper service returned " + response.status
                    );
                }

                const data = await response.json();

                if (data.text) {
                    questionInput.value = data.text;
                    status.innerText =
                        "✅ Speech converted to text. Click Ask Question.";
                } else {
                    status.innerText =
                        "❌ No speech was detected.";
                }

            } catch (error) {
                console.error(error);

                status.innerText =
                    "❌ Whisper service connection failed: " +
                    error.message;
            }
        };

        mediaRecorder.start();

        // Record for 5 seconds
        setTimeout(() => {
            if (
                mediaRecorder &&
                mediaRecorder.state === "recording"
            ) {
                mediaRecorder.stop();
            }
        }, 5000);

    } catch (error) {
        console.error(error);

        status.innerText =
            "❌ Microphone error: " + error.message;
    }
}


function speakAnswer() {
    const answerElement =
        document.querySelector(".answer");

    if (!answerElement) {
        alert("No answer is available yet.");
        return;
    }

    const text = answerElement.innerText.trim();

    if (!text) {
        alert("The answer is empty.");
        return;
    }

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);
}