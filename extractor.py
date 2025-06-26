from pdfminer.high_level import extract_text

def extraer_texto_pdf(ruta_pdf):
    texto = extract_text(ruta_pdf)
    return texto

if __name__ == "__main__":
    ruta = "data/FUNDAMENTO+DE+LA+IA+volumen+I.pdf"
    texto = extraer_texto_pdf(ruta)

    with open("data/FUNDAMENTO+DE+LA+IA+volumen+I_extraido.txt", "w", encoding="utf-8") as archivo_salida:
        archivo_salida.write(texto)

    print("✅ Texto extraído y guardado en 'data/FUNDAMENTO+DE+LA+IA+volumen+I_extraido.txt'")
