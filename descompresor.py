import sys


def reconstruirArbol(ArbolBase, codigo, lencodigo, byte):
	if not lencodigo:
		ArbolBase.append(byte)
		ArbolBase.append([])
		ArbolBase.append([])
		return
	if not ArbolBase:
		ArbolBase.append(0)
		ArbolBase.append([])
		ArbolBase.append([])
	if codigo & (1 << (lencodigo - 1)):
		return reconstruirArbol(ArbolBase[2], codigo, lencodigo - 1, byte)
	return reconstruirArbol(ArbolBase[1], codigo, lencodigo - 1, byte)


def restante(hecho, total):
	print(f"\r  -> {hecho}÷{total} => {100*hecho/total:.2f}%", end = "\r")


def nextBit(huff, overflow, bytebuffer, bitbuffer):
	if bitbuffer == -1:
		restante(bytebuffer, len(huff))
	bytebuffer += bitbuffer == -1
	bitbuffer += (bitbuffer == -1) << 3
	if bytebuffer != len(huff) and (bytebuffer != len(huff) - 1 or overflow != bitbuffer + 1):
		return huff[bytebuffer] & (1 << bitbuffer) > 0, bytebuffer, bitbuffer - 1
	return -1, bytebuffer, bitbuffer


def comparar(huff, arbol, overflow, archivo):
	bytebuffer, bitbuffer = 0, 7
	subarbol = arbol
	bit, bytebuffer, bitbuffer = nextBit(huff, overflow, bytebuffer, bitbuffer)
	with open(archivo, "wb") as guardar:
		while bit != -1:
			subarbol = subarbol[1 + bit]
			if not (subarbol[1] or subarbol[2]):
				guardar.write(bytes([subarbol[0]]))
				subarbol = arbol
			bit, bytebuffer, bitbuffer = nextBit(huff, overflow, bytebuffer, bitbuffer)
	return subarbol == arbol


def main():
	argumentos = sys.argv[1:]
	huff, arbol, archivo = argumentos
	huff, arbol = open(huff, "rb").read(), open(arbol, "rb").read()
	overflow, arbol = arbol[0], arbol[1:]
	arbolBase = [0, [], []]
	i = 0
	while i < len(arbol):
		valor = arbol[i]
		i += 1
		lencod = arbol[i]
		lencodNOCHANGE = arbol[i]
		i += 1
		codigo = 1
		while lencod > 8:
			codigo = (codigo << 8) | arbol[i]
			lencod -= 8
			i += 1
		codigo = (codigo << lencod) | (arbol[i] >> (8 - lencod))
		i += 1
		reconstruirArbol(arbolBase, codigo, lencodNOCHANGE, valor)
	ejecucion = comparar(huff, arbolBase, overflow, archivo)
	if ejecucion:
		print(f"\n{archivo} descomprimido con éxito")
		return
	print("\narchivos inválidos")


if __name__ == "__main__":
	main()
