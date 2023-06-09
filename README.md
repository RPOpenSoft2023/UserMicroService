# UserMicroService

## Required Packages:
- View requirement.txt in the project directory.

## Instructions to build & install the software:
- Clone the repository

  ```
  git clone https://github.com/RPOpenSoft2023/UserMicroService.git
  ```
- Install Python 3.10 from source

  ```
  https://www.python.org/downloads/release/python-3109/
  ```
- Install virtualenv

  ```
  pip install virtualenv
  ```
- Create virtual environment

  ```
  python -m virtualenv myenv
  ```
- Activate the virtual environment
  
  Windows:
  
  ```
  ./myenv/Scripts/activate
  ```
  Linux:
  
  ```
  source myenv/bin/activate
  ```
- Add environment variables for connecting to Postgres Database
  
  Windows:
  
  ```
  [System.Environment]::SetEnvironmentVariable('DATABASE_USER', 'postgres')
  [System.Environment]::SetEnvironmentVariable('DATABASE_PASSWORD', 'demo')
  [System.Environment]::SetEnvironmentVariable('DATABASE_NAME', 'users-db')
  ```
  Linux:
  
  ```
  export DATABASE_USER='postgres'
  export DATABASE_PASSWORD='demo'
  export DATABASE_NAME='users-db'
  ```
- Change directory to the cloned folder i.e. UserMicroService

  ```
  cd UserMicroService
  ```
- Install all the required packages

  ```
  pip install -r requirements.txt
  ```
- Make migrations

  ```
  python manage.py makemigrations
  ```
- Migrate to create the tables inside the database

  ```
  python manage.py migrate
  ```
- Create superuser to use django admin panel

  ```
  python manage.py createsuperuser
  ```

## Instructions to run the software:
- Run the server

  ```
  python manage.py runserver
  ```
- To access the django admin panel use following url

  ```
  localhost:8000/admin
  ```
