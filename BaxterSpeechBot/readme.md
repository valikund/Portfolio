Baxter Speech Bot

Created a a voice interface for the Baxter robot, based on Google Speech Api, Api.ai, IBM Watson TTS. Users can interact with Baxter trough voice. Robot can perform online queries, start teaching by demonstration, do simple movements etc. The interesting thing is that it is possible to perform programming-by-demonstration trough voice commands, and api.ai gets refreshed too by the new commands dynamically. (Wrote the whole thing also with wit.ai, but the performance is much worse).

I tried out all the available speech-to-text options (2017). The clear winner was Google Speech both in accuracy and speed. This program has minimal latency, since it is streaming the voice to the cloud. The delay between ending the sentence and getting natural language understanding feedback was around 2 seconds.

The robot movements:
wave_hand_right, wave_hand_left, LearnedActions directory

Main function:
StreamingMain.py -with streaming recognition
GoogleSpeechToText.py -without streaming, but much more speech backends

The available robot actions:
botActions.py

The streaming speech recognizer class:
client.py

Video: https://www.youtube.com/watch?v=dMY-XXwBIb8

