# 🥗 Gestor de Alimentos

## 📌 ¿Qué es?
Este proyecto es una **API REST** construida con **FastAPI** y **SQLAlchemy** que permite gestionar alimentos, recetas y tiendas, además de las relaciones entre ellos:

- 📦 **Alimentos** → control de nombre, cantidad, fecha de caducidad y si están congelados.  
- 🏬 **Tiendas** → dónde comprar cada alimento.  
- 🍳 **Recetas** → qué se puede cocinar con los alimentos disponibles.  
- 🔗 **Relaciones** → 
  - alimento ↔ tienda  
  - alimento ↔ receta  

La idea es poder **controlar tu nevera desde el móvil** sin tener que mirarla físicamente:  
- Saber cuándo caduca cada alimento.  
- Saber dónde comprarlo.  
- Saber qué recetas puedes hacer con lo que tienes.  

Todo esto se ejecuta en un **servidor local** 🚀.

## 📂 Archivos principales

- `main.py` → define los **endpoints de la API** con FastAPI.  
- `crud.py` → funciones para crear, leer, actualizar y eliminar (CRUD) alimentos, recetas y tiendas.  
- `models.py` → modelos de base de datos con SQLAlchemy, incluidas las relaciones many-to-many.  
- `schemas.py` → modelos de validación y respuesta con Pydantic.  
- `database.py` → configuración de la base de datos y conexión con PostgreSQL.  

## 🛠️ Tecnologías utilizadas
- [FastAPI](https://fastapi.tiangolo.com/) ⚡
- [SQLAlchemy](https://www.sqlalchemy.org/) 🗄️
- [Pydantic](https://docs.pydantic.dev/) ✅
- [PostgreSQL](https://www.postgresql.org/) 🐘
- [Uvicorn](https://www.uvicorn.org/) 🚀

## ⚙️ Instalación y ejecución

# 1. Clonar el repositorio
git clone https://github.com/tuusuario/gestor-alimentos.git
cd gestor-alimentos

# 2. Crear un entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows

pip install -r requirements.txt

# 3. Configurar la base de datos en PostgreSQL
Crea una base de datos llamada gestor_alimentos.
Ajusta usuario y contraseña en database.py si es necesario.
postgresql+psycopg2://postgres:1234@localhost:5432/gestor_alimentos

# 4. Levantar el servidor
uvicorn app.main:app --reload

## 📖 Documentación interactiva
- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- Redoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

## 📖 Endpoints principales

### 🔹 Alimentos
- POST /alimentos/ → Crear alimento  
- GET /alimentos/ → Listar alimentos  
- GET /alimentos/{id} → Obtener alimento por ID  
- PUT /alimentos/{id} → Actualizar alimento  
- DELETE /alimentos/{id} → Eliminar alimento  

### 🔹 Tiendas
- POST /tiendas/ → Crear tienda  
- GET /tiendas/ → Listar tiendas  
- GET /tiendas/{id} → Obtener tienda por ID  
- PUT /tiendas/{id} → Actualizar tienda  
- DELETE /tiendas/{id} → Eliminar tienda  

### 🔹 Recetas
- POST /recetas/ → Crear receta  
- GET /recetas/ → Listar recetas  
- GET /recetas/{id} → Obtener receta por ID  
- PUT /recetas/{id} → Actualizar receta  
- DELETE /recetas/{id} → Eliminar receta  

### 🔹 Relaciones
- POST /alimentos/{id_alimento}/tiendas/{id_tienda} → Asociar alimento con tienda  
- POST /alimentos/{id_alimento}/recetas/{id_receta} → Asociar alimento con receta  

## 🗃️ Modelo de datos
```mermaid
erDiagram
    ALIMENTO {
        int id_alimento PK
        string nombre_alimento
        float cantidad
        date caducidad
        bool congelado
    }
    TIENDA {
        int id_tienda PK
        string nombre_tienda
        string pagina_web
        string lugar
    }
    RECETA {
        int id_receta PK
        string nombre_receta
        string autor
        string url
    }
    ALIMENTO ||--o{ TIENDA : "se compra en"
    ALIMENTO ||--o{ RECETA : "se usa en"
```
## 🚀 Futuras mejoras
- Implementar autenticación de usuarios 🔑.  
- Agregar soporte para migraciones con Alembic 🛠️.  
- Desplegar en la nube (ej. Railway, Render, Heroku) 🌐.  
- Crear interfaz móvil o web conectada a la API 📱.  

## 👨‍💻 Autor
Proyecto desarrollado por **Alejnado Lara Lara** ✨
