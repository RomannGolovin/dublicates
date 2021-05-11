import librosa
import matplotlib.pyplot as plt
import librosa.display
import os

while True:
    print('Введите адрес файла:')
    data = input()
    if (os.path.exists(data)) & (data[-4:] == '.wav'):
        break
    if not os.path.exists(data):
        print('Такого файла не существует')
    if data[-4:] != '.wav':
        print('Выбран неподходящий файл')

mass, sr = librosa.load(data)
mass_stft = librosa.stft(mass)
mass_db = librosa.amplitude_to_db(abs(mass_stft))
mass_max = mass_db.max(axis=0)
centroids = librosa.feature.spectral_centroid(mass, sr=sr)[0]

plt.figure(figsize=(15, 5))
librosa.display.waveplot(mass, sr=sr)

plt.figure(figsize=(15, 5))
librosa.display.specshow(mass_db, sr=sr)

plt.figure(figsize=(15, 5))
frames = range(len(centroids))
t = librosa.frames_to_time(frames)
plt.plot(t, centroids)

plt.figure(figsize=(15, 5))
plt.plot(t, mass_max)
plt.show()
