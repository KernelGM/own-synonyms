import unidecode
import requests
from bs4 import BeautifulSoup


class Synonyms():
    def __init__(self, word) -> None:
        """Inicia o processo de busca na pagina sinonimos.com.br.

        Args:
            word (str): palavra a ser procurada no site
        """
        self.word = unidecode.unidecode(word.strip().lower())
        self.url = f'http://www.sinonimos.com.br/{self.word}'
        self.resp_get = requests.get(self.url)
        self.soup = BeautifulSoup(self.resp_get.content, features='lxml')
        self.synonyms = []

    def find_title(self):
        """Acha o titulo, algo como: sinonimo de "palavra" e printa isso
        se não achar é porque a palavra foi digitada errada ou não tem
        no banco de dados.
        """
        try:
            print(self.soup.find('h1', {'class': 'h-palavra'}).get_text())
        except Exception:
            print('Essa palavra não existe no banco de dados ou você a digitou \
errado!')

    def find_synonyms(self):
        """Acha os sinonimos da palavra desejada ordenando cada uma com
        o sentido, a ordem e as palavras equivalentes.
        """
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

    def run(self):
        """Executa todos os métodos anteriores.
        """
        try:
            Synonyms(self.word)
            self.find_title()
            self.find_synonyms()
            print('\n')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    string = 'Para começar o projeto você pode optar por várias técnicas, \
        a fim de coletar as informações necessárias'

    string = string.lower().strip().replace('.', '').replace(',', '').split()

    bag_of_words = [word for word in string if len(word) >= 5]
    for word in bag_of_words:
        Synonyms(word).run()
