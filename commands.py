import webbrowser
import subprocess
import datetime


def execute_command(command):

    command = command.lower().strip()

    print("COMMAND RECEIVED:", command)

    # YouTube
    if "youtube" in command or "you tube" in command:

        print("Opening YouTube...")

        subprocess.Popen([
            "cmd",
            "/c",
            "start",
            "",
            "https://www.youtube.com"
        ])

        return "Opening YouTube."

    # Google
    elif "google" in command:

        print("Opening Google...")

        subprocess.Popen([
            "cmd",
            "/c",
            "start",
            "",
            "https://www.google.com"
        ])

        return "Opening Google."

    # Calculator
    elif "calculator" in command:

        subprocess.Popen("calc.exe")

        return "Opening Calculator."

    # Notepad
    elif "notepad" in command:

        subprocess.Popen("notepad.exe")

        return "Opening Notepad."

    # File Explorer
    elif "file" in command:

        subprocess.Popen("explorer.exe")

        return "Opening File Explorer."

    # Time
    elif "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        return "The time is " + current_time

    # Date
    elif "date" in command:

        today = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        return "Today's date is " + today

    # Exit
    elif "exit" in command or "quit" in command:

        return "EXIT"

    else:

        return "I don't know that command yet."