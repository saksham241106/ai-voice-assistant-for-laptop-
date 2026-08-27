from flask import Flask, render_template, request, jsonify
import datetime
import webbrowser
import subprocess
import platform
import shutil
import urllib.parse
import random
import os
from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
def ask_openai(message):

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions="""
            You are AURA, a friendly personal AI assistant.
            Answer clearly and helpfully.
            Keep normal answers reasonably concise.
            You are part of a student's AI assistant project.
            """,
            input=message
        )

        return response.output_text

    except Exception as e:
        print("OpenAI error:", e)
        return "Sorry, I couldn't connect to my AI brain."
app = Flask(__name__)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# AURA COMMAND ENGINE
# ==========================================

def process_command(command):

    command = command.lower().strip()

    # -------------------------------
    # HELLO
    # -------------------------------

    if any(word in command for word in ["hello", "hi", "hey"]):

        return "Hello! I am AURA. How can I help you today?"


    # -------------------------------
    # WHO ARE YOU
    # -------------------------------

    if "who are you" in command:

        return (
            "I am AURA, your personal AI assistant. "
            "I can open applications, search the web, "
            "tell you the time, give system information "
            "and help you with everyday tasks."
        )


    # -------------------------------
    # TIME
    # -------------------------------

    if "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}."


    # -------------------------------
    # DATE
    # -------------------------------

    if (
        "date" in command
        or "today" in command
        or "today's date" in command
    ):

        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return f"Today is {current_date}."


    # -------------------------------
    # YOUTUBE
    # -------------------------------

    if "youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return "Opening YouTube for you."


    # -------------------------------
    # GOOGLE
    # -------------------------------

    if "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        return "Opening Google."


    # -------------------------------
    # GITHUB
    # -------------------------------

    if "open github" in command:

        webbrowser.open(
            "https://github.com"
        )

        return "Opening GitHub."


    # -------------------------------
    # GMAIL
    # -------------------------------

    if "open gmail" in command:

        webbrowser.open(
            "https://mail.google.com"
        )

        return "Opening Gmail."


    # -------------------------------
    # CHATGPT
    # -------------------------------

    if "open chatgpt" in command:

        webbrowser.open(
            "https://chatgpt.com"
        )

        return "Opening ChatGPT."


    # -------------------------------
    # MUSIC
    # -------------------------------

    if (
        "play music" in command
        or "open music" in command
    ):

        webbrowser.open(
            "https://music.youtube.com"
        )

        return "Opening YouTube Music."


    # -------------------------------
    # SEARCH WEB
    # -------------------------------

    if (
        "search web" in command
        or "search google" in command
    ):

        if "search web" in command:

            search_text = command.replace(
                "search web", ""
            ).strip()

        else:

            search_text = command.replace(
                "search google", ""
            ).strip()


        if not search_text:

            return "What would you like me to search for?"


        encoded_query = urllib.parse.quote_plus(
            search_text
        )

        url = (
            "https://www.google.com/search?q="
            + encoded_query
        )

        webbrowser.open(url)

        return f"Searching the web for {search_text}."


    # -------------------------------
    # CALCULATOR
    # -------------------------------

    if (
        "open calculator" in command
        or "calculator" == command
    ):

        try:

            subprocess.Popen(
                "calc.exe"
            )

            return "Opening Calculator."

        except Exception:

            return "I couldn't open Calculator."


    # -------------------------------
    # VS CODE
    # -------------------------------

    if (
        "open vscode" in command
        or "open vs code" in command
    ):

        try:

            subprocess.Popen(
                "code"
            )

            return "Opening Visual Studio Code."

        except Exception:

            return (
                "I couldn't open VS Code. "
                "Make sure the code command is available."
            )


    # -------------------------------
    # WEATHER
    # -------------------------------

    if "weather" in command:

        webbrowser.open(
            "https://www.google.com/search?q=weather"
        )

        return "Opening the latest weather information."


    # -------------------------------
    # SYSTEM INFORMATION
    # -------------------------------

    if (
        "system information" in command
        or "system info" in command
        or "my computer" in command
    ):

        system = platform.system()

        version = platform.version()

        processor = platform.processor()

        disk = shutil.disk_usage("/")

        free_gb = round(
            disk.free / (1024 ** 3),
            2
        )

        total_gb = round(
            disk.total / (1024 ** 3),
            2
        )


        return (
            f"Your system is running {system}. "
            f"Processor: {processor}. "
            f"Disk space: {free_gb} GB free "
            f"out of {total_gb} GB."
        )


    # -------------------------------
    # JOKE
    # -------------------------------

    if "joke" in command:

        jokes = [

            "Why did the programmer quit his job? "
            "Because he didn't get arrays!",

            "Why do programmers prefer dark mode? "
            "Because light attracts bugs!",

            "There are only 10 kinds of people: "
            "those who understand binary and those who don't."

        ]

        return random.choice(jokes)


    # -------------------------------
    # HELP
    # -------------------------------

    if (
        "help" in command
        or "what can you do" in command
        or "commands" in command
    ):

        return (
            "I can open YouTube, Google, GitHub, Gmail, "
            "ChatGPT, VS Code and Calculator. "
            "I can search the web, tell the time and date, "
            "give system information, open music, "
            "check weather and tell jokes."
        )


    # -------------------------------
    # THANK YOU
    # -------------------------------

    if (
        "thank you" in command
        or "thanks" in command
    ):

        return "You're welcome! I'm always ready to help."


    # -------------------------------
    # EXIT
    # -------------------------------

    if (
        "goodbye" in command
        or "bye" in command
    ):

        return "Goodbye! I'll be here whenever you need me."


    # -------------------------------
    # UNKNOWN COMMAND
    # -------------------------------

    return (
        "I don't know that command yet. "
        "Try saying 'help' to see what I can do."
    )


# ==========================================
# COMMAND API
# ==========================================

@app.route("/command", methods=["POST"])
def command():

    data = request.get_json()

    message = data.get("command", "").strip()

    if not message:
        return jsonify({
            "response": "Please type something."
        })

    # Your local AURA commands first
    local_response = process_command(message)

    # Send unknown/general questions to OpenAI
    if local_response.startswith("I don't know that command"):
        response = ask_openai(message)
    else:
        response = local_response

    return jsonify({
        "response": response
    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("          AURA AI ASSISTANT")
    print("======================================")
    print()
    print("AURA is running!")
    print()
    print("Open:")
    print("http://127.0.0.1:5000")
    print()
    print("Available commands:")
    print("- YouTube")
    print("- Google")
    print("- Search Web")
    print("- GitHub")
    print("- Gmail")
    print("- ChatGPT")
    print("- VS Code")
    print("- Calculator")
    print("- Music")
    print("- Weather")
    print("- Time")
    print("- Date")
    print("- System Information")
    print("- Jokes")
    print()
    print("======================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
