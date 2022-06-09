# Explicación: Para recibir los argumentos de ejecución.
import sys


# Explicación: Reconstruya un árbol de Huffman a partir de un código
# - de bits correlacionado con un byte.
# Dominio: El árbol actual, el código, la longitud del código y
# - el byte.
# Codominio: Vacío (contruya el árbol). 
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
	if codigo & 1 << (lencodigo - 1):
		return reconstruirArbol(ArbolBase[2], codigo, lencodigo - 1, byte)
	return reconstruirArbol(ArbolBase[1], codigo, lencodigo - 1, byte)


# Explicación: Crea el árbol de Huffman a partir de un stream de
# - bytes.
# Dominio: Un stream de bytes.
# Codominio: El árbol de Huffman.
def crearArbol(arbol):
	overflow = arbol[0]
	arbolBase = [0, [], []]
	i = 1
	while i < len(arbol):
		valor = arbol[i]
		i += 1
		lencod = arbol[i]
		lencodNOCHANGE = arbol[i]
		i += 1
		codigo = 0
		while lencod > 8:
			codigo = codigo << 8 | arbol[i]
			lencod -= 8
			i += 1
		codigo = codigo << lencod | (arbol[i] >> (8 - lencod))
		i += 1
		reconstruirArbol(arbolBase, codigo, lencodNOCHANGE, valor)
	return arbolBase, overflow


# Explicación: Muestra el progreso de la compresión.
# Dominio: Lo hecho y el total necesario.
# Codominio: Vacío (imprima el progreso en porcentaje a la pantalla).
# NOTA: Este código solo existe como defecto, nunca es activado.
def restante(hecho, total):
	print(f"\r  -> {hecho}÷{total} => {100*hecho/total:.2f}%", end = "\r")


# Explicación: Encuentra el siguiente bit en una serie de bytes.
# Dominio: El stream de bytes, el bit overflow, el pointer del
# - byte en el byte stream y el pointer del bit en el byte.
# Codominio: El bit, el nuevo pointer de byte y el nuevo pointer
# - del bit.
def nextBit(huff, overflow, bytebuffer, bitbuffer):
	# Código para mostrar el progreso.
	#if bitbuffer == -1:
	#	restante(bytebuffer, len(huff))
	bytebuffer += bitbuffer == -1
	bitbuffer += (bitbuffer == -1) << 3
	if bytebuffer != len(huff) and (bytebuffer != len(huff) - 1 or overflow != bitbuffer + 1):
		return huff[bytebuffer] & 1 << bitbuffer > 0, bytebuffer, bitbuffer - 1
	return -1, bytebuffer, bitbuffer


# Explicación: Descomprime un archivo a partir del árbol de referencia
# - y el stream de bits caracterizado por el archivo.
# Dominio: Una lista de bytes, el árbol binario en forma de [nodo, [...], [...]],
# - el overflow y el lugar archivo donde se guarda la respuesta.
# Codominio: Retorne 1 si fue un éxito y 0 si hubo un error (guarda
# - el archivo descomprimido).
def comparar(huff, arbol, overflow, archivo):
	bytebuffer, bitbuffer = 0, 7
	subarbol = arbol
	bit, bytebuffer, bitbuffer = nextBit(huff, overflow, bytebuffer, bitbuffer)
	with open(archivo, "wb") as guardar:
		while bit != -1:
			subarbol = subarbol[1 + bit]
			if not subarbol[1] and not subarbol[2]:
				guardar.write(bytes([subarbol[0]]))
				subarbol = arbol
			bit, bytebuffer, bitbuffer = nextBit(huff, overflow, bytebuffer, bitbuffer)
	return subarbol == arbol


# Explicación: Descomprime un archivo a partir de los tres archivos
# - establecidos en los parámetros de activación.
# Dominio: Vacío (recibe los parárametros de la función).
# Codominio: Vacío (guarda el resultado en un archivo).
def main():
	argumentos = sys.argv[1:]
	huff, arbol, archivo = argumentos
	huff, arbol = open(huff, "rb").read(), open(arbol, "rb").read()
	try:
		arbolBase, overflow = crearArbol(arbol)
		ejecucion = comparar(huff, arbolBase, overflow, archivo)
		# Código para mostrar el progreso.
		#print()
		if ejecucion:
			print(f"{archivo} descomprimido con éxito")
			return
	except IndexError as e:
		pass
	print("archivos inválidos")


# Explicación: Activación.
if __name__ == "__main__":
	main()