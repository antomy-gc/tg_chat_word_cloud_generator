import json
import re
from os.path import join

import matplotlib.pyplot as plt
from stop_words import get_stop_words
from wordcloud import WordCloud


class WordCloudCreator:
    workdir: str
    stopwords: set[str]

    def __init__(self):
        stopwords = set(get_stop_words('russian'))
        stopwords.add('знаю')
        stopwords.add('поэтому')
        stopwords.add('вообще')
        stopwords.add('могу')
        self.stopwords = stopwords

    def run(self, workdir, filename):
        self.workdir = workdir
        username, messages = self.load_message_history(filename)
        frequencies = self.make_frequencies_dict(messages)
        cloud = self.gen_cloud(frequencies)
        self.make_image(cloud, username)

    def load_message_history(self, filename: str) -> tuple[str, list[str]]:
        file = open(join(self.workdir, filename), encoding='UTF-8')
        data = json.load(file)
        user_name: str = data['name']
        messages = data["messages"]

        messages = filter(lambda item: item["type"] == 'message', messages)
        messages = map(lambda item: item["text"], messages)
        messages = filter(lambda text: text is not None and type(text) is str and len(text) > 0, messages)

        file.close()
        return user_name, list(messages)

    def make_frequencies_dict(self, messages: list) -> dict[str, float]:
        result = dict()
        for message in messages:
            msg_words = re.findall('[a-zA-Zа-яА-Я]+', message)
            for word in msg_words:
                word = word.lower()
                if (not self.stopwords.__contains__(word)) and len(word) > 3:
                    if result.get(word) is None:
                        result[word] = float(0)
                    result[word] += 1.0
        return result

    @staticmethod
    def gen_cloud(words_dict: dict):
        return WordCloud(width=1170,
                         prefer_horizontal=0.9,
                         height=2532,
                         background_color='black',
                         margin=20,
                         colormap='Pastel1',
                         collocations=False).generate_from_frequencies(words_dict)

    def make_image(self, wordcloud, username):
        # Устанавливаем размер картинки
        plt.figure(figsize=(1170, 2532), dpi=1)
        # Использовать все пространство
        plt.gca().set_position([0, 0, 1, 1])

        plt.imshow(wordcloud)
        plt.axis("off")
        filename = join(self.workdir, username)
        plt.savefig(f'{filename}.png')
