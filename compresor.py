# Explicación: Para recibir los argumentos de ejecución.
import sys


# Explicación: Determina los bytes presentes en un archivo y sus
# - respectivas frecuencias.
# Dominio: Un String representativo del nombre del archivo.
# Codominio: Una lista de 256 valores naturales y los bytes presentes
# - en el archivo.
def recibirFrecuencias(archivo):
	archivo = open(archivo, "rb").read()
	frecuencias = [0]*256
	for i in archivo:
		frecuencias[i] += 1
	return frecuencias, archivo


# Explicación: Inserta con búsqueda binaria el par objeto y su
# - frecuencia relativa dentro de la lista.
# Dominio: La lista de referencia, un objeto y la frecuencia de este.
# Codominio: Vacío (cambia la lista en sí).
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


# Explicación: Ordena las frecuencias y sus repspectivos bytes con
# - Binary Insertion Sort.
# Dominio: Una lista de 256 valores naturales.
# Codominio: Una lista de listas ordenada de mayor a menor.
def ordenarFrecuencias(frecuencias):
	valores = []
	for i in range(len(frecuencias)):
		if frecuencias[i]:
			insertar(valores, [i, [], []], frecuencias[i])
	return valores


# Explicación: Determina la altura de un árbol.
# Dominio: El árbol en forma de [nodo, [...], [...]].
# Codominio: Un valor entero representativo de la altura.
def altura(arbol):
	if arbol:
		return max(altura(arbol[1]), altura(arbol[2])) + 1
	return -1


# Explicación: Determina los elementos de un nivel en el árbol.
# Dominio: Un árbol y los elementos en el nivel de interés.
# Codominio: Una lista con nodos del árbol..
def nivel(arbol, n):
	if arbol:
		if n != 0:
			return nivel(arbol[1], n - 1) + nivel(arbol[2], n - 1)
		return [arbol[0]]
	return []


# Explicación: Determina la anchura de un árbol.
# Dominio: El árbol en forma de [nodo, [...], [...]].
# Codominio: La máxima anchura.
def anchura(arbol):
	max_anchura = -1
	for nivelActual in range(altura(arbol) + 1):
		cardinalidadNivel = len(nivel(arbol, nivelActual))
		max_anchura = max(max_anchura, cardinalidadNivel)
	return max_anchura


# Explicación: Determina los códigos representativos del árbol y sus hojas.
# Dominio: El árbol, los códigos guardados, los niveles guardados, 
# - la altura actual y el código.
# Codominio: Vacío (edita las listas respectivas).
def recorrerHuffman(arbol, asociaciones, niveles, alturaActual = 0, codigo = 1):
	niveles[alturaActual] += 1
	if arbol[1] or arbol[2]:
		if arbol[1]:
			recorrerHuffman(arbol[1], asociaciones, niveles, alturaActual + 1, codigo << 1)
		if arbol[2]:
			recorrerHuffman(arbol[2], asociaciones, niveles, alturaActual + 1, codigo << 1 | 1)
		return
	asociaciones[arbol[0]] = codigo


# Explicación: Crea el árbol de Huffman a partir de las frecuencias
# - de los bytes.
# Dominio: Una lista ordenada de mayor a menor frecuencias con los
# - respectivos bytes.
# Codominio: Una asociación entre cada byte encontrado y un código,
# - la altura del árbol, su ancho y los niveles de las hojas.
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


# Explicación: Determina si una máscara tiene longitud mayor a una
# - longitud.
# Dominio: Una máscara de bits y un natural i.
# Codominio: Un valor booleano.
def CMP(msk, i):
	return msk >= 1 << i


# Explicación: Determina la longitud de una máscara de bits.
# Dominio: Una máscara de bits.
# Codominio: Un valor natural.
def lenBits(bits):
	i = 1
	while CMP(bits, i + 1):
		i += 1
	return i


# Explicación: Determina la longitud de cada código.
# Dominio: Los códigos.
# Codominio: Una lista con las longitudes de cada código.
def crearLongitudes(asociaciones):
	longitudes = [0]*256
	for i in range(len(asociaciones)):
		longitudes[i] = lenBits(asociaciones[i])
		asociaciones[i] ^= 1 << longitudes[i]
	return longitudes


# Explicación: Muestra el progreso de la compresión.
# Dominio: Lo hecho y el total necesario.
# Codominio: Vacío (imprima el progreso en porcentaje a la pantalla).
# NOTA: Este código solo existe como defecto, nunca es activado.
def restante(hecho, total):
	print(f"\r  -> {hecho + 1}÷{total} => {100*(hecho + 1)/total:.2f}%", end = "\r")


# Explicación: Reemplaza cada byte por su código y lo guarda
# - en un nuevo archivo.
# Dominio: La ubicación del archivo, los contenidos, las asociaciones y
# - las longitudes.
# Codominio: Guarda el archivo comprimido y el overflow en términos de bits.
def guardarHUFF(ubic, archivo, asociaciones, longitudes, buffer = 0, lenbuffer = 0, overflow = 0):
	with open(ubic + ".huff", "wb") as guardar:
			for j in range(len(archivo)):
				# Manipulación de bits mágico.
				i = archivo[j]
				lencod = longitudes[i]
				asociacion = asociaciones[i]
				if lencod + lenbuffer <= 8:
					# Si la serie de bits (el código) cabe en el bytebuffer
					# - sin un overflow, se agrega.
					buffer = buffer << lencod | asociacion
					lenbuffer += lencod
				else:
					# Si la serie de bits no cabe en el bytebuffer,
					# - se agrega lo que se puede sin hacer un
					# - un overflow, y el resto se guarda.
					lenbuffer = lencod + lenbuffer - 8
					buffer = buffer << (lencod - lenbuffer) | (asociacion >> lenbuffer)
					guardar.write(bytes([buffer]))
					buffer = asociacion & ((1 << lenbuffer) - 1)
					while lenbuffer >= 8:
						subbuffer = (buffer & ((1 << lenbuffer) - 1)) >> (lenbuffer - 8)
						guardar.write(bytes([subbuffer]))
						lenbuffer -= 8
					buffer &= (1 << lenbuffer) - 1
				# Código para mostrar el progreso.
				#restante(j, len(archivo))
			if lenbuffer:
				overflow = 8 - lenbuffer
				guardar.write(bytes([buffer << overflow]))
	# Código para mostrar el progreso.
	#print()
	return overflow


# Explicación: Guarda el árbol de Huffman.
# Dominio: La ubicación del archivo, los contenidos, las asociaciones y
# - las longitudes.
# Codominio: Vacío (guarda el árbol de Huffman).
def guardarTABLE(ubic, overflow, asociaciones, longitudes):
	MSK = (1 << 8) - 1
	with open(ubic + ".table", "wb") as guardar:
		guardar.write(bytes([overflow]))
		for i in range(len(asociaciones)):
			if longitudes[i]:
				longitud = longitudes[i]
				guardar.write(bytes([i, longitud]))
				while longitud > 8:
					guardar.write(bytes([(asociaciones[i] >> (longitud - 8)) & MSK]))
					longitud -= 8
				guardar.write(bytes([(asociaciones[i] & ((1 << longitud) - 1)) << (8 - longitud)]))


# Explicación: Comprime un archivo en un parámetros.
# Dominio: 
# Codominio: Vacío (imprime si se logró la compresión y los
# - tres archivos de interés: ".huff", ".table" y ".stats").
def main():
	argumentos = sys.argv[1:]
	frecuencias, archivo = recibirFrecuencias(argumentos[0])
	relaciones = ordenarFrecuencias(frecuencias)
	asociaciones, altura, anchura, npn = crearArbol(relaciones.copy())
	longitudes = crearLongitudes(asociaciones)
	overflow = guardarHUFF(argumentos[0], archivo, asociaciones, longitudes)
	guardarTABLE(argumentos[0], overflow, asociaciones, longitudes)
	# Guarda las estadísticas.
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


# Explicación: Activación.
if __name__ == "__main__":
	main()
