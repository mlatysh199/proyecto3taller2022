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


def nextBit(huff, overflow, bufferx, buffery):
	if buffery == -1:
		buffery = 7
		bufferx += 1
	if bufferx == len(huff) or (bufferx == len(huff) - 1 and overflow == buffery + 1):
		return -1, buffery, bufferx
	return huff[bufferx] & (1 << buffery) > 0, bufferx, buffery - 1


# Retorna -1 si lo alcanza.
def recorrerArbol(ArbolBase, codigo, lencodigo, respuesta):
	if not (ArbolBase[1] or ArbolBase[2]):
		if not lencodigo: 
			respuesta.append(ArbolBase[0])
			return -1
		return -2
	if not lencodigo:
		return
	if codigo & (1 << (lencodigo - 1)):
		return recorrerArbol(ArbolBase[2], codigo, lencodigo - 1, respuesta)
	return recorrerArbol(ArbolBase[1], codigo, lencodigo - 1, respuesta)


def comparar(huff, arbol, overflow):
	buffer = 1
	lenbuffer = 0
	bufferx, buffery = 0, 7
	respuesta = []
	bit, bufferx, buffery = nextBit(huff, overflow, bufferx, buffery)
	while bit != -1:
		buffer <<= 1
		buffer |= bit
		lenbuffer += 1
		intento = recorrerArbol(arbol, buffer, lenbuffer, respuesta)
		if intento == -2:
			return []
		if intento == -1:
			buffer = 1
			lenbuffer = 0
		bit, bufferx, buffery = nextBit(huff, overflow, bufferx, buffery)
	return respuesta*(not lenbuffer)


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
	salida = comparar(huff, arbolBase, overflow)
	if salida:
		with open(archivo, "wb") as guardar:
			guardar.write(bytes(salida))
		print(f"{archivo} descomprimido con éxito")
		return
	print("archivos inválidos")
	return


if __name__ == "__main__":
	main()
