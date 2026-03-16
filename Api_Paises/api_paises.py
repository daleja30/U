# Importar las herramientas necesarias
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def obtener_paises():
    url = "https://restcountries.com/v3.1/region/europe"

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()

        paises = []

        for p in respuesta.json():
            pais = {
                "nombre": p['name']['common'],
                "googleMaps": p['maps']['googleMaps']
            }
            paises.append(pais)

        # ordenar países alfabéticamente
        paises = sorted(paises, key=lambda x: x['nombre']) #Si la función cabe en una línea → lambda // Si crece o se reutiliza → def
        return paises

    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return []

# -------- BUSQUEDA BINARIA --------
def busqueda_binaria(lista, objetivo):
    izquierda = 0
    derecha = len(lista) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        nombre_medio = lista[medio]['nombre'].lower()

        if nombre_medio == objetivo.lower():
            return lista[medio]

        elif nombre_medio < objetivo.lower():
            izquierda = medio + 1

        else:
            derecha = medio - 1

    return None
# ----------------------------------

@app.route("/", methods=["GET","POST"])
def index():
    paises = obtener_paises()
    resultado = None

    if request.method == "POST":
        nombre_buscar = request.form["pais"]
        resultado = busqueda_binaria(paises, nombre_buscar)

    return render_template("index.html", paises=paises, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)