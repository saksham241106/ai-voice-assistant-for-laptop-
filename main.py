from voice import listen
from speech import speak
from commands import execute_command


print("================================")
print("          AURA ASSISTANT")
print("================================")

speak("Hello! I am AURA. Say Hey AURA to wake me.")


while True:

    print("\nWaiting for Hey AURA...")

    # Listen for wake word
    wake_word = listen(3)

    if not wake_word:
        continue

    print("Heard:", wake_word)

    # Check wake word
    if (
        "hey aura" in wake_word
        or "hello aura" in wake_word
        or "hey ora" in wake_word
    ):

        speak("Yes? How can I help you?")

        # Listen for actual command
        command = listen(5)

        if not command:
            speak("I didn't hear a command.")
            continue

        print("Command:", command)

        response = execute_command(command)

        if response == "EXIT":

            speak("Goodbye!")

            break

        speak(response)