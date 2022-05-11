import requests
import unidecode
from bs4 import BeautifulSoup


class Synonyms():
    def __init__(self) -> None:
        self.synonyms = []

    def find_title(self):
        try:
            print(self.soup.find('h1', {'class': 'h-palavra'}).get_text())
        except Exception:
            print('Essa palavra não existe no BD ou você a digitou errado!')

    def find_synonyms(self):
        for data in self.soup.find_all('p', {'class': 'sinonimos'}):
            for remove_example in self.soup.find_all('span'):
                for remove_number in self.soup.find_all('em'):
                    if 'class' in remove_number.attrs:
                        if 'number' in remove_number.attrs['class']:
                            remove_number.extract()
                    if 'class' in remove_example.attrs:
                        if 'exemplo' in remove_example.attrs['class']:
                            remove_example.extract()
            self.synonyms.append(
                data.get_text().strip().replace('.', '').split(','))

        for index, word in enumerate(self.synonyms):
            print(index, word)

    def word(self, word):
        self.word = unidecode.unidecode(word.strip().lower())
        self.url = f'http://www.sinonimos.com.br/{self.word}'
        self.resp_get = requests.get(self.url)
        self.soup = BeautifulSoup(self.resp_get.content, features='lxml')
        try:
            self.find_title()
            self.find_synonyms()
        except Exception as e:
            print(e)

    def text(self, text, size_of_word=5):
        self.text = text.lower().strip()\
            .replace('.', '').replace(',', '').split()

        self.bag_of_words = [
            word for word in self.text if len(word) >= size_of_word
        ]

        for single_word in self.bag_of_words:
            Synonyms().word(single_word)


if __name__ == '__main__':
    texto = 'Para começar o projeto você pode optar por várias técnicas, \
        a fim de coletar as informações necessárias'

    Synonyms().text(texto)

    palavra = 'achar'

    Synonyms().word(palavra)
