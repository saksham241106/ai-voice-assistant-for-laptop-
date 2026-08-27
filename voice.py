import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav


recognizer = sr.Recognizer()



def listen(seconds=3):

    print("\nAURA is listening...")

    sample_rate = 16000

    try:

        recording = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write(
            "recording.wav",
            sample_rate,
            recording
        )

        print("AURA is understanding...")

        recognizer = sr.Recognizer()

        with sr.AudioFile("recording.wav") as source:

            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("YOU:", text)

        return text.lower().strip()

    except sr.UnknownValueError:

        print("AURA couldn't understand you.")

        return ""

    except sr.RequestError:

        print("Speech recognition service is unavailable.")

        return ""

    except Exception as e:

        print("ERROR:", e)

        return ""