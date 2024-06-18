# Titulo del proyecto

Book Reviews para certificacion de Talento Digital

## Descripción del proyecto

Proyecto destinado a mostrar capacidades basicas de un sistema en django para acceso modificacion y manejo de datos

## Capturas de Pantalla del Proyecto

![Home](https://r2.trinum.xyz/home_books.png)
Vista inicio de la aplicación.

![Login](https://r2.trinum.xyz/login_books.png)
Login

![Profile](https://r2.trinum.xyz/profile_%20books.png)
Perfil Usuario Registrado

![Book](https://r2.trinum.xyz/single_book.png)
Detalles de un libro

![Genre](https://r2.trinum.xyz/genre_book.png)
Genres

## Prerrequisitos o Dependencias

- Sistema Operativo (Ubuntu, Windows, MacOs)
- Lenguaje de programación (Python 3.10)
- Framework (Django 5)
- Base de datos (PostgreSQL >= 12)

## Instalación del Proyecto

Creacion del ambiente virtual
```bash
$ python -m venv venv
```

Activamos el entorno virtual

```bash
$ source venv/bin/activate #sistemas UNIX
$ .\venv\Scripts\activate #sistemas Windows
```

Instalamos dependencias

```bash
$ (venv) pip install -r requirements.txt
```

## Instrucciones para Ejecutar el Proyecto

Inicializamos el proyecto para lo cual contamos con un archivo para configurar la base de datos, conexiones, usuarios iniciales, y datos semilla.

Para lo cual el script nos preguntara los datos de conexion para postgres, usuario, contraseña, creara la base de datos, con las migraciones iniciales y los usuario iniciales

```bash
cd resena_libros/ #debemos trasladarnos a la carpeta del proyecto
python set_db.py
```

## Iniciar servidor desarrollo

Una vez configurado lo anterior se puede iniciar el servidor de django.

```bash
python manage.py runserver
```

## Credenciales de Acceso

Se crearon 2 usuarios para pruebas pero puede experimentar creando otros tambien

### Para Usuario Tipo Administrador

- Email: administrador@mail.com
- Contraseña: Abc123#

### Para Usuario Tipo Huésped

- Email: lector@mail.com
- Contraseña: Abc123#

## Autor

- [Jose Duarte](https://github.com/saert3311) forkeado de -> [Brayan Diaz C](https://github.com/brayandiazc)

## Licencia

Este proyecto está bajo la Licencia MIT - ve el archivo [LICENSE.md](LICENSE) para detalles

---
