const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition = null;


// ============================================================
// SPEECH RECOGNITION
// ============================================================

if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = function () {

        const status =
            document.getElementById("speechStatus");

        if (status) {
            status.innerText =
                "🎤 Listening... Please speak.";
        }
    };


    recognition.onresult = function (event) {

        const transcript =
            event.results[0][0].transcript;

        const questionInput =
            document.getElementById("questionInput");

        if (questionInput) {

            questionInput.value =
                transcript;
        }

        const status =
            document.getElementById("speechStatus");

        if (status) {

            status.innerText =
                "✅ Speech captured. Click Ask Question.";
        }
    };


    recognition.onerror = function (event) {

        const status =
            document.getElementById("speechStatus");

        if (status) {

            status.innerText =
                "❌ Speech error: " + event.error;
        }
    };


    recognition.onend = function () {

        const status =
            document.getElementById("speechStatus");

        if (
            status &&
            status.innerText ===
            "🎤 Listening... Please speak."
        ) {

            status.innerText =
                "Finished listening.";
        }
    };

}


// ============================================================
// START LISTENING
// ============================================================

function startListening() {

    if (!recognition) {

        const status =
            document.getElementById("speechStatus");

        status.innerText =
            "❌ Speech recognition is not supported.";

        return;
    }

    try {

        recognition.start();

    } catch (error) {

        console.log(error);

    }
}


// ============================================================
// TEXT TO SPEECH
// ============================================================

function speakAnswer() {

    const answerElement =
        document.querySelector(".answer");

    if (!answerElement) {

        alert(
            "No answer is available yet."
        );

        return;
    }

    const text =
        answerElement.innerText.trim();

    if (!text) {

        alert(
            "The answer is empty."
        );

        return;
    }

    const speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.cancel();

    window.speechSynthesis.speak(
        speech
    );
}