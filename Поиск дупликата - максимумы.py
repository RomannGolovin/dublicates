import librosa
import numpy as np
import glob
import os

while True:
    data = input('Введите директорию для хранения служебных файлов:\n')
    if data[-1] != '\\':
        data += '\\'
    if os.path.exists(data + "first_path.txt"):
        break
    if not os.path.exists(data + "first_path.txt"):
        print('Такой директории не существует или выбрана неверная директория')

file = open(data + "first_path.txt")
path = file.read()
file.close()

while True:
    data = input('Введите адрес файла:\n')
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

os.chdir(path)
music_list = []
for file in glob.glob("*.npy"):
    music_list.append(file)

flag = True
print('Поиск дубликатов файла по методу максимумов дал следующие результаты:')
for i in range(len(music_list)):
    mass_2 = np.load(path+music_list[i])
    if np.array_equal(mass_max, mass_2):
        print(music_list[i][:-3]+'wav')
        flag = False

if flag:
    final_path = path + data[data.rfind('\\')+1:-4]
    np.save(final_path, mass_max)
    print('Дубликаты не обнаружены')
