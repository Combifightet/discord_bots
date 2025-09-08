from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import requests

class Meaning:
	def __init__(self, meaning:str, tuples:tuple[str, str, str|None]|None, examples:list[str]):
		"""
		Class that holds a meaning object, only used for structuring data
		Args:
			meaning (str): The meaning text
			tuples (tuple[str, str, Optional[str]]|None): A tuple of additional information about the meaning, e.g. (Wortart, Substantiv, f)
			examples (list[str]): A list of example sentences for this meaning
		"""
		self.meaning = meaning
		self.tuples = tuples
		self.examples = examples

def findTuple(tuples:ResultSet, key:str) -> tuple[str, str]:
	print(type(tuples))
	for tuple in tuples:
		result = tuple.find(string=lambda text: key in text if text else False)
		if result is not None:
			return (result, tuple.find('dd').text)


def main():
	word = 'Titel'

	response: requests.Response = requests.get(f'https://www.duden.de/rechtschreibung/{word}')
	soup = BeautifulSoup(response.text, 'html.parser')

	title:str = soup.find('h1').text,
	url:str = soup.find('meta', property='og:url')['content']
	imagUrl:str = soup.find('meta', property='og:image:url')['content']

	tuples:ResultSet = soup.find_all('dl', class_='tuple')

	# <div class="division "  id="bedeutungen">
	meaningHtml:Tag = soup.find('div', class_='division', id='bedeutungen')
	meaning:str = meaningHtml.find('h2').text
	meaningsHtml:Tag = meaningHtml.find_all('li')

	meanings:list[list[str]] = []
	meanings = meaningsHtml
	Meaning()


	print()

	print('\n')
	print('Title:   ', str(title).replace('\\xad','').replace('\xad', ''))
	print('Url:     ', url)
	print(findTuple(tuples, 'Wortart'))
	print(findTuple(tuples, 'Häufigkeit')) # - TODO: these need postprocessing
	print(findTuple(tuples, 'Aussprache')) # - TODO: these need postprocessing
	# --- Rechtschreibung ---
	# --- Bedeutungen (n) ---            ! Wichtig
	print(meaning)
	# print(meanings)
	for m in meanings:
		print()
		print(m.prettify())
	# --- Synonyme zu <wort> ---
	# --- Herkunft ---
	# --- Grammatik ---
	print('ImageUrl:', imagUrl)
	print('\n')

	if (response.status_code>=400 and response.status_code<500):
		print(f'can\'t find a duden entry for \'{word}\'')

if __name__ == '__main__':
	main()
