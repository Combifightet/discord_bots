from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import requests

class Meaning:
	def __init__(self, meaning:str, tuples:tuple[str, str, str | None] | None, examples:list[str]):
		"""
		Class that holds a meaning object, only used for structuring data
		Args:
			meaning (str): The meaning text
			tuples (tuple[str, str, str | None] | None): A tuple of additional information about the meaning<br>tuple(\<title\>, \<content\>, \<link\>)
			examples (list[str]): A list of example sentences for this meaning
		"""
		self.meaning = meaning
		self.tuples = tuples
		self.examples = examples

def tuplesToDict(tuples:ResultSet) -> dict[str, str]:
	result:dict[str, str] = {}
	for tuple in tuples:
		result[tuple.find('dt').text] = tuple.find('dd').text
	return result

def dictValWhereKeyContains(d:dict[str, str], keyPart:str, caseSensitive=False) -> str | None:
	for k in d.keys():
		if (caseSensitive and keyPart in k) or (not caseSensitive and keyPart.lower() in k.lower()):
			return d[k]
	return None

def main():
	word = 'Titel'

	response: requests.Response = requests.get(f'https://www.duden.de/rechtschreibung/{word}')
	soup = BeautifulSoup(response.text, 'html.parser')

	title:str = soup.find('h1').text,
	url:str = soup.find('meta', property='og:url')['content']
	imagUrl:str = soup.find('meta', property='og:image:url')['content']

	tuples:ResultSet = soup.find_all('dl', class_='tuple')

	infos:dict[str, str] = tuplesToDict(tuples)

	# <div class="division "  id="bedeutungen">
	meaningHtml:Tag = soup.find('div', class_='division', id='bedeutungen')
	meaning:str = meaningHtml.find('h2').text
	meaningsHtml:Tag = meaningHtml.find_all('li', class_='enumeration__item')
	for m in meaningsHtml:
		subMeanings:Tag = m.find_all('li', class_='enumeration__sub-item')
		for sm in subMeanings:
			pass

	meanings:list[list[str]] = []
	meanings = meaningsHtml
	# Meaning()



	print('\n')
	print('Title:     ', str(title).replace('\\xad','').replace('\xad', ''))
	print('Url:       ', url)
	print('Wortart:   ', dictValWhereKeyContains(infos, 'wortart'))
	print('Häufigkeit:', dictValWhereKeyContains(infos, 'häufigkeit')) # - TODO: these need postprocessing
	print('Aussprache:', dictValWhereKeyContains(infos, 'aussprache')) # - TODO: these need postprocessing
	# --- Rechtschreibung ---
	# --- Bedeutungen (n) ---            ! Wichtig
	print(meaning)
	# print(meaningHtml.prettify())
	print(meanings[-1].prettify())
	# for m in meanings:
	# 	print()
	# 	print(m.prettify())
	# --- Synonyme zu <wort> ---
	# --- Herkunft ---
	# --- Grammatik ---
	print('ImageUrl:  ', imagUrl)
	print('\n')

	if (response.status_code>=400 and response.status_code<500):
		print(f'can\'t find a duden entry for \'{word}\'')

if __name__ == '__main__':
	main()
