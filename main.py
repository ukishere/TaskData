import json
from operator import itemgetter
import xml.etree.ElementTree as ET

def get_words(string):
    words = {}

    string = string.strip()
    string = string.rstrip('\n')
    string = string.lower()
    string_list = string.split()

    for word in string_list:
        if words.get(word) == None:
            words[word] = 1
        else:
            words[word] += 1

    return words

def words_comparison(words1, words2):
    for word in words1:
        if words2.get(word) != None:
            words2[word] = words1[word] + words2[word]

    words1.update(words2)

    return words1

def get_top10(words):
    words_len_6 = {}

    for word in words:
        if len(word) > 6:
            words_len_6[word] = words[word]

    words_len_6 = sorted(words_len_6.items(), key=itemgetter(1))
    words_len_6.reverse()

    return words_len_6[0:10]

def read_json():
    with open('newsafr.json') as file_json:
        data = json.load(file_json)
        all_words = {}
        for item in data['rss']['channel']['items']:
            words = get_words(item['title'])
            all_words = words_comparison(all_words, words)

            words = get_words(item['description'])
            all_words = words_comparison(all_words, words)

        print('Поиск в файле .json:')
        print(get_top10(all_words))

def read_xml():
    parser = ET.XMLParser(encoding = 'utf-8')
    tree = ET.parse('newsafr.xml', parser)
    root = tree.getroot()
    channel = root.find('channel')
    items = channel.findall('item')
    all_words = {}

    for item in items:
        words = get_words(item.find('title').text)
        all_words = words_comparison(all_words, words)

        words = get_words(item.find('description').text)
        all_words = words_comparison(all_words, words)

    print('Поиск в файле .xml:')
    print(get_top10(all_words))

choise = 0

while choise != 3:
    try:
        choise = int(input('1. Прочитать .json\n2. Прочитать .xml\n3. Выход\n'))
        if choise == 1:
            read_json()
        elif choise == 2:
            read_xml()
        elif choise == 3:
            break
        else:
            print('Неверный ввод')
    except ValueError:
        print('Неверный ввод')