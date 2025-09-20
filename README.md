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

## 📂 Estructura del proyecto
```
gestor-alimentos/
│── app/
│   ├── main.py        # Endpoints de la API (FastAPI)
│   ├── crud.py        # Funciones CRUD para alimentos, recetas y tiendas
│   ├── models.py      # Modelos SQLAlchemy + relaciones
│   ├── schemas.py     # Modelos Pydantic (entrada/salida de datos)
│   └── database.py    # Configuración de la base de datos PostgreSQL
│── frontend/
│   ├── index.html     # Interfaz web con botones
│   ├── script.js      # Lógica para llamar a la API desde el navegador
│   └── syles.css      # Haz que la interfaz se vea bonita y responsive
│── requirements.txt   # Dependencias del proyecto
│── run.bat            # Enciende el servidor y activa ngrok
│── README.md          # Documentación
```


## 🛠️ Tecnologías utilizadas
- [FastAPI](https://fastapi.tiangolo.com/) ⚡ → Framework backend para construir la API REST.  
- [SQLAlchemy](https://www.sqlalchemy.org/) 🗄️ → ORM para interactuar con la base de datos.  
- [Pydantic](https://docs.pydantic.dev/) ✅ → Validación de datos y esquemas.  
- [PostgreSQL](https://www.postgresql.org/) 🐘 → Base de datos relacional.  
- [Uvicorn](https://www.uvicorn.org/) 🚀 → Servidor ASGI para ejecutar FastAPI.  
- [HTML](https://developer.mozilla.org/docs/Web/HTML) + [JavaScript](https://developer.mozilla.org/docs/Web/JavaScript) 🌐 → Frontend sencillo para interactuar con la API.  
- [ngrok](https://ngrok.com/) 🌍 → Exponer el servidor local a Internet de forma segura.  

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

# 5. Abrir el frontend
Abre este archivo en tu navegador
frontend/index.html

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
- Portar a una aplicación para iOs de forma que el servidor esté de forma local en el dispositivo
- Mejorar frontend
- Conexión con APIs de supermercados
- Avisos de caducidad

## 👨‍💻 Autor
Proyecto desarrollado por **Alejnado Lara Lara** ✨
