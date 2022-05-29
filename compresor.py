import sys


def recibirFrecuencias(archivo):
	archivo = open(archivo, "rb").read()
	frecuencias = [0]*256
	for i in archivo:
		frecuencias[i] += 1
	return frecuencias, archivo


def insertar(valores, byte, frecuencia):
	inf = 0
	sup = len(valores)
	if not sup:
		valores.append([byte, frecuencia])
		return
	mid = (inf + sup) >> 1
	while inf != mid:
		if valores[mid][1] >= frecuencia:
			inf = mid
		elif valores[mid][1] < frecuencia:
			sup = mid
		mid = (inf + sup) >> 1
	if valores[mid][1] > frecuencia:
		valores.insert(sup, [byte, frecuencia])
		return
	valores.insert(mid, [byte, frecuencia])


def ordenarFrecuencias(frecuencias):
	valores = []
	for i in range(len(frecuencias)):
		if frecuencias[i]:
			insertar(valores, [i, [], []], frecuencias[i])
	return valores


def altura(arbol):
    if arbol:
        return max(altura(arbol[1]), altura(arbol[2])) + 1
    return -1


def nivel(arbol, n):
    if arbol:
        if n != 0:
            return nivel(arbol[1], n - 1) + nivel(arbol[2], n - 1)
        return [arbol[0]]
    return []


def anchura(arbol):
    max_anchura = -1
    for nivelActual in range(altura(arbol) + 1):
        cardinalidadNivel = len(nivel(arbol, nivelActual))
        max_anchura = max(max_anchura, cardinalidadNivel)
    return max_anchura


def recorrerHuffman(arbol, asociaciones, niveles, alturaActual = 0, padre = 1):
    niveles[alturaActual] += 1
    if arbol[1] or arbol[2]:
        if arbol[1]:
            recorrerHuffman(arbol[1], asociaciones, niveles, alturaActual + 1, padre << 1)
        if arbol[2]:
            recorrerHuffman(arbol[2], asociaciones, niveles, alturaActual + 1, (padre << 1) | 1)
        return
    asociaciones[arbol[0]] = padre


def crearArbol(relaciones):
	while len(relaciones) > 1:
		menor1 = relaciones.pop()
		menor2 = relaciones.pop()
		sumaMenores = menor1[1] + menor2[1]
		insertar(relaciones, [sumaMenores, menor1[0], menor2[0]], sumaMenores)
	asociaciones = [0]*256
	alt = altura(relaciones[0][0])
	niveles = [0]*(alt + 1)
	ancho = anchura(relaciones[0][0])
	recorrerHuffman(relaciones[0][0], asociaciones, niveles)
	return asociaciones, alt, ancho, niveles


def CMP(msk, i):
	return msk >= 1 << i


def lenBits(bits):
	i = 1
	while CMP(bits, i + 1):
		i += 1
	return i


def main():
	argumentos = sys.argv[1:]
	frecuencias, archivo = recibirFrecuencias(argumentos[0])
	relaciones = ordenarFrecuencias(frecuencias)
	asociaciones, altura, anchura, npn = crearArbol(relaciones.copy())
	buffer = 1
	lenbuffer = 0
	overflow = 0
	MSK = (1 << 8) - 1
	with open(argumentos[0] + ".huff", "wb") as guardar:
		for i in archivo:
			lencod = lenBits(asociaciones[i])
			if lencod + lenbuffer <= 8:
				buffer = (buffer << lencod) | (asociaciones[i] ^ (1 << (lencod)))
				lenbuffer += lencod
			else:
				buffer = (buffer << (8 - lenbuffer)) | ((asociaciones[i] ^ (1 << (lencod))) >> (lencod + lenbuffer - 8))
				guardar.write(bytes([buffer ^ (1 << 8)]))
				lenbuffer = lencod + lenbuffer - 8
				buffer = (asociaciones[i] ^ (1 << (lencod))) & ((1 << lenbuffer) - 1) | (1 << lenbuffer)
				while lenbuffer >= 8:
					subbuffer = (buffer & ((1 << lenbuffer) - 1)) >> (lenbuffer - 8)
					guardar.write(bytes([subbuffer]))
					lenbuffer -= 8
				buffer &= (1 << lenbuffer) - 1
				buffer |= (1 << lenbuffer)
		if lenbuffer:
			overflow = 8 - lenbuffer
			guardar.write(bytes([(buffer << overflow) ^ (1 << 8)]))
	with open(argumentos[0] + ".table", "wb") as guardar:
		guardar.write(bytes([overflow]))
		for i in range(len(asociaciones)):
			if asociaciones[i]:
				longitud = lenBits(asociaciones[i])
				guardar.write(bytes([i, longitud]))
				while longitud > 8:
					guardar.write(bytes([(asociaciones[i] >> (longitud - 8)) & MSK]))
					longitud -= 8
				guardar.write(bytes([(asociaciones[i] & ((1 << longitud) - 1)) << (8 - longitud)]))
	with open(argumentos[0] + ".stats", "w") as guardar:
		guardar.write(f"altura:{altura}\n")
		guardar.write(f"anchura:{anchura}\n")
		guardar.write(f"nodos_por_nivel:{altura}\n")
		for i in range(len(npn)):
			guardar.write(f"{i}:{npn[i]}\n")
		guardar.write(f"frecuencias:{len(relaciones)}\n")
		for i in range(len(relaciones)):
			guardar.write(f"{i}:{relaciones[i][0][0]}:{relaciones[i][1]}\n")
	print(f"{argumentos[0]}.huff {argumentos[0]}.table {argumentos[0]}.stats creados exitosamente")


if __name__ == "__main__":
	main()
