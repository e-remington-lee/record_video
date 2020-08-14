## https://www.youtube.com/watch?v=Oa_d-zaUti8&t=435s
## 11- Preprocessing audio data for Deep Learning
import librosa, librosa.display
import matplotlib.pyplot as plt
import numpy as np


sound_file = "./databases/TESS_and_RAVDESS/Angry/03-01-05-01-01-01-01.wav"

# sample rate is per second. 2 second video we have about 44,000 samples
signal, sr = librosa.load(sound_file, sr=22050)

# librosa.display.waveplot(signal, sr=sr)
# plt.xlabel("Time")
# plt.ylabel("Amplitude")
# plt.show()

fft = np.fft.fft(signal)

magnitude = np.abs(fft)
frequency = np.linspace(0, sr, len(magnitude))

left_magnitude = magnitude[:int(len(frequency)/2)]
left_frequency = frequency[:int(len(frequency)/2)]

# plt.plot(left_frequency, left_magnitude)
# plt.plot(frequency, magnitude)
# plt.xlabel("Frequency")
# plt.ylabel("Magnitude")
# plt.show()

# how many samples we perform a fourier transform on
n_fft = 2048
# How much we shift to the right per fourier transform
hop_length = 512

stft = librosa.core.stft(signal, hop_length=hop_length, n_fft=n_fft)
spectogram = np.abs(stft)

# This makes it easier to visualize. Can be run on just the spectrogram
log_spectrogram = librosa.amplitude_to_db(spectogram)

# librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length)
# plt.xlabel("Time")
# plt.ylabel("Frequency")
# plt.colorbar()
# plt.show()

# n_mfcc = 13 is standard. One video talks about how there can be 26, but 13 is most valubale for AI 
mffc = librosa.feature.mfcc(signal, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)
print(mffc)
print(mffc.T)

librosa.display.specshow(mffc, sr=sr, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("MFCC")
plt.colorbar()
plt.show()