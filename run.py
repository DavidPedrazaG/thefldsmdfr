# pylint: skip-file
import asyncio
import os
import webbrowser
import re
import pyperclip as clipboard
from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from FastApi.app.helpers.api_key_auth import validar_usuario, get_api_key

# Initialize FastAPI application
app = FastAPI()

# Global variable to hold Docker process
docker_process = None

# Initialize Jinja2 templates and mount static files directory
templates = Jinja2Templates(directory="FastApi/templates")
app.mount("/static", StaticFiles(directory=os.path.join("FastApi",
                                "public", "static")), name="static")

async def ejecutar_comando_async(comando):
    """
    Execute a shell command asynchronously.

    Args:
        comando (list): The command to execute as a list of strings.

    Returns:
        str: The stdout output from the command if successful.

    Raises:
        Exception: If the command execution fails.
    """
    try:
        process = await asyncio.create_subprocess_exec(
            *comando,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"Command executed successfully: {' '.join(comando)}")
            return stdout.decode()
        else:
            print(f"Error executing command: {stderr.decode()}")
            raise Exception(f"Error executing command: {stderr.decode()}")

    except Exception as e:
        print(f"Exception occurred while executing command: {str(e)}")
        raise

async def ejecutar_docker():
    """
    Build and run Docker containers asynchronously using Docker Compose.

    This function builds Docker images using 'docker-compose build' and starts
    containers using 'docker-compose up -d'. It also opens the FastAPI docs in
    the browser if successful.
    """
    global docker_process
    print("Building Docker images")
    await ejecutar_comando_async(["docker-compose", "build"])
    print("\nStarting Docker containers with 'up -d'")

    docker_process = await asyncio.create_subprocess_exec(
        "docker-compose", "up", "-d",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await docker_process.communicate()

    if docker_process.returncode == 0:
        webbrowser.open("http://localhost:9000/docs")
    else:
        print(f"Error starting Docker: return code {docker_process.returncode}")

@app.get("/", include_in_schema=False)
def read_root():
    """
    Root endpoint that redirects to the Pylint form page.
    
    Returns:
        RedirectResponse: Redirects the user to the '/pylint' route.
    """
    return RedirectResponse("/pylint")

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    """
    Renders the login form page.

    Args:
        request (Request): The current request object.

    Returns:
        TemplateResponse: Renders the login.html template.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Handles user login by validating credentials and generating an API key.

    Args:
        request (Request): The current request object.
        username (str): The submitted username.
        password (str): The submitted password.

    Returns:
        TemplateResponse: Renders the login page with a success or failure message.
    """
    api_key = validar_usuario(username, password)

    if api_key is None:
        return templates.TemplateResponse("login.html", {"request": request,
                                                         "message": "Invalid credentials"})

    elif api_key is True:
        return templates.TemplateResponse(
            "login.html", {"request": request,
            "message": "Session is still valid. Please wait until it expires to log in again."}
        )

    clipboard.copy(api_key)  # Copy API key to clipboard
    message = "Login successful. API key has been copied to your clipboard. Docker images are being built..."

    asyncio.create_task(ejecutar_docker())  # Asynchronously run Docker process
    return templates.TemplateResponse("login.html", {"request": request, "message": message, "alert": "Good"})

@app.get("/pylint")
async def pylint_form(request: Request):
    """
    Renders the Pylint form page.

    Args:
        request (Request): The current request object.

    Returns:
        TemplateResponse: Renders the pylint.html template.
    """
    return templates.TemplateResponse("pylint.html", {"request": request})

@app.post("/pylint")
async def pylint(request: Request):
    """
    Handles Pylint execution and displays the Pylint score.

    Args:
        request (Request): The current request object.

    Returns:
        TemplateResponse: Renders the pylint.html template with the Pylint score.
    """
    output = await ejecutar_comando_async(["pylint", "FastApi/app/"])
    print(output)

    # Extract the Pylint score from the output using regex
    match = re.search(r"rated at ([0-9]+\.[0-9]+)/10", output)
    point = 0
    if match:
        point = float(match.group(1))

    return templates.TemplateResponse("pylint.html", {"request": request, "point": point, "message": f"The code score is {point}"})

@app.get("/protected-endpoint")
async def protected_endpoint(api_key: str = Depends(get_api_key)):
    """
    A protected endpoint that requires an API key for access.

    Args:
        api_key (str): The API key provided via the request header.

    Returns:
        dict: A message confirming access to the protected endpoint.
    """
    return {"message": "Access granted to the protected endpoint"}

if __name__ == "__main__":
    import uvicorn
    import atexit

    def cerrar_docker():
        """
        Stops the Docker process when the application is terminated.
        """
        if docker_process:
            docker_process.terminate()
            docker_process.wait()

    atexit.register(cerrar_docker)  # Register the function to stop Docker on exit

    try:
        # Open the Pylint form in the browser
        webbrowser.open("http://localhost:8090/pylint")
        uvicorn.run(app, host="0.0.0.0", port=8090)
    except KeyboardInterrupt:
        cerrar_docker()  # Ensure Docker is stopped on KeyboardInterrupt
