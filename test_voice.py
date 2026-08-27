from voice import listen



print("================================")
print("       AURA VOICE TEST")
print("================================")

print("\nSay something after the recording starts.")

text = listen()

print("\nFinal result:")

print(text)