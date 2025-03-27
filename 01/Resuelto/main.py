from flask import Flask, jsonify, request
import random
import proximo_feriado as feriado

app = Flask(__name__)

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


def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    pelicula_encontrada = peliculas[id-1]
    return jsonify(pelicula_encontrada)


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    nuevo_titulo = request.json['titulo']
    nuevo_genero = request.json['genero']

    pelicula_actualizada = peliculas[id - 1]
    pelicula_actualizada['titulo'] = nuevo_titulo
    pelicula_actualizada['genero'] = nuevo_genero

    return jsonify(pelicula_actualizada)


def eliminar_pelicula(id):
    peliculas.pop(id - 1)
    for i in range(id - 1, len(peliculas)):
        peliculas[i]['id'] -= 1
    return jsonify({'mensaje': 'Película eliminada correctamente'})


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


def listado_genero(genero):
    listado = []
    for i in range(0, len(peliculas)):
        if(peliculas[i]['genero'] == genero):
            listado.append(peliculas[i])

    return jsonify(listado), 200


def listado_coincidencia(texto):
    listado = [p for p in peliculas if texto.lower() in p['titulo'].lower()]
    if not listado:
        return jsonify({'mensaje': f'No hay peliculas que coincidan\
                        con"{texto}".'}), 200
    return jsonify(listado), 200


def sugerir_aleatoria():
    if(peliculas != []):
        return peliculas[random.randint(0, len(peliculas))]


def sugerir_aleatoria_genero(genero):
    listado = [i for i in peliculas if i['genero'] == genero]
    pelicula_aleatoria = random.choice(listado)
    return jsonify(pelicula_aleatoria), 200


def sugerir_pelicula_feriado(genero):
    next_holiday = feriado.NextHoliday()
    feriado.next_holiday.fetch_holidays()
    listado = [i for i in peliculas if i['genero'] == genero]
    pelicula_aleatoria = random.choice(listado)
    texto = (
        f"El proximo feriado es el {feriado.next_holiday.string_holiday()} "
        f"con motivo {feriado.next_holiday.string_motivo()}. Te sugiero ver "
        f"la pelicula de {genero} {pelicula_aleatoria['titulo']}"
    )
    return jsonify(texto), 200

app.add_url_rule('/peliculas',
                 'obtener_peliculas',
                 obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>',
                 'obtener_pelicula',
                 obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas',
                 'agregar_pelicula',
                 agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>',
                 'actualizar_pelicula',
                 actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>',
                 'eliminar_pelicula',
                 eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/genero/<genero>',
                 'listado_genero',
                 listado_genero, methods=['GET'])
app.add_url_rule('/peliculas/buscar/<texto>',
                 'listado_coincidencia',
                 listado_coincidencia, methods=['GET'])
app.add_url_rule('/peliculas/sugerir',
                 'sugerir_aleatoria',
                 sugerir_aleatoria, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<genero>',
                 'sugerir_aleatoria_genero',
                 sugerir_aleatoria_genero, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/feriado/<genero>',
                 'sugerir_pelicula_feriado',
                 sugerir_pelicula_feriado, methods=['GET'])

if __name__ == '__main__':
    app.run()
