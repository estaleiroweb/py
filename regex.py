from importlib.resources import contents
import re
#import regex from 

text_to_search='''
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha HaHa

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \\ | ( )

coreyms.com

321-555-4321
123.555.1234

Mr. Schafer
Mr Smith
Ms Davis
Mr. T
'''

sentence='Start a sentence and then bring it to an end'
pattern=re.compile(r'\bm\w+.? (\w+)',re.IGNORECASE) #re.IGNORECASE + re.MULTILINE + re.DEBUG + re.ASCII + re.DOTALL + re.LOCALE + re.TEMPLATE + re.UNICODE

print(': search: retorna o match da primeira ocorrência')
print(pattern.search(text_to_search)) # re.search(regexp_rtext,text_to_search))
print()

matches=pattern.finditer(text_to_search) # re.finditer(regexp_rtext,text_to_search))
print('- finditer: retorna um iterador com todas os searchs')
print(matches)
print()

print('- finditer for')
for m in matches: 
	print(m)
	print(m.group(0))
	print({
		'obj':m,
		'group':m.group(0),
		'groups':m.groups(0),
		'groupdict':m.groupdict(),
		'start':m.start(0),
		'end':m.end(0),
		'span':m.span(0),
		'lastindex':m.lastindex,
		'endpos':m.endpos,
		'lastgroup':m.lastgroup,
		'pos':m.pos,
		'regs':m.regs,
		'string':m.string,
	},sep='\n')
print()

print('- findall: retorna uma tupla com todas as matched strings')
print(pattern.findall(text_to_search)) # re.findall(regexp_rtext,text_to_search))
print()

print('- match: a partir do inicio da string')
print(pattern.match(text_to_search)) # re.match(regexp_rtext,text_to_search))
print()

print('- match: a partir do inicio da string')
print(pattern.sub('.',text_to_search)) # re.sub(regexp_rtext_from,regexp_rtext_to,text_to_search))
print()

'''
with open(__file__,'r',encoding='utf-8') as f:
	contents= f.read()
	matches=pattern.finditer(contents)
	for match in matches: print(match)

'''