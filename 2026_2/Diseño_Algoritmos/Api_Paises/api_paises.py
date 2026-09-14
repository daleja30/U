# Importar la biblioteca para realizar peticiones a APIs
import requests

# Importar Flask y las funciones necesarias
from flask import Flask, render_template, request


# Crear la aplicación Flask
app = Flask(__name__)


# ==========================================================
# OBTENER PAÍSES DE EUROPA
# ==========================================================

def obtener_paises():

    # URL de la API para obtener los países de Europa
    url = "https://countries.dev/region/Europe"

    try:

        # Realizar petición a la API
        respuesta = requests.get(url, timeout=10)

        # Verificar que la petición fue exitosa
        respuesta.raise_for_status()

        # Convertir la respuesta a formato JSON
        datos = respuesta.json()

        # Crear lista vacía para almacenar los países
        paises = []

        # Recorrer los países recibidos
        for p in datos:

            # Crear un diccionario con la información
            # que necesitamos para la página principal
            pais = {
                "nombre": p.get("name", "Sin nombre"),
                "codigo": p.get("alpha3Code", ""),
                "googleMaps": p.get("maps", {}).get("googleMaps", "")
            }

            # Agregar el país a la lista
            paises.append(pais)

        # Ordenar los países alfabéticamente
        paises = sorted(
            paises,
            key=lambda x: x["nombre"].lower()
        )

        # Retornar la lista ordenada
        return paises

    # Capturar errores de conexión
    except requests.exceptions.RequestException as e:

        # Mostrar el error en la terminal
        print(f"Error de conexión con la API: {e}")

        # Retornar lista vacía
        return []

    # Capturar otros errores
    except Exception as e:

        # Mostrar el error en la terminal
        print(f"Error procesando los datos: {e}")

        # Retornar lista vacía
        return []


# ==========================================================
# OBTENER INFORMACIÓN COMPLETA DE UN PAÍS
# ==========================================================

def obtener_pais(codigo):

    # Crear la URL para consultar un país específico
    url = f"https://countries.dev/alpha/{codigo}?full=true"

    try:

        # Realizar petición a la API
        respuesta = requests.get(url, timeout=10)

        # Verificar que la petición fue exitosa
        respuesta.raise_for_status()

        # Convertir la respuesta JSON
        pais = respuesta.json()

        # Retornar la información del país
        return pais

    # Capturar errores de conexión
    except requests.exceptions.RequestException as e:

        # Mostrar el error en la terminal
        print(f"Error consultando el país: {e}")

        # Retornar None
        return None

    # Capturar otros errores
    except Exception as e:

        # Mostrar el error
        print(f"Error procesando el país: {e}")

        # Retornar None
        return None


# ==========================================================
# BÚSQUEDA BINARIA
# ==========================================================

def busqueda_binaria(lista, objetivo):

    # Posición inicial
    izquierda = 0

    # Posición final
    derecha = len(lista) - 1

    # Repetir mientras exista un rango de búsqueda
    while izquierda <= derecha:

        # Calcular la posición central
        medio = (izquierda + derecha) // 2

        # Obtener el nombre del país central
        nombre_medio = lista[medio]["nombre"].lower()

        # Convertir el objetivo a minúsculas
        objetivo_minuscula = objetivo.lower()

        # Verificar si encontramos el país
        if nombre_medio == objetivo_minuscula:

            # Retornar el país
            return lista[medio]

        # Si el país buscado está después
        elif nombre_medio < objetivo_minuscula:

            # Buscar en la mitad derecha
            izquierda = medio + 1

        # Si el país buscado está antes
        else:

            # Buscar en la mitad izquierda
            derecha = medio - 1

    # No se encontró el país
    return None


# ==========================================================
# PÁGINA PRINCIPAL
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    # Obtener los países de Europa
    paises = obtener_paises()

    # Inicializar resultado
    resultado = None

    # Verificar si se realizó una búsqueda
    if request.method == "POST":

        # Obtener el nombre escrito
        nombre_buscar = request.form.get("pais", "").strip()

        # Verificar que no esté vacío
        if nombre_buscar:

            # Ejecutar búsqueda binaria
            resultado = busqueda_binaria(
                paises,
                nombre_buscar
            )

    # Mostrar la página principal
    return render_template(
        "index.html",
        paises=paises,
        resultado=resultado
    )


# ==========================================================
# DETALLE DE UN PAÍS
# ==========================================================

@app.route("/pais/<codigo>")
def detalle_pais(codigo):

    # Consultar la información completa
    # directamente en la API
    pais = obtener_pais(codigo)

    # Verificar si encontramos el país
    if pais is None:

        # Mostrar mensaje de error
        return "No se pudo encontrar el país", 404

    # Enviar la información al HTML
    return render_template(
        "detalle_pais.html",
        pais=pais
    )


# ==========================================================
# EJECUTAR LA APLICACIÓN
# ==========================================================

if __name__ == "__main__":

    # Iniciar Flask
    app.run(debug=True)