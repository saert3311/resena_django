from django.core.management.utils import get_random_secret_key
import psycopg2
import subprocess
from book_manager.models import User

def load_data(fixture_file):
  command = ['python', 'manage.py', 'loaddata', fixture_file]
  subprocess.run(command)

def migrate_django():
  command = ['python', 'manage.py', 'migrate']
  subprocess.run(command)

secret = get_random_secret_key()

master_postgres = input("Usuario de postgres: [postgres]") or "postgres"
master_password = input("Contrasena de postgres: [blank]")

#get db database info into variables from input
db_name = input("Nombre Base de datos que crearemos para django: ")
db_user = input("Usuario de base de datos django: ")
db_password = input("Contrasena base de datos django: ")

try:
    # Connect to the default PostgreSQL database as a superuser
    conn = psycopg2.connect(
        database="postgres",
        user=master_postgres,
        password=master_password,
        host="localhost",
        port="5432"
    )
    conn.autocommit = True 
    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Create the new database
    cur.execute(f"CREATE DATABASE {db_name}")
    print(f"Base de datos '{db_name}' creada!")

    # Create the new user and grant privileges
    cur.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
    print(f"Usuario '{db_user}' creado!")

    # Grant all privileges on the new database to the new user
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cur.close()
        conn.close()
        print("Operaciones finalizadas!.")

# Write the secret key to a file .env
with open('.env', 'w') as f:
    f.write(f"DJANGO_SECRET={secret}")
    f.write(f"\nDJANGO_DB={db_name}")
    f.write(f"\nDJANGO_USER={db_user}")
    f.write(f"\nDJANGO_PASS={db_password}")

print("Archivo .env creado!")

#Crear datos iniciales
migrate_django()
load_data('datos.json')
#Crear usuarios de Prueba
User.objects.create_user(username='administrador', 
                        first_name='Administrador', last_name='Admin',
                        email='administrador@mail.com',password='Abc123#', user_type=0)
User.objects.create_user(username='lector', 
                        first_name='Lector', last_name='Lector',
                        email='lector@mail.com',password='Abc123#', user_type=1)


print("Datos Semilla Inicializados!")
