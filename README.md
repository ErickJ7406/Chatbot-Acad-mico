# 📚 Chatbot Académico con Búsqueda Semántica

Este proyecto es un chatbot inteligente diseñado para responder preguntas sobre un libro de texto específico ("Introducción a la Inteligencia Artificial") utilizando técnicas avanzadas de Procesamiento de Lenguaje Natural (PLN).

En lugar de una simple búsqueda por palabras clave, el chatbot comprende el significado semántico de las preguntas y encuentra los fragmentos más relevantes del libro, proporcionando respuestas coherentes y contextualizadas.

![Captura de Pantalla del Chatbot](![image](https://github.com/user-attachments/assets/6623b192-3d00-4a1f-9a53-8042cc3c624d)
)

---

## ✨ Características Principales

- **Búsqueda Semántica Avanzada:** Utiliza `sentence-transformers` para generar embeddings vectoriales y `FAISS` (de Facebook AI) para realizar búsquedas de similitud ultrarrápidas.
- **Interfaz de Usuario Interactiva:** Construido con `Streamlit` para ofrecer una experiencia de chat amigable y en tiempo real.
- **Historial de Conversación:** Guarda el contexto de la sesión, permitiendo una interacción más natural.
- **Procesamiento de PDF:** Extrae automáticamente el texto de un documento PDF para construir su base de conocimiento.
- **Lógica de Relevancia:** Filtra y presenta solo los resultados que superan un umbral de similitud, asegurando respuestas de calidad.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.8+
- **Interfaz:** Streamlit
- **PLN / Embeddings:** Sentence-Transformers
- **Búsqueda Vectorial:** FAISS (CPU)
- **Extracción de PDF:** PDFMiner.six

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### Paso 1: Clonar el Repositorio

Primero, clona este repositorio en tu máquina:
```bash
git clone <URL_DEL_REPOSITORIO>
cd AsistenteIA
```

### Paso 2: Crear y Activar un Entorno Virtual

Es muy recomendable trabajar en un entorno virtual para aislar las dependencias del proyecto.

```bash
# Crear el entorno
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

Instala todas las librerías necesarias usando el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Paso 4: Preparar los Datos (¡Paso Crucial!)

El chatbot necesita procesar tu libro para poder responder preguntas sobre él.

1.  **Coloca tu libro en PDF** dentro de la carpeta `data/`. El proyecto asume que el archivo se llama `FUNDAMENTO+DE+LA+IA+volumen+I.pdf`. Si tu archivo tiene otro nombre, deberás actualizarlo en `extractor.py`.

2.  **Genera los archivos de conocimiento**. Ejecuta el siguiente script para extraer el texto, dividirlo en fragmentos y crear los embeddings y el índice FAISS. Este proceso solo necesita hacerse una vez (o cada vez que cambies el libro).

    ```bash
    python embeddings.py
    ```

    Al finalizar, deberías ver nuevos archivos en tu carpeta `data/`, incluyendo `faiss.index` y `embeddings.pkl`.

### Paso 5: Ejecutar el Chatbot

¡Todo está listo! Lanza la aplicación de Streamlit con el siguiente comando:

```bash
streamlit run app.py
```

Se abrirá una nueva pestaña en tu navegador con la interfaz del chatbot, lista para que empieces a hacer preguntas.

---

## 📂 Estructura del Proyecto

```
.AsistenteIA/
├── data/
│   ├── FUNDAMENTO+DE+LA+IA+volumen+I.pdf  # El libro base
│   ├── chunks.txt                       # Texto del libro dividido en fragmentos
│   ├── embeddings.pkl                   # Vectores de los fragmentos
│   └── faiss.index                      # Índice para búsqueda rápida
├── venv/                                # Entorno virtual
├── app.py                             # Lógica de la interfaz con Streamlit
├── chunker.py                         # Script para dividir el texto
├── embeddings.py                      # Script para generar embeddings e índice FAISS
├── extractor.py                       # Script para extraer texto del PDF
├── search_engine.py                   # Clase principal del motor de búsqueda semántica
├── requirements.txt                   # Lista de dependencias de Python
└── README.md                          # Este archivo
```
