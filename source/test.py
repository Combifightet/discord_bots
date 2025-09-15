from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import requests

from typing import Optional

class Meaning:
	def __init__(self, meaning:Optional[str], infos:Optional[dict[str, tuple[str, Optional[str]]]], examples:Optional[list[str]]):
		"""
		Class that holds a meaning object, only used for structuring data
		Args:
			meaning (str): The meaning text
			tuples (dict[str, tuple[str, str | None]] | None): A dict of additional information about the meaning<br>dict(\<title\>, tuple(\<content\>, \<link\>))
			examples (list[str]): A list of example sentences for this meaning
		"""
		self.meaning = meaning
		self.infos = infos
		self.examples = examples
	
	def __str__(self):
		infoString:str = ''
		if self.infos:
			for info in self.infos.keys():
				infoString += f'\n  {info}: {self.infos[info][0]}'
				if self.infos[info][1] is not None:
					infoString += f' ({self.infos[info][1]})'

		examplesString:str = ''
		if self.examples:
			examplesString = '\n  Examples:'
			for example in self.examples:
				examplesString += f'\n   - {example}'

		return f'{self.meaning}\n{infoString}\n{examplesString}'
	
	def toMdListItem(self) -> str:
		blank_line:str = ' ​  '
		result:str = f'{blank_line}\n0. '

		items:list[str] = []

		if self.meaning:
			items.append(self.meaning)

		if self.infos:
			for key in self.infos.keys():
				value:tuple[str, Optional[str]] = self.infos[key]
				if value[1]:
					items.append(f'{key}        [**{value[0]}**]({value[1]})')
				else:
					items.append(f'{key}        **{value[0]}**')

		if self.examples:
			examples_str:str = '```'
			for example in self.examples:
				examples_str += f'\n• {example}'
			examples_str += '\n```'
			items.append(examples_str)
		
		if items:
			result += items.pop(0)
		for item in items:
			result += f'\n{blank_line}\n{item}'
		return result


	

def tuplesToDict(tuples:ResultSet) -> dict[str, tuple[str, str|None]]:
	result:dict[str, str] = {}
	for tuple in tuples:
		linkTag:Tag = tuple.find('dd').find('a')
		link:str = None
		if linkTag is not None:
			link = linkTag.get('href')

		result[tuple.find('dt').text] = (tuple.find('dd').text.lstrip('\n').rstrip('\n'), link)
	return result

def dictValWhereKeyContains(d:dict[str, tuple[str, str|None]], keyPart:str, caseSensitive=False) -> str | None:
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

	# <div class="division "  id="bedeutungen">
	meaningHtml:Tag = soup.find('div', class_='division', id='bedeutungen')
	meaningTitle:str = meaningHtml.find('h2').text
	meaningsHtml:Tag = meaningHtml.find_all('li', class_='enumeration__item')
	meanings:list[list[Meaning]] = []
	for m in meaningsHtml:
		subMeaningsHtml:Tag = m.find_all('li', class_='enumeration__sub-item')
		subMeanings:list[Meaning] = []
		for sm in subMeaningsHtml:
			meaning:str = None
			if sm.find('div', class_='enumeration__text'):
				meaning = sm.find('div', class_='enumeration__text').text
			
			infos:dict[str, tuple[str, str|None]] = tuplesToDict(sm.find_all('dl', class_='tuple'))

			examples:list[str] = []
			if sm.find('ul', class_='note__list'):
				for example in sm.find('ul', class_='note__list').find_all('li'):
					examples.append(example.text)
			
			subMeanings.append(Meaning(meaning, infos, examples))
			print('--------------------------------------------')
			print(subMeanings[-1].toMdListItem())
		meanings.append(subMeanings)
			
	
	tuples:ResultSet = soup.find_all('dl', class_='tuple')
	pronounciation:Optional[Tag] = None
	for tup in tuples:
		pronounciation = tup.find(class_='ipa')
		if pronounciation:
			break

	infos:dict[str, str] = tuplesToDict(tuples)

	# Meaning()

	# _**▃▃ ▃▃ ▁▁▁ ▁▁▁ ▁▁▁**_

	# ▰▰▱▱▱

	print('\n')
	print('Title:     ', f'**{title[0].replace('\\xad','').replace('\xad', '')}**')
	print('Url:       ', url)
	print('Wortart:   ', f'**{dictValWhereKeyContains(infos, 'wortart')[0]}**')
	print('Häufigkeit:', f'_**{dictValWhereKeyContains(infos, 'häufigkeit')[0].replace('▒', '▃▃ ').replace('░', '▁▁▁')}**_')
	print('Aussprache:', f'**{pronounciation.text}**')
	# --- Rechtschreibung ---
	# --- Bedeutungen (n) ---            ! Wichtig
	print(meaningTitle)
	# print(meaningHtml.prettify())
	# print(meanings[-1].prettify())
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
