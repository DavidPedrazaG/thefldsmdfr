# The FLDSMDFR
# Implementation of Validation in a Microservices Project

## Description

Leveraging Python's libraries and tools for building microservices applications, this project implements an application with two main entity types: **Movie** and **Plant**, each with their respective subclasses. These entities contain specific attributes and values, modeled using **Pydantic** (for data validation) and **Peewee** (for database management).

The application manages these entities through their respective CRUD (Create, Read, Update, Delete) endpoints, implemented using **FastAPI** and protected with an **API Key**. Additionally, data type validations ensure that the input data matches the expected types.

The project is executed using three **Docker** images:
1. **Database**: Implemented with **MariaDB**.
2. **Adminer**: A database management interface (similar to phpMyAdmin).
3. **Backend**: Built with **FastAPI** and documented using **Swagger**.

## Requirements

- **Python 3** installed
- **Docker Desktop** installed

## Steps to Run the Application

1. **Download the project**: Once the project is downloaded on your machine, open the project directory in your terminal.  
   Example on Windows:  
   `C:\Users\david\Documents\thefldsmdfr`

2. **Create the virtual environment**: 
   
   - If you have more than one Python version installed, run:  
     `python3 -m venv venv`

   - If you have only one Python version installed, run:  
     `python -m venv venv`

3. **Activate the virtual environment**: 

   - On Linux/Mac:  
     `source venv/bin/activate`

   - On Windows (Powershell):  
     `venv\Scripts\activate`

4. **Install the required libraries** (adjust the slashes `\` as needed for your OS):

   ```bash
   pip install -r FastApi\requirements.txt
   ```

5. **Open Docker Desktop**: Ensure Docker Desktop is running.

6. **Run the application**:

   - From **Visual Studio Code**: Open the IDE via the terminal with the command:  
     `code .`  
     Then run the `run.py` file.

   - From the terminal:  
     `python run.py`

7. **Test the application**: Once the application is running, you can test the endpoints.

## Login Information

For login, you can use your institutional email as the username and your full name in CamelCase format as the password.

## Delivery Information

- **Course**: Elective III - Microservices in Python
- **Instructor**: Nicolas Duran Garces

## Participants

- Camilo Duarte Rivera - 240220221023
- David Felipe Pedraza Guadir - 240220221027
