"""API_KEY authentication"""
import os
import re
import secrets
import time
from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

# pylint: disable=E0401
# pylint: disable=C0103
# pylint: disable=W0603
# pylint: disable=W1514
# Load environment variables from a .env file
load_dotenv()

# Constants
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Global variables to store authentication state
usuario_autenticado = None  # Tracks authenticated user
tiempo_expiracion = None    # Tracks the token expiration time
DURACION_TOKEN = 600        # Token validity duration (10 minutes, in seconds)

def generar_api_key() -> str:
    """
    Generate a unique API key and append it to the .env file.
    
    This function generates a random 32-character API key using the `secrets` 
    module, and writes this key to the `.env` file in the specified path.
    
    Returns:
        str: The generated API key.
    """
    key = secrets.token_urlsafe(32)

    # Leer el contenido del archivo .env
    with open("FastApi/app/.env", "r") as env_file:
        env_content = env_file.read()

    if "API_KEY=" in env_content:
        env_content = re.sub(r"API_KEY=.*", f"API_KEY={key}",
                             env_content)
    else:
        env_content += f"\nAPI_KEY={key}"

    with open("FastApi/app/.env", "w") as env_file:
        env_file.write(env_content)

    return key

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Validate the API key provided in the request header.
    
    This function checks the API key sent in the request against the 
    API key stored in environment variables. If the keys match, it returns
    the API key, otherwise raises an HTTP 403 error.
    
    Args:
        api_key (str): API key retrieved from the request's Security header.
    
    Returns:
        str: The validated API key.
    
    Raises:
        HTTPException: If the provided API key does not match the stored API key, 
        a 403 Forbidden error is raised.
    """
    API_KEY = os.getenv("API_KEY")
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "status": False,
            "status_code": status.HTTP_403_FORBIDDEN,
            "message": "Unauthorized",
        },
    )

def validar_usuario(usuario: str, password: str) -> str:
    """
    Validate user credentials and generate an API key if authentication is successful.
    
    This function checks if the provided username and password match the 
    predefined valid user credentials. If the user is already authenticated and 
    their token has not expired, the function returns `True`. Otherwise, if the 
    credentials are valid, a new API key is generated, and the user's authentication 
    state is updated.
    
    Args:
        usuario (str): The username provided by the user.
        password (str): The password provided by the user.
    
    Returns:
        str: The generated API key if authentication is successful.
        None: If authentication fails.
    """
    global usuario_autenticado, tiempo_expiracion

    # Predefined valid users and their corresponding passwords
    usuarios_validos = {
        "nicolas.duran@eam.edu.co": "NicolasDuranGarces",
        "d@p.com": "1234",
        "c@d.com": "1234"
    }

    # If the user is already authenticated and their token hasn't expired
    if usuario_autenticado and time.time() < tiempo_expiracion:
        return True  # User is still authenticated

    # If the provided credentials are valid
    if usuario in usuarios_validos and usuarios_validos[usuario] == password:
        API_KEY = generar_api_key()  # Generate a new API key
        usuario_autenticado = usuario  # Update authenticated user
        tiempo_expiracion = time.time() + DURACION_TOKEN  # Set token expiration time
        return API_KEY  # Return the generated API key

    return None  # Authentication failed
