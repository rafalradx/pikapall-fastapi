# Project Name

**Pikapall-fastapi**

## Table of Contents

- [Prerequisites ](#prerequisites)
- [Installation ](#installation)
- [Running](#running)
- [Contributing](#contributing)
- [Info](#info)
- [Contact](#contact)
- [License](#license)

## Prerequisites
Make sure your environment meets the following requirements:
- Python 3.6 or newer with pip
- PostgreSQL database (other databases may be required if your application's requirements differ)
- Any code editor (e.g., Visual Studio Code, PyCharm)

## Installation
1. Clone the repository:
Paste this URL to terminal:

git clone https://github.com/rafalradx/pikapall-fastapi.git

2. Navigate to the cloned repository:
cd pikapall-fastapi

3. Create a Python virtual environment (recommended but optional):
python3 -m venv venv


4. Install dependencies using pip:
pip install pipfile


5. Configure the environment variables:
To run application you have to create a file ".env" in project directory

Copy this code to your ".env" :
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=567234
POSTGRES_PORT=5432
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET_KEY=a9bk2vhXAcZEJPQu-3jBhlRB8G1i5GvPrUW0mR1W0-0
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=15
JWT_REF_EXPIRE_DAYS=7

CLOUDINARY_NAME={your_cloudinary_name}
CLOUDINARY_API_KEY={your_cloudinary_api_key}
CLOUDINARY_API_SECRET={your_cloudinary_api_secret}

To get cloudinary you have to create account on : https://cloudinary.com/




## Running
1. Ensure your database is running and configured according to the settings in the `.env` file.
1.1 To run application you have to run docker, and paste "docker compose up"
2. Run the application:
To terminal paste: "python main.py" , P.S. You have to be in your project directory "cd path/to/project"

Now you should see :
"@app.on_event("startup")
INFO:     Started server process [8905]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)"


copy adress "http://0.0.0.0:8000" to your browser and enjoy our application :)


## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request with your change.

## Info

This project was completed during the "Python Developer" course organized by GOIT POLSKA Sp. z o.o.

## Contact

Created by **'Devs for Pokemons'**

**Katarzyna Drajok** _katarzyna.drajok@gmail.com_

**Katarzyna Czempiel** _katarzyna.czempiel@gmail.com_

**Rafał Pietras** _rafal.radx@gmail.com_

**Dawid Radzimski** _dawid.radzimski@gmail.com_

**Marcin Żołnowski** _marcin.zolnowski.olsztyn@gmail.com_

Feel free to contact us!
Thank you for using Pikapall-fastapi!

## License

This project is licensed under the MIT License.