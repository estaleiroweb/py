import requests
from selectolax.parser import HTMLParser


url = 'https://pt.iban.com/currency-codes'
print(url)

try:
    res = requests.get(url)
except:
    print('error URL')
    quit()

tree = HTMLParser(res.text)

tags = tree.css('div.flat-services table tr')

for node in tags:
    # itens = [t.text() for t in node.css('td')]
    itens = [t.text() for t in node.iter()]
    print({node.tag:itens,'attr':node.attributes})

    # print(node.text(deep=True, separator=',', strip=True))

    # for i in node.iter():
    #     print('###',i)
    # print(node.parent.tag)
    # print(node.html)