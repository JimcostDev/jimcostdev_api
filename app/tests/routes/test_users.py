import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from routes.user import (
    create_user_endpoint,
    get_user_endpoint, 
    get_userbyEmail_endpoint,
    update_user_endpoint,
    reset_password_endpoint,
    delete_user_endpoint
)
from database.models.user_model import (
    UserModel, 
    UserResponseModel,
    UserUpdateModel, 
    ResetPasswordModel
)
from fastapi import HTTPException, status

# Sample test data
test_user_data = UserModel(
    full_name="Test User",
    username="testuser",
    email="test@example.com",
    password="TestPassword123*",
    confirm_password="TestPassword123*",
    secret="testsecret"
)

def test_create_user_success():
    """Test successful user creation"""
    with patch('database.operations.user_db.user_exists_by_email', return_value=False), \
         patch('database.operations.user_db.user_exists_by_username', return_value=False), \
         patch('database.operations.user_db.create_user', return_value=(test_user_data.model_dump(), status.HTTP_201_CREATED)):
        
        result = create_user_endpoint(test_user_data)
        assert result == {"message": "Usuario creado exitosamente"}

def test_create_user_email_exists():
    """Test user creation with existing email"""
    with patch('database.operations.user_db.user_exists_by_email', return_value=True):
        with pytest.raises(HTTPException) as excinfo:
            create_user_endpoint(test_user_data)
        
        assert excinfo.value.status_code == status.HTTP_409_CONFLICT
        

def test_create_user_username_exists():
    """Test user creation with existing username"""
    with patch('database.operations.user_db.user_exists_by_email', return_value=False), \
         patch('database.operations.user_db.user_exists_by_username', return_value=True):
        with pytest.raises(HTTPException) as excinfo:
            create_user_endpoint(test_user_data)
        
        assert excinfo.value.status_code == status.HTTP_409_CONFLICT

def test_get_user_success():
    """Test successful user retrieval by username"""
    with patch('database.operations.user_db.get_user', return_value={
        'id': 1,
        'full_name': 'Test User',
        'username': 'testuser',
        'email': 'test@example.com'
    }):
        result = get_user_endpoint(test_user_data.username)
        assert result.get('full_name') == 'Test User'
        assert result.get('username') == 'testuser'
        assert result.get('email') == 'test@example.com'

def test_get_user_by_email_success():
    """Test successful user retrieval by email"""
    with patch('database.operations.user_db.get_user_by_email', return_value={
        'id': 1,
        'full_name': 'Test User',
        'username': 'testuser',
        'email': 'test@example.com'
    }):
        result = get_userbyEmail_endpoint(test_user_data.email)
        assert result.get('full_name') == 'Test User'
        assert result.get('username') == 'testuser'
        assert result.get('email') == 'test@example.com'

def test_get_user_not_found():
    """Test user retrieval for non-existent user"""
    with patch('database.operations.user_db.get_user', return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            get_user_endpoint("nonexistentuser")
        
        assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_user_by_email_not_found():
    """Test user retrieval by non-existent email"""
    with patch('database.operations.user_db.get_user_by_email', return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            get_userbyEmail_endpoint("nonexistent@example.com")
        
        assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND

def test_update_user_success():
    """Test successful user update"""
    update_data = UserUpdateModel(full_name="Updated Name")
    current_user = {"username": "testuser"}
    
    with patch('database.operations.user_db.update_user', return_value={"message": "Usuario actualizado exitosamente"}), \
         patch('routes.user.check_user_role', return_value=current_user):
        
        result = update_user_endpoint(update_data, current_user)
        assert result == {"message": "Usuario actualizado exitosamente"}

def test_reset_password_success():
    """Test successful password reset"""
    reset_data = ResetPasswordModel(new_password="NewPassword123*")
    
    with patch('database.operations.user_db.reset_password', return_value={"message": "Contraseña restablecida exitosamente"}):
        result = reset_password_endpoint(reset_data, "testuser", "testsecret")
        assert result == {"message": "Contraseña restablecida exitosamente"}

def test_delete_user_success():
    """Test successful user deletion"""
    current_user = {"username": "testuser"}
    
    with patch('database.operations.user_db.delete_user', return_value=("Usuario eliminado exitosamente", status.HTTP_200_OK)), \
         patch('routes.user.check_user_role', return_value=current_user):
        
        result = delete_user_endpoint(current_user)
        assert result == {"message": "Usuario eliminado exitosamente"}