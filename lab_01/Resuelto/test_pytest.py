import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={
            'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'
        })

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={
            'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'
        })

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={
            'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'
        })

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        m.get('http://localhost:5000/peliculas/genero/Acción', status_code=200, json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])
        
        # Simulamos la respuesta para buscar coincidencias de texto 
        m.get('http://localhost:5000/peliculas/buscar/the', status_code=200, json=[
            {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
            {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
            {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
            {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
            {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'}
        ])
        
        # Simulamos la respuesta para sugerir una pelicula aleatoria
        m.get('http://localhost:5000/peliculas/sugerir', status_code=200, json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})
        
        # Simulamos la respuesta para sugerir una pelicula aleatoria de un genero particular
        m.get('http://localhost:5000/peliculas/sugerir/Ciencia%20ficción', status_code=200, json={
            'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'
        })

        # Simulamos la respuesta para sugerir una pelicula aleatoria de un genero particular para el proximo feriado
        # m.get('http://localhost:5000/peliculas/sugerir/feriado/Ciencia ficción', status_code=200, json=)

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200

def test_listado_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/genero/Acción')
    assert response.status_code == 200

def test_listado_coincidencia(mock_response):
    response = requests.get('http://localhost:5000/peliculas/buscar/the')
    assert response.status_code == 200

def test_sugerir_aleatoria(mock_response):
    response = requests.get('http://localhost:5000/peliculas/sugerir')
    assert response.status_code == 200


def test_sugerir_aleatoria_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/sugerir/Ciencia ficción')
    assert response.status_code == 200

# def test_sugerir_pelicula_feriado(mock_response):
#     response = requests.get('http://localhost:5000/peliculas/sugerir/feriado/Ciencia ficción')
#     assert response.status_code == 200