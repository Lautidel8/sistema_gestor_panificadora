# Sistema Gestor de Panificadora Janssen 🍞

## Descripción

Este proyecto es un **sistema de gestión y control** diseñado para una panadería familiar, con el objetivo de modernizar y optimizar la administración de pedidos y el control de stock de materia prima.
Reemplaza el método tradicional de gestión (WhatsApp y pizarra) por una solución automatizada.

El sistema permite registrar, gestionar y controlar pedidos, así como llevar un seguimiento del stock de materia prima, mejorando la organización interna y el control de las operaciones diarias.

## Características ✨

* **Gestión de Pedidos:**
    * Registrar nuevos pedidos indicando cliente, fecha, productos y cantidades.
    * Modificar pedidos existentes.
    * Eliminar pedidos.
    * Asignar y actualizar estados a los pedidos (Pendiente, Entregado, Cancelado).
    * Calcular el precio total de los pedidos.
    * Filtrar pedidos por fecha.
* **Gestión de Productos:**
    * Cargar nuevos productos con nombre y precio unitario.
    * Asignar materias primas (receta) a cada producto.
    * Modificar productos existentes.
    * Eliminar productos.
* **Control de Stock de Materia Prima:**
    * Cargar nueva materia prima (nombre, distribuidor, unidad).
    * Actualizar las cantidades de stock existentes.
    * Eliminar materias primas (con validación si está asociada a un producto).
    * Visualizar el stock disponible de todas las materias primas.
    * Validación de stock disponible al cargar/modificar pedidos.
* **Interfaz Gráfica:**
    * Interfaz de usuario intuitiva desarrollada con Flet.
    * Navegación entre diferentes pantallas.
* **Seguridad:**
    * Inicio de sesión protegido por contraseña para el gerente.

## Tecnologías Utilizadas 🛠️

* **Lenguaje:** Python
* **Framework UI:** Flet
* **Base de Datos:** MySQL
* **Contenedorización:** Docker (para la base de datos MySQL)
* **Librerías Python:**
    * `mysql-connector-python`
    * `bcrypt` (para hashing de contraseñas)
    * `flet`

## Configuración e Instalación ⚙️

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL-del-repositorio>
    cd sistema_gestor_panificadora
    ```

2.  **Base de Datos MySQL:**
    * **Opción 1: Usando Docker (Recomendado)**
        * Asegúrate de tener Docker y Docker Compose instalados.
        * Desde la raíz del proyecto, ejecuta:
            ```bash
            docker-compose up -d
            ```
        * Esto iniciará un contenedor MySQL con el nombre `practicasprof`, la base de datos `Panaderia` y la contraseña `admin` para el usuario `root`, accesible en el puerto `3307` de tu máquina local.
    * **Opción 2: Instalación Manual**
        * Instala un servidor MySQL.
        * Crea una base de datos llamada `Panaderia`.
        * Asegúrate de que la configuración de conexión en `backend/conexion_a_BD/conexion_db.py` coincida con tu configuración de MySQL (host, puerto, usuario, contraseña, base de datos).
        * Ejecuta el script `db_practicasprof.sql` para crear las tablas necesarias.

3.  **Dependencias de Python:**
    * Se recomienda crear un entorno virtual:
        ```bash
        python -m venv venv
        source venv/bin/activate  # En Windows: venv\Scripts\activate
        ```
    * Instala las librerías necesarias (puedes crear un archivo `requirements.txt` con `flet`, `mysql-connector-python`, `bcrypt`):
        ```bash
        pip install flet mysql-connector-python bcrypt
        ```

## Ejecución de la Aplicación ▶️

1.  Asegúrate de que la base de datos MySQL esté en ejecución (ya sea el contenedor Docker o tu servidor local).
2.  Activa tu entorno virtual (si creaste uno).
3.  Ejecuta el archivo principal:
    ```bash
    python main.py
    ```
4.  La aplicación se iniciará en modo pantalla completa. Ingresa la contraseña (por defecto "1234") para acceder al sistema.

