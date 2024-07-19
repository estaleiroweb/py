import requests
from bs4 import BeautifulSoup
import json
import os

__path__=os.path.dirname(__file__)

def load(nome_arquivo:str)->str:
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f'O arquivo {nome_arquivo} não foi encontrado.')
    except IOError:
        print(f'Ocorreu um erro ao tentar ler o arquivo {nome_arquivo}.')

content=load(__path__+'/emojis.html')
# response = requests.get('https://www.webfx.com/tools/emoji-cheat-sheet/')
# content= response.content

soup = BeautifulSoup(content, 'html.parser')

emoji_dict = {}
for sections in soup.select('.section'):
    # sections.get_text
    section = sections.get('id')
    for items in sections:
        if not items.text.strip(): continue
        name = items.get('data-alt-name')
        char = items.select('.windows.emojicon')[0].text.strip()
        item = items.select('._tips > .shortcode')[0].text.strip()[1:-1]
        unicode = items.select('._tips > .unicode')[0].text.strip()
            
        # print(section, item, name, unicode, char)
        emoji_dict[item] = [char,unicode,section,name]

emoji_json = json.dumps(emoji_dict, indent=4, ensure_ascii=False)

with open(__path__+'/emojis.json', 'w', encoding='utf-8') as f:
    f.write(emoji_json)

print('Emojis JSON salvo em emojis.json')
