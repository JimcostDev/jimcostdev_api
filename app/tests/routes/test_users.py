import pytest
import httpx
from unittest.mock import patch

# URL base para los endpoints
url_create = "https://jimcostdev.koyeb.app/users"
url_get = "https://jimcostdev.koyeb.app/users/jimcostdev"

# Datos de usuario para las pruebas
user_data = {
    "full_name": "Ronaldo Jiménez Acosta",
    "username": "jimcostdev",
    "email": "jimcostdev@gmail.com",
    "secret": "supersecret",
    "password": "Password123*",
    "confirm_password": "Password123*"
}

# Respuesta simulada del servidor para un GET (cuando se obtiene el perfil de un usuario)
mock_response_get = {
    "id": 1,
    "full_name": "Ronaldo Jiménez Acosta",
    "username": "jimcostdev",
    "email": "jimcostdev@gmail.com"
}

# Respuesta simulada del servidor para un POST (cuando se crea un usuario)
mock_response_create = {
    "message": "Usuario creado exitosamente"
}

# Fixtures para mockear las funciones de HTTP
@pytest.fixture
def mock_post():
    with patch("httpx.Client.post") as mock:
        yield mock

@pytest.fixture
def mock_get():
    with patch("httpx.Client.get") as mock:
        yield mock

# Test de creación de usuario
def test_create_user(mock_post):
    # Configuramos el mock para simular la respuesta de la API al crear un usuario
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = mock_response_create
    
    # Llamamos a httpx.post directamente con los datos del usuario
    with httpx.Client() as client:
        response = client.post(url_create, json=user_data)
    
    # Verificamos que la respuesta sea correcta
    assert response.status_code == 201
    assert response.json() == mock_response_create
    
    # Verificamos que el mock fue llamado con los datos correctos
    mock_post.assert_called_once_with(url_create, json=user_data)

# Test de obtención de perfil de usuario
def test_get_user_profile(mock_get):
    # Configuramos el mock para simular la respuesta de la API al obtener el perfil
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_get
    
    # Usamos httpx.Client() para simular el GET a la API
    with httpx.Client() as client:
        response = client.get(url_get)
    
    # Verificamos que la respuesta sea la esperada
    assert response.status_code == 200
    assert response.json() == mock_response_get
    
    # Verificamos que el mock de get fue llamado con la URL correcta
    mock_get.assert_called_once_with(url_get)
