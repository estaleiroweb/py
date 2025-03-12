# Classes/Objects

# Magic Methods
print([
    '\N{GREEK CAPITAL LETTER DELTA}',  # Using the character name
    '\u0394',  # Using a 16-bit hex value
    '\U00000394',  # Using a 32-bit hex value
    chr(57344),
    ord('\ue000'),
])

u = b'\x80abc'
# print(u.decode('utf-8', 'replace')))
# print(u.decode('utf-8', 'backslashreplace')))
# print(u.decode('utf-8', 'ignore')))

u = chr(40960) + 'abcd' + chr(1972)
print([
    u.encode('utf-8'),
    u.encode('ascii', 'ignore'),
    u.encode('ascii', 'replace'),
    u.encode('ascii', 'xmlcharrefreplace'),
    u.encode('ascii', 'backslashreplace'),
    u.encode('ascii', 'namereplace'),
])

s = 'a\xac\u1234\u20ac\U00008000'
print(s, [ord(c) for c in s])

x = ['\u2588', u'\u2588', r'\u2588', b'Hello', 20.5, 20.5e10, 1]
print(x)
print([type(c) for c in x])

# print(type(x))
# b = "Hello, World!"
