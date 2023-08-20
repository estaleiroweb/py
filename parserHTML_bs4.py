import requests
import re
from bs4 import BeautifulSoup, ResultSet, Tag
from pprint import pprint

url = 'https://pt.iban.com/currency-codes'
print(url)

try:
    res = requests.get(url)
except:
    print('error URL')
    quit()

def addslashes(string, sub=re.compile(r"[\\\"']").sub):
    def fixup(m):
        return "\\" + m.group(0)
    return sub(fixup, string)
soup = BeautifulSoup(res.text, features='html.parser')
# soup = BeautifulSoup(res.text, features='lxml')

# tags = soup.find_all('a', attrs={'href': re.compile(r'\.mid$')}, string=re.compile(r'^((?!\().)*$'))
# tags=soup.find_all('table')
trs = soup.select('div.flat-services table tr')


def quote(tag: Tag):
    t = tag.text.strip()
    if t:
        if re.match('\d+(\.\d*)?|\d*\.\d+$',t):
            return t
        return f'"{addslashes(t)}"'
    return 'None'


for tr in trs:
    cells = tr.select('th,td')
    line = [quote(tag) for tag in cells]
    print(','.join(line))
    # for tag in cells:
    #     pprint({
    #         'attrs': tag.attrs,
    #         'contents': len(tag.contents),
    #         'children': tag.children,
    #         'example': f'{tag}'[0:100],
    #         'text': f'{tag.text}'[0:100],
    #     })
    # l:ResultSet=tag
