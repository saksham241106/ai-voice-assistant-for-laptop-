const micButton =
    document.getElementById("micButton");

const auraAvatar =
    document.getElementById("auraAvatar");

const status =
    document.getElementById("status");

const chatInput =
    document.getElementById("chatInput");

const sendButton =
    document.getElementById("sendButton");

const chatMessages =
    document.getElementById("chatMessages");


let recognition = null;


/* =========================
   VOICE RECOGNITION
========================= */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    recognition =
        new SpeechRecognition();

    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = false;


    recognition.onstart = function () {

        micButton.classList.add("listening");

        auraAvatar.classList.add("listening");

        status.innerHTML =
            "🔵 Listening...";

    };


    recognition.onresult =
        function (event) {

            const text =
                event.results[0][0]
                .transcript;

            addUserMessage(text);

            sendCommand(text);

        };


    recognition.onerror =
        function () {

            micButton.classList.remove(
                "listening"
            );

            auraAvatar.classList.remove(
                "listening"
            );

            status.innerHTML =
                "❌ Could not understand";

        };


    recognition.onend =
        function () {

            micButton.classList.remove(
                "listening"
            );

            auraAvatar.classList.remove(
                "listening"
            );

        };

}


/* =========================
   MICROPHONE
========================= */

micButton.addEventListener(
    "click",
    function () {

        if (!recognition) {

            alert(
                "Voice recognition is not supported. Use Google Chrome."
            );

            return;

        }

        recognition.start();

    }
);


/* =========================
   CHAT INPUT
========================= */

sendButton.addEventListener(
    "click",
    sendChat
);


chatInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            sendChat();

        }

    }
);


function sendChat() {

    const message =
        chatInput.value.trim();


    if (!message) {

        return;

    }


    addUserMessage(message);

    chatInput.value = "";

    sendCommand(message);

}


/* =========================
   ADD USER MESSAGE
========================= */

function addUserMessage(message) {

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        "chat-message user";


    messageDiv.innerHTML = `

        <div class="message-avatar">
            You
        </div>

        <div class="message-content">

            <strong>You</strong>

            <p>${escapeHtml(message)}</p>

        </div>

    `;


    chatMessages.appendChild(
        messageDiv
    );


    scrollChat();

}


/* =========================
   ADD AURA MESSAGE
========================= */

function addAuraMessage(message) {

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        "chat-message aura";


    messageDiv.innerHTML = `

        <div class="message-avatar">
            A
        </div>

        <div class="message-content">

            <strong>AURA</strong>

            <p>${escapeHtml(message)}</p>

        </div>

    `;


    chatMessages.appendChild(
        messageDiv
    );


    scrollChat();

}


/* =========================
   SEND TO FLASK
========================= */

async function sendCommand(command) {

    status.innerHTML =
        "🧠 Thinking...";


    try {

        const response =
            await fetch("/command", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    command: command

                })

            });


        const data =
            await response.json();


        addAuraMessage(
            data.response
        );


        speak(
            data.response
        );


    }

    catch (error) {

        console.error(error);


        addAuraMessage(
            "Sorry, I couldn't connect to my server."
        );


        status.innerHTML =
            "❌ Server error";

    }

}


/* =========================
   AURA VOICE
========================= */

function speak(text) {

    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.lang =
        "en-IN";

    speech.rate =
        0.95;

    speech.pitch =
        1.05;

    speech.volume =
        1;


    speech.onstart =
        function () {

            auraAvatar.classList.remove(
                "listening"
            );

            auraAvatar.classList.add(
                "speaking"
            );


            status.innerHTML =
                "🗣️ AURA is speaking...";

        };


    speech.onend =
        function () {

            auraAvatar.classList.remove(
                "speaking"
            );


            status.innerHTML =
                "🟢 Ready";

        };


    window.speechSynthesis.speak(
        speech
    );

}


/* =========================
   SCROLL CHAT
========================= */

function scrollChat() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


/* =========================
   SECURITY
========================= */

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;

}