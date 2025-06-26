import pickle
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def cargar_chunks(ruta_chunks, min_longitud=50):
    """
    Lee los chunks desde un archivo de texto y filtra los muy cortos.
    Devuelve una lista de tuplas (id_chunk, texto_chunk).
    """
    with open(ruta_chunks, "r", encoding="utf-8") as f:
        contenido = f.read()

    chunks_con_id = []
    for chunk_bloque in contenido.split('--- CHUNK '):
        if chunk_bloque.strip():
            partes = chunk_bloque.split('\n', 1)
            if len(partes) > 1:
                try:
                    # El ID es el número después de '--- CHUNK '
                    id_chunk = int(partes[0].split('---')[0].strip())
                    texto = partes[1].strip()
                    if len(texto) >= min_longitud:
                        chunks_con_id.append((id_chunk, texto))
                except (ValueError, IndexError):
                    # Ignorar bloques que no tengan un formato de ID numérico válido
                    continue
    return chunks_con_id

def generar_embeddings(chunks_texto, modelo_nombre="all-MiniLM-L6-v2"):
    """
    Usa SentenceTransformer para generar embeddings de los textos de los chunks.
    """
    modelo = SentenceTransformer(modelo_nombre)
    embeddings = modelo.encode(chunks_texto, show_progress_bar=True)
    return embeddings

def guardar_embeddings(embeddings, chunks_con_id, ruta_salida):
    """
    Guarda embeddings y chunks (con ID) como una lista de tuplas.
    Formato: (embedding, (id_chunk, texto_chunk))
    """
    data = list(zip(embeddings, chunks_con_id))
    with open(ruta_salida, "wb") as f:
        pickle.dump(data, f)


def construir_indice_faiss(embeddings_np):
    """
    Construye un índice FAISS usando similitud coseno (normalizando los vectores).
    """
    faiss.normalize_L2(embeddings_np)
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner Product ≈ Cosine similarity
    index.add(embeddings_np)
    return index

def guardar_indice(index, ruta_index):
    """
    Guarda el índice FAISS en disco.
    """
    faiss.write_index(index, ruta_index)

if __name__ == "__main__":
    ruta_chunks = "data/chunks.txt"
    ruta_embeddings = "data/embeddings.pkl"
    ruta_index_faiss = "data/faiss.index"

    # Paso 1: cargar chunks con sus IDs
    chunks_con_id = cargar_chunks(ruta_chunks, min_longitud=50)
    print(f"📦 Cargando {len(chunks_con_id)} chunks válidos...")

    # Extraer solo el texto para generar los embeddings
    chunks_texto = [chunk[1] for chunk in chunks_con_id]

    # Paso 2: generar embeddings
    embeddings = generar_embeddings(chunks_texto)

    # Paso 3: guardar embeddings y chunks (con ID)
    guardar_embeddings(embeddings, chunks_con_id, ruta_embeddings)
    print(f"✅ Embeddings guardados en '{ruta_embeddings}'")

    # Paso 4: crear índice FAISS
    embeddings_np = np.array(embeddings)
    index = construir_indice_faiss(embeddings_np)
    guardar_indice(index, ruta_index_faiss)
    print(f"✅ Índice FAISS guardado en '{ruta_index_faiss}'")

    print("🚀 Todo listo. Puedes ahora hacer búsquedas semánticas con FAISS.")