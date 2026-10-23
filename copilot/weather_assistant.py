# get_temperature que obtiene la temperatura actual de una ciudad usando la API de wttr.in
def get_temperature(city):
    import requests

    # Formatear la ciudad para la URL
    city_formatted = city.replace(" ", "+")
    url = f"https://wttr.in/{city_formatted}?format=%t"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        temperature = response.text.strip()
        return temperature
    except requests.RequestException as e:
        return f"Error al obtener la temperatura: {e}"

# Función give_recommendation que recomienda qué hacer según la temperatura


def give_recommendation(temperature):
    try:
        temp_value = float(temperature.replace("°C", "").strip())
        if temp_value < 10:
            return "Hace frío, te recomiendo abrigarte bien."
        elif 10 <= temp_value < 20:
            return "El clima es fresco, una chaqueta ligera sería ideal."
        elif 20 <= temp_value < 30:
            return "El clima es agradable, puedes salir a pasear."
        else:
            return "Hace calor, asegúrate de hidratarte y usar protector solar."
    except ValueError:
        return "No se pudo interpretar la temperatura para dar una recomendación."


def main():
    city = input("Ingrese el nombre de la ciudad: ")
    temperature = get_temperature(city)
    recommendation = give_recommendation(temperature)
    print(f"La temperatura actual en {city} es: {temperature}")
    print(f"Recomendación: {recommendation}")


if __name__ == "__main__":
    main()
