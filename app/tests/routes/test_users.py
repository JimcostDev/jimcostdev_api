import pytest
import httpx
from unittest.mock import patch

# La URL del endpoint
url = "https://jimcostdev.koyeb.app/users/jimcostdev"

# La respuesta esperada del endpoint
mock_response = {
    "id": 1,
    "full_name": "Ronaldo Jiménez Acosta",
    "username": "jimcostdev",
    "email": "jimcostdev@gmail.com"
}

# Función que simula el comportamiento de obtener datos de un perfil de usuario
def get_user_profile():
    # Hacemos la solicitud GET a la API (simulada en el test)
    response = httpx.get(url)
    return response.json()

# Test para verificar el comportamiento de la API con mock
@patch("httpx.get")  # Aquí mockeamos httpx.get
def test_get_user_profile(mock_get):
    # Configuramos el mock para devolver una respuesta simulada
    mock_get.return_value.status_code = 200  # Indicamos que el código de estado es 200 (OK)
    mock_get.return_value.json.return_value = mock_response  # Simulamos la respuesta en formato JSON

    # Llamamos a la función que simula la consulta de la API
    user_profile = get_user_profile()

    # Comprobamos que la respuesta sea la esperada
    assert user_profile["id"] == 1
    assert user_profile["full_name"] == "Ronaldo Jiménez Acosta"
    assert user_profile["username"] == "jimcostdev"
    assert user_profile["email"] == "jimcostdev@gmail.com"

    # Verificamos que httpx.get fue llamado una vez con la URL correcta
    mock_get.assert_called_once_with(url)
