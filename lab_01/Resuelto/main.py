from flask import Flask, jsonify, request, Response
from typing import List, Dict, Tuple, Union, Optional
import random
import proximo_feriado as feriado

app: Flask = Flask(__name__)

peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def obtener_peliculas() -> Response:
    """Obtiene el listado completo de películas.
    
    Returns:
        Lista de todas las películas en formato JSON.
    """
    return jsonify(peliculas)


def obtener_pelicula(id: int) -> Response:
    """Obtiene una película específica por su ID.
    
    Args:
        id: ID de la película a buscar.
        
    Returns:
        Datos de la película en formato JSON.
    """
    pelicula_encontrada = peliculas[id-1]
    return jsonify(pelicula_encontrada)


def agregar_pelicula() -> Tuple[Response, int]:
    """Agrega una nueva película al listado.
    
    Returns:
        Datos de la nueva película en formato JSON y código HTTP 201 (Created).
    """
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id: int) -> Response:
    """Actualiza los datos de una película existente.
    
    Args:
        id: ID de la película a actualizar.
        
    Returns:
        Datos actualizados de la película en formato JSON.
    """
    nuevo_titulo = request.json['titulo']
    nuevo_genero = request.json['genero']
    pelicula_actualizada = peliculas[id - 1]
    pelicula_actualizada['titulo'] = nuevo_titulo
    pelicula_actualizada['genero'] = nuevo_genero
    return jsonify(pelicula_actualizada)


def eliminar_pelicula(id: int) -> Response:
    """Elimina una película del listado.
    
    Args:
        id: ID de la película a eliminar.
        
    Returns:
        Mensaje de confirmación en formato JSON.
    """
    peliculas.pop(id - 1)
    for i in range(id - 1, len(peliculas)):
        peliculas[i]['id'] -= 1
    return jsonify({'mensaje': 'Película eliminada correctamente'})


def obtener_nuevo_id() -> int:
    """Genera un nuevo ID para una película.
    
    Returns:
        Nuevo ID disponible.
    """
    return peliculas[-1]['id'] + 1 if peliculas else 1


def listado_genero(genero: str) -> Tuple[Response, int]:
    """Obtiene películas filtradas por género.
    
    Args:
        genero: Género por el cual filtrar.
        
    Returns:
        Listado de películas en formato JSON y código HTTP 200 (OK).
    """
    listado = [
        p for p in peliculas if p['genero'] == genero
    ]
    return jsonify(listado), 200


def listado_coincidencia(texto: str) -> Tuple[Response, int]:
    """Busca películas cuyo título contenga el texto especificado.
    
    Args:
        texto: Texto a buscar en los títulos.
        
    Returns:
        Listado de películas encontradas en formato JSON y código HTTP 200 (OK), 
        o mensaje de no encontradas.
    """
    listado = [
        p for p in peliculas if texto.lower() in p['titulo'].lower()
    ]
    if not listado:
        return jsonify({'mensaje': f'No hay peliculas que coincidan con "{texto}".'}), 200
    return jsonify(listado), 200


def sugerir_aleatoria() -> Optional[Dict[str, Union[int, str]]]:
    """Sugiere una película aleatoria del listado.
    
    Returns:
        Datos de la película sugerida.
    """
    return random.choice(peliculas) if peliculas else None


def sugerir_aleatoria_genero(genero: str) -> Tuple[Response, int]:
    """Sugiere una película aleatoria de un género específico.
    
    Args:
        genero: Género de las películas a considerar.
        
    Returns:
        Película aleatoria en formato JSON y código HTTP 200 (OK).
    """
    listado = [
        p for p in peliculas if p['genero'] == genero
    ]
    pelicula_aleatoria = random.choice(listado)
    return jsonify(pelicula_aleatoria), 200


def sugerir_pelicula_feriado(genero: str) -> Tuple[Response, int]:
    """Sugiere una película para el próximo feriado.
    
    Args:
        genero: Género de la película a sugerir.
        
    Returns:
        Mensaje con sugerencia en formato JSON y código HTTP 200 (OK).
    """
    next_holiday = feriado.NextHoliday()
    next_holiday.fetch_holidays()
    listado = [
        p for p in peliculas if p['genero'] == genero
    ]
    pelicula_aleatoria = random.choice(listado)
    texto = (
        f"El proximo feriado es el {next_holiday.string_holiday()} "
        f"con motivo {next_holiday.string_motivo()}. Te sugiero ver "
        f"la pelicula de {genero} {pelicula_aleatoria['titulo']}"
    )
    return jsonify(texto), 200


# Configuración de rutas
app.add_url_rule('/peliculas', 'obtener_peliculas',
                                         obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula',
                                         obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula',
                                         agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula',
                                         actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula',
                                         eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/genero/<genero>', 'listado_genero',
                                         listado_genero, methods=['GET'])
app.add_url_rule('/peliculas/buscar/<texto>', 'listado_coincidencia',
                                         listado_coincidencia, methods=['GET'])
app.add_url_rule('/peliculas/sugerir', 'sugerir_aleatoria',
                                         sugerir_aleatoria, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<genero>', 'sugerir_aleatoria_genero',
                                         sugerir_aleatoria_genero, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/feriado/<genero>', 'sugerir_pelicula_feriado',
                                         sugerir_pelicula_feriado, methods=['GET'])

if __name__ == '__main__':
    app.run()