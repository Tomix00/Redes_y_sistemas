import requests


# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(
        f"ID: {pelicula['id']}, "
        f"Título: {pelicula['titulo']}, "
        f"Género: {pelicula['genero']}"
    )
print()


# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas',
                         json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(
        f"ID: {pelicula_agregada['id']}, "
        f"Título: {pelicula_agregada['titulo']}, "
        f"Género: {pelicula_agregada['genero']}"
    )
else:
    print("Error al agregar la película.")
print()


# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(
        f"ID: {pelicula['id']}, "
        f"Título: {pelicula['titulo']}, "
        f"Género: {pelicula['genero']}"
    )
else:
    print("Error al obtener los detalles de la película.")
print()


# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(
    f'http://localhost:5000/peliculas/{id_pelicula}',
    json=datos_actualizados
)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(
        f"ID: {pelicula_actualizada['id']}, "
        f"Título: {pelicula_actualizada['titulo']}, "
        f"Género: {pelicula_actualizada['genero']}"
    )
else:
    print("Error al actualizar la película.")
print()


# Obtener películas de un género
genero = 'Acción'  # Género a buscar
response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
if response.status_code == 200:
    peliculas_genero = response.json()
    print(f"Películas de género '{genero}':")
    for pelicula in peliculas_genero:
        print(
            f"ID: {pelicula['id']}, "
            f"Título: {pelicula['titulo']}, "
            f"Género: {pelicula['genero']}"
        )
else:
    print(f"Error al obtener películas de género '{genero}'.")
print()


# Listado de coincidencias
texto = 'the'
response = requests.get(f'http://localhost:5000/peliculas/buscar/{texto}')
if response.status_code == 200:
    peliculas_coincidencia = response.json()
    print(f"Películas que contienen '{texto}' en el título:")
    for pelicula in peliculas_coincidencia:
        print(
            f"ID: {pelicula['id']}, "
            f"Título: {pelicula['titulo']}, "
            f"Género: {pelicula['genero']}"
        )
else:
    print(f"Error al buscar películas con '{texto}' en el título.")
print()


# Sugerencia aleatoria
response = requests.get('http://localhost:5000/peliculas/sugerir')
if response.status_code == 200:
    pelicula_aleatoria = response.json()
    print("Película aleatoria sugerida:")
    print(
        f"ID: {pelicula_aleatoria['id']}, "
        f"Título: {pelicula_aleatoria['titulo']}, "
        f"Género: {pelicula_aleatoria['genero']}"
    )
else:
    print("Error al sugerir una película aleatoria.")
print()


# Sugerencia aleatoria de un género
genero = 'Ciencia ficción'  # Género para la sugerencia
response = requests.get(f'http://localhost:5000/peliculas/sugerir/{genero}')
if response.status_code == 200:
    pelicula_aleatoria_genero = response.json()
    print(f"Película aleatoria de género '{genero}':")
    print(
        f"ID: {pelicula_aleatoria_genero['id']}, "
        f"Título: {pelicula_aleatoria_genero['titulo']}"
    )
else:
    print(f"Error al sugerir una película aleatoria de género '{genero}'.")
print()


# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()


# Sugerencia aleatoria de un género para el proximo feriado
genero = 'Ciencia ficción'  # Género para la sugerencia
response = requests.get(
    f'http://localhost:5000/peliculas/sugerir/feriado/{genero}'
)
if response.status_code == 200:
    sugerir_pelicula_feriado = response.json()
    print(response.json())
else:
    print(
        f"Error al sugerir una película aleatoria de género "
        f"para el proximo feriado '{genero}'."
    )
print()
