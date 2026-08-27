import sounddevice as sd
import scipy.io.wavfile as wav

print("================================")
print("       AURA MICROPHONE TEST")
print("================================")

print("\nAvailable microphones:\n")

devices = sd.query_devices()

for i, device in enumerate(devices):
    if device["max_input_channels"] > 0:
        print(i, "-", device["name"])

print("\nRecording will start for 5 seconds.")
print("Speak normally when recording starts.")

input("\nPress ENTER to start...")

sample_rate = 16000

print("\nRecording...")

recording = sd.rec(
    int(5 * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

wav.write(
    "test_recording.wav",
    sample_rate,
    recording
)

print("\nRecording finished!")
print("File saved as: test_recording.wav")