# test.py

import pytest
from main import app

@pytest.fixture
def client():
    app.testing = True  # activa el modo de testing de Flask
    with app.test_client() as client:
        yield client

def test_obtener_peliculas(client):
    response = client.get('/peliculas')
    assert response.status_code == 200
    data = response.get_json()
    # Dependiendo del estado inicial de 'peliculas', ajustar la cantidad de elementos esperados
    assert isinstance(data, list)
    # Ejemplo: verificar que haya al menos 12 películas
    assert len(data) >= 12

def test_agregar_pelicula(client):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = client.post('/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == 'Pelicula de prueba'
    # Puedes agregar más aserciones según la lógica de 'obtener_nuevo_id'

def test_obtener_detalle_pelicula(client):
    response = client.get('/peliculas/1')
    # Esto dependerá de que la función 'obtener_pelicula' esté implementada correctamente
    # Aquí se espera un 200 y los detalles de la película con id 1
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(client):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = client.put('/peliculas/1', json=datos_actualizados)
    # Verifica el status code y los cambios realizados
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(client):
    response = client.delete('/peliculas/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'mensaje' in data
    response = client.get('/peliculas/1')
    # assert response.status_code == 404 

def test_listado_genero(client):
    response = client.get('/peliculas/genero/Acción')
    assert response.status_code == 200
    data = response.get_json()
    assert all(p['genero'] == 'Acción' for p in data)

def test_listado_coincidencia(client):
    response = client.get('/peliculas/buscar/the')
    assert response.status_code == 200
    data = response.get_json()
    assert any('the' in p['titulo'].lower() for p in data)

def test_sugerir_aleatoria(client):
    response = client.get('/peliculas/sugerir')
    assert response.status_code == 200
    data = response.get_json()
    assert 'titulo' in data and 'genero' in data

def test_sugerir_aleatoria_genero(client):
    response = client.get('/peliculas/sugerir/Ciencia%20ficción')
    assert response.status_code == 200
    data = response.get_json()
    assert data['genero'] == 'Ciencia ficción'

