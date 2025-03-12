precos = [1000,1500,1250,2500]

def add_tax(preco):
	return preco * 1.1

precos_com_imposto=list(map(add_tax,precos))
print(precos_com_imposto)
