import os
import re

def cargar_texto(ruta_txt):
    """
    Lee el contenido del archivo de texto plano.
    """
    with open(ruta_txt, "r", encoding="utf-8") as f:
        return f.read()

def dividir_en_oraciones(texto):
    # Divide el texto en oraciones usando regex (puedes mejorar el patrón según el idioma)
    oraciones = re.split(r'(?<=[.!?])\s+', texto)
    return [o.strip() for o in oraciones if o.strip()]

def chunkear_texto(texto, max_caracteres=500, overlap=1):
    """
    Divide el texto en chunks de máximo 'max_caracteres', sin cortar oraciones.
    overlap: número de oraciones que se repiten entre chunks para mantener contexto.
    """
    oraciones = dividir_en_oraciones(texto)
    chunks = []
    chunk_actual = []

    for oracion in oraciones:
        if sum(len(o) for o in chunk_actual) + len(oracion) + len(chunk_actual) <= max_caracteres:
            chunk_actual.append(oracion)
        else:
            if chunk_actual:
                chunks.append(' '.join(chunk_actual))
            # Solapamiento: toma las últimas 'overlap' oraciones para el siguiente chunk
            chunk_actual = chunk_actual[-overlap:] if overlap > 0 else []
            chunk_actual.append(oracion)

    if chunk_actual:
        chunks.append(' '.join(chunk_actual))

    return chunks

def guardar_chunks(chunks, ruta_salida):
    """
    Guarda los chunks en un archivo de texto, cada uno separado por líneas.
    """
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- CHUNK {i+1} ---\n{chunk}\n\n")

if __name__ == "__main__":
    ruta_txt = "data/FUNDAMENTO+DE+LA+IA+volumen+I_extraido.txt"
    texto = cargar_texto(ruta_txt)
    chunks = chunkear_texto(texto, max_caracteres=500, overlap=1)
    guardar_chunks(chunks, "data/chunks.txt")
    print(f"✅ Se generaron {len(chunks)} chunks y se guardaron en 'data/chunks.txt'")
