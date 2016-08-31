# Got this here: http://developers.vokaturi.com/using/python-sample
# "On Windows, you replace Vokaturi_mac.so with Vokaturi_win32.dll 
#  or Vokaturi_win64.dll, and you may have to put libgcc_s_sjlj-1.dll 
#  in the same folder as your script." 
# analyze_one_file.py
#
# Paul Boersma 2016-04-14
#
# A script that uses the Vokaturi library to extract the emotions from
# a wav file on disk. The file has to contain a mono recording.
#
# Call syntax:
#   python3 analyze_one_file.py path_to_sound_file.wav

import sys
import os
import scipy.io.wavfile

sys.path.append(os.path.join(sys.path[0],'api'))

import Vokaturi

file_name = sys.argv[1]

libPath = os.path.join(sys.path[0],'lib','Vokaturi_mac.so')
Vokaturi.load(libPath)

os.system('clear')

(sample_rate, samples) = scipy.io.wavfile.read(file_name)
samples = samples[:] / 32768.0
buffer_length = len(samples)
c_buffer = Vokaturi.SampleArrayC(buffer_length)

# something weird with original sample code here.
# try just the first element in array.
for index in range(len(samples)):
   c_buffer[index] = samples[index][0]

voice = Vokaturi.Voice(sample_rate, buffer_length)
emotionProbabilities = Vokaturi.EmotionProbabilities()
voice.fill(buffer_length, c_buffer)
voice.extract(None, None, emotionProbabilities)
voice.destroy()

print("  (◕‿◕)   Happiness: %.3f" % emotionProbabilities.happiness)
print("  (ಠ_ಠ)   Neutral: %.3f" % emotionProbabilities.neutrality)
print("  (ಠ⌣ಠ)   Sadness: %.3f" % emotionProbabilities.sadness)
print("  (⊙﹏⊙)  Fear: %.3f" % emotionProbabilities.fear)
print("ヽ(ಠ_ಠ)ノ Anger: %.3f" % emotionProbabilities.anger)
