import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

from word_list import Word as custom_word

model_path = r"Model\vosk-model-en-us-aspire-0.2\vosk-model-en-us-aspire-0.2"
audio_filename = input("Enter the audio file's name: ")

model = Model(model_path)
wf = wave.open("sample.wav", "rb") # Opens the Audio File
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# Gets the list of JSON dicts
results = []

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)

part_result = json.loads(rec.FinalResult())
results.append(part_result)

# Converting the JSON dicts to "Word" objects
list_of_words = []

for sentence in results:
    if len(sentence) == 1:
        # For empty returns
        continue
    for obj in sentence["result"]:
        w=custom_word.Word(obj)
        list_of_words.append(w)

wf.close() # Closes the Audio File

for word in list_of_words:
    print(word.to_string())