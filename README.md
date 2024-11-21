# Project Setup

This guide will help you set up the project and run it locally.

## Prerequisites

Ensure you have Python 3.x and pip installed on your machine.

## Steps to Run the Project Locally

### 1. Create and Activate Virtual Environment

Before installing the dependencies, you need to create and activate the virtual environment. If you haven't created one yet, you can do so with the following command:

```bash
python -m venv venv
```
To activate the virtual environment, follow the instructions based on your operating system:

On Windows:

```bash
venv\Scripts\activate
```
On macOS/Linux:

```bash
source venv/bin/activate
```

### 2. Install Dependencies
Once the virtual environment is activated, install the required dependencies from requirements.txt by running the following command:

```bash
pip install -r requirements.txt
```

### 3. Run Migrations
To apply the database migrations, run the following command:

```bash
python manage.py migrate
```
### 4. Start the Development Server
To start the Django development server, run:

```bash
python manage.py runserver
```
Your server will now be running at http://localhost:8000.

### 5. Access the API Documentation
You can access the API documentation at:

[API Documentation](http://localhost:8000/api/docs/swagger)





