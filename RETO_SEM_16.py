# RETO DE SEMANA 16. Consulta a la API de OpenWeather
# El programa es un consultor del clima con los siguientes requerimientos:
# Debe consultar el clima de la ciudad o la latitud y la longitud que ingrese usuario.
# ● Para ello, se debe preguntar primero al usuario las
# coordenadas o el nombre de la ciudad, en el siguiente formato:
# "CIUDAD, SIGLAS_DEL_PAÍS".
# ● Solicitar al usuario su API key de OpenWeather.
# ● Si el usuario introduce mal los datos, el programa debe indicar qué dato es el
# incorrecto.
# ● Los posibles errores deben estar cubiertos por un try/except.
# ● Si la API no encuentra la ciudad, se debe indicar al usuario con un mensaje.
# ● Al final, si todo salió bien, debe mostrar un mensaje como el siguiente ejemplo:
# “El clima en Mexico City es muy nuboso”.
# ● En caso de que el usuario ingrese las coordenadas incorrectas, debe incluir 
# una sugerencia de buscar o verificar las coordenadas en la 
# página https://www.coordenadas-gps.com/

import requests

def solicitar_entrada(prompt, validador, mensaje_error):
    """Solicita una entrada al usuario con validación y opción de corrección."""
    while True:
        entrada = input(prompt).strip()
        if validador(entrada):
            return entrada
        print(mensaje_error)
        corregir = input("¿Desea intentar de nuevo? (S/N): ").strip().upper()
        if corregir != 'S':
            raise ValueError("Entrada cancelada por el usuario.")

def cerrar_programa():
    """Función para cerrar el programa de manera ordenada."""
    print("Gracias por usar el consultor del clima. ¡Hasta luego!")
    input("Presione Enter para salir...")
    exit()

def obtener_clima_ciudad(ciudad, api_key):
    """Consulta el clima de una ciudad usando la API de OpenWeather."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            temp_kelvin = data["main"]["temp"]
            temp_celsius = temp_kelvin - 273.15
            descripcion = data["weather"][0]["description"]
            print(f"El clima en {data['name']} es {descripcion}.")
        elif response.status_code == 404:
            print("Ciudad no encontrada. Por favor verifica el nombre y las siglas del país.")
        else:
            print("Error al hacer la petición:", response.status_code, response.text)
    except requests.RequestException as e:
        print("Error de conexión:", str(e))

def obtener_clima_coordenadas(lat, lon, api_key):
    """Consulta el clima usando latitud y longitud con la API de OpenWeather."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang=es"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            temp_kelvin = data["main"]["temp"]
            temp_celsius = temp_kelvin - 273.15
            descripcion = data["weather"][0]["description"]
            print(f"El clima en {data['name']} es {descripcion}.")
        elif response.status_code == 404:
            print("Coordenadas no encontradas. Por favor verifica las coordenadas en https://www.coordenadas-gps.com/")
        else:
            print("Error al hacer la petición:", response.status_code, response.text)
    except requests.RequestException as e:
        print("Error de conexión:", str(e))

def main():
    """Función principal para ejecutar el programa."""
    print("Consulta de pronóstico del clima")
    print("-" * 40)
    try:
        api_key = solicitar_entrada("Ingrese su API Key de OpenWeather: ", lambda x: x != "", "API Key incorrecta: no puede estar vacía.")
    except ValueError:
        return
    
    try:
        opcion = solicitar_entrada("¿Desea ingresar una ciudad (C) o coordenadas (K)? ", lambda x: x.upper() in ['C', 'K'], "Opción no válida. Debe ser C o K.")
        opcion = opcion.upper()
    except ValueError:
        return
    
    if opcion == 'C':
        try:
            ciudad = solicitar_entrada("Ingrese la ciudad y el país (formato: CIUDAD, SIGLAS_DEL_PAÍS): ", lambda x: len(x.split(',')) == 2 and x.split(',')[1].strip().isalpha() and len(x.split(',')[1].strip()) == 2 and x.split(',')[1].strip().isupper(), "Formato de ciudad incorrecto: debe ser CIUDAD, SIGLAS_DEL_PAÍS.")
        except ValueError:
            return
        obtener_clima_ciudad(ciudad, api_key)
        cerrar_programa()
    elif opcion == 'K':
        def validador_lat(x):
            try:
                val = float(x)
                return -90 <= val <= 90
            except ValueError:
                return False
        
        try:
            lat_str = solicitar_entrada("Ingrese la latitud: ", validador_lat, "Latitud debe ser un número entre -90 y 90.")
            lat = float(lat_str)
        except ValueError:
            return
        
        def validador_lon(x):
            try:
                val = float(x)
                return -180 <= val <= 180
            except ValueError:
                return False
        
        try:
            lon_str = solicitar_entrada("Ingrese la longitud: ", validador_lon, "Longitud debe ser un número entre -180 y 180.")
            lon = float(lon_str)
        except ValueError:
            return
        
        obtener_clima_coordenadas(lat, lon, api_key)
        cerrar_programa()

if __name__ == "__main__":    main()


