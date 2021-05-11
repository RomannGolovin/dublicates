import librosa
import numpy as np
import glob
import os

while True:
    data = input('Введите директорию для хранения служебных файлов:\n')
    if os.path.exists(data):
        break
    if not os.path.exists(data):
        print('Такой директории не существует')

while True:
    path = input('Введите директорию с аудиофайлами:\n')
    if os.path.exists(path):
        break
    if not os.path.exists(path):
        print('Такой директории не существует')

while True:
    path_2 = input('Введите директорию для хранения отпечатков:\n')
    if os.path.exists(path_2):
        break
    if not os.path.exists(path_2):
        print('Такой директории не существует')

first_path = path_2 + "\Максимумы\\"
second_path = path_2 + "\Центроиды\\"
os.chdir(path)
music_list = []

file = open(data+'\\first_path.txt', "w+")
file.write(first_path)
file.close()

file = open(data+'\second_path.txt', "w+")
file.write(second_path)
file.close()

for file in glob.glob("*.wav"):
    music_list.append(file)

if len(music_list) > 0:
    print('Создание отпечатков началось, ожидайте')
else:
    print('В указанной директории аудиофайлов не обнаружено')

for i in range(len(music_list)):
    data = music_list[i]
    x, sr = librosa.load(data)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))

    mass_max = Xdb.max(axis=0)
    final_path = first_path + music_list[i][:len(music_list[i])-4]
    np.save(final_path, mass_max)

    centroids = librosa.feature.spectral_centroid(x, sr=sr)[0]
    final_path_2 = second_path + music_list[i][:len(music_list[i])-4]
    np.save(final_path_2, centroids)

if len(music_list) > 0:
    print('Создание отпечатков завершено')

yes_list = ['Yes', 'yes', 'Да', 'да']
no_list = ['No', 'no', 'Нет', 'нет']

# создание списка отпечатков типа максимум
os.chdir(first_path)
max_list = []
for file in glob.glob("*.npy"):
    max_list.append(file)

# поиск по максимумам тк они занимают меньше места

while True:
    search_files = input('Желаете провести поиск дубликатов среди имеющихся файлов? (Да/Нет)\n')
    if search_files in yes_list or search_files in no_list:
        break
    else:
        print('Пожалуйста, введите корректный ответ')

if search_files in yes_list:
    dub_found = -1  # число найденных групп дубликатов
    dub_list = []  # список строк с названиями найденных дубликатов
    # dub_index = 0
    repeat_list = []  # номера элементов у которых есть дубликаты
    for i in range(len(max_list)):
        flag = False  # если False, то еще не найдены дубликаты этого элемента
        mass_1 = np.load(first_path + max_list[i])
        for j in range(i + 1, len(max_list)):
            mass_2 = np.load(first_path + max_list[j])
            if np.array_equal(mass_1, mass_2) and j not in repeat_list:
                dub_list.append('')
                if flag:
                    repeat_list.append(j)
                    dub_list[dub_found] += '; ' + max_list[j][:-3] + 'wav'
                else:
                    flag = True
                    dub_found += 1
                    dub_list[dub_found] += max_list[i][:-3] + 'wav'
                    repeat_list.append(i)
                    repeat_list.append(j)
                    dub_list[dub_found] += '; ' + max_list[j][:-3] + 'wav'

if search_files in yes_list:
    print('Найдены следующие группы дубликатов:')
    for i in range(len(dub_list)):
        if len(dub_list[i]) > 0: print("{}: {}, {}".format(i+1, dub_list[i], len(dub_list[i])))
else:
    print('работа программы завершена')

if dub_found > 0:
    while True:
        delete_files = input('Желаете удалить некоторые из найденных дубликатов? (Да/Нет)\n')
        if delete_files in yes_list or search_files in no_list:
            break
        else:
            print('Пожалуйста, введите корректный ответ')


# найти элементы  у которых есть дубликаты

# лучше записывать в строку номера элементов дубликатов с разделителями 1.2.10.
# а в другой список просто номера в любом порядке

# берем i-й элемент
# сравниваем по очереди элементы с i-м
# если нашли дубликат (j-й) и j нет в repeat_list, то:
    # создаем элемент в dub_list (порядковый номер dub_found)
    # если мы еще не находили дубликат i-го, то
        # в элемент dub_list (порядковый номер dub_found) добавляем i-й, точку и j-й
        # добавляем в repeat_list элементы со значениями i и j
    # если уже находили дубликат i-го, то
        # в элемент dub_list (порядковый номер dub_found) добавляем точку и j-й
        # добавляем в repeat_list элемент со значениями j
    # увеличиваем dub_found на 1



# эту часть мб нужно будет переделать
#    if dub_found == 0:
#        print('Дубликаты не обнаружены')
#    else:
#        print('Обнаружено ', dub_found, ' дубликатов:')
#        for i in range(dub_found):
#            print(i, ': ', dub_list[i])
#
#        delete_files = input('Желаете провести поиск дубликатов среди имеющихся файлов? (Да/Нет)\n')
#        if delete_files == 'Да' or 'да' or 'Yes' or 'yes': # тут тоже надо сделать проверку правильности ответа

