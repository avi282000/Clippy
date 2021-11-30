import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

from word_list import Word as custom_word

model_path = r"Model\vosk-model-en-us-daanzu-20200905\vosk-model-en-us-daanzu-20200905"
audio_filename = input("Enter the audio file's name: ")
audio_filename = audio_filename + ".wav"

model = Model(model_path)
wf = wave.open(audio_filename, 'rb') # Opens the Audio File
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
        w=custom_word(obj)
        list_of_words.append(w)

wf.close() # Closes the Audio File

for word in list_of_words:
    print(word.to_string())

offset = 0.5
threshold = 1

starts = []
ends = []

for i in range(len(list_of_words) - 1):
    current_word = list_of_words[i]
    next_word = list_of_words[i+1]
    if next_word.start - current_word.end > threshold:
        # Finds Silence and crops it out
        starts.append(current_word.end + offset)
        ends.append(next_word.start - offset)

# The Segments divided, based on the silence
segments = []
length = max(len(starts), len(ends))
for i in range(length + 1):
    if i == 0:
        segments.append((0, starts[0]))
    elif i == length:
        segments.append((ends[i-1], None))
    else:
        segments.append((ends[i-1], starts[i]))

print("Got the following segments:\n")
print(segments)