import re
# Abrindo um arquivo em modo de leitura ('r')
nome_arquivo = 'C:\\AppData\\Code\\py\\SIP_BICC.txt'
conteudo=None

try:
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
except FileNotFoundError:
    print(f'O arquivo {nome_arquivo} não foi encontrado.')
except IOError:
    print(f'Ocorreu um erro ao tentar ler o arquivo {nome_arquivo}.')

if not conteudo: quit()

def h2char(hexa):
    return chr(int(hexa, 16))
def h2charMatch(hexa):
    return h2char(hexa.group(0)[-2:])
def h2text(match):
    return re.sub(r'[0-0A-Fa-f]{2}',h2charMatch,re.sub(r'\n','',match.group(1)))
def b2text(match):
    # return bytes.fromhex(match.group(1)) #.decode('utf-8')
    c=match.group(1)
    c=re.sub(r'\\t','\t',c)
    c=re.sub(r'\\r','\r',c)
    c=re.sub(r'\\n','\n',c)
    c=re.sub(r'\\x[0-9A-Fa-f]{2}',h2charMatch,c)
    return c

conteudo = re.sub(r"b'((?:\\'|[^'])*?)'", b2text, conteudo)
conteudo = re.sub(r'DATA\n([0-9A-F\n]*)END', h2text, conteudo)
print(conteudo)

