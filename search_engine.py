import faiss
import pickle
import re
import numpy as np
from sentence_transformers import SentenceTransformer

class BuscadorSemantico:
    def __init__(self, ruta_index="data/faiss.index", ruta_chunks="data/embeddings.pkl",
                 modelo_nombre="all-MiniLM-L6-v2", top_k=3, umbral_similitud=0.65):
        """
        Inicializa el buscador semántico con FAISS y el modelo de embeddings.
        """
        self.modelo = SentenceTransformer(modelo_nombre)
        self.index = faiss.read_index(ruta_index)
        self.top_k = top_k
        self.umbral = umbral_similitud
        # Carga los chunks con su ID: [(id, texto), ...]
        self.chunks_con_id = self._cargar_chunks_con_id(ruta_chunks)

    def _cargar_chunks_con_id(self, ruta):
        """
        Carga los datos de los chunks (id, texto) desde embeddings.pkl.
        """
        with open(ruta, "rb") as f:
            data = pickle.load(f)
        # El pkl guarda (embedding, (id, texto)), extraemos solo (id, texto)
        return [chunk_info for _, chunk_info in data]

    def buscar(self, pregunta):
        """
        Devuelve los chunks más relevantes a una pregunta, incluyendo su ID.
        """
        pregunta_limpia = limpiar_puntuacion(pregunta)
        embedding = self.modelo.encode([pregunta_limpia])
        faiss.normalize_L2(embedding)
        D, I = self.index.search(embedding, self.top_k)

        resultados = []
        usados = set()
        for sim, idx in zip(D[0], I[0]):
            if sim >= self.umbral and idx not in usados:
                # Obtenemos el ID y el texto del chunk
                id_chunk, texto_chunk = self.chunks_con_id[idx]
                if texto_chunk and len(texto_chunk.split()) > 10:
                    resultados.append({
                        "id": id_chunk,
                        "chunk": texto_chunk.strip(),
                        "similitud": round(sim, 3)
                    })
                    usados.add(idx)

        if not resultados:
            return [{
                "id": None,
                "chunk": "🤖 Lo siento, no encontré información relevante sobre eso en el libro.",
                "similitud": 0.0
            }]

        return resultados

def limpiar_puntuacion(texto):
    # Lista de palabras vacías comunes en español
    palabras_vacias = [
        'a', 'un', 'una', 'unas', 'unos', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde',
        'durante', 'e', 'el', 'ella', 'ellas', 'ellos', 'en', 'entre', 'esa', 'esas', 'ese',
        'eso', 'esos', 'esta', 'estas', 'este', 'esto', 'estos', 'hasta', 'la', 'las', 'le',
        'les', 'lo', 'los', 'mas', 'me', 'mi', 'mis', 'muy', 'o', 'para', 'pero', 'por',
        'porque', 'que', 'qué', 'se', 'sin', 'sobre', 'su', 'sus', 'te', 'tu', 'tus', 'y', 'ya',
        'como', 'cual', 'cuales', 'cuando', 'donde', 'es', 'eres', 'somos', 'son'
    ]
    
    # Convertir a minúsculas y eliminar puntuación
    texto_limpio = texto.lower()
    texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio, flags=re.UNICODE)
    
    # Eliminar palabras vacías
    palabras = texto_limpio.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_vacias]
    
    return ' '.join(palabras_filtradas)