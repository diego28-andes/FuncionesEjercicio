# CookHub - Sistema de Gestión Culinaria

> **PROYECTO ACADÉMICO GENERADO AUTOMÁTICAMENTE**  
> Este es un proyecto base funcional con datos mock. Los estudiantes deben implementar la persistencia real y lógica de negocio.

## 🎯 Objetivo del Proyecto

Desarrollar una aplicación web completa para que un chef ejecutivo pueda gestionar recetas e ingredientes de una cocina profesional. El sistema permite realizar operaciones CRUD completas y generar reportes de popularidad.

## 📁 Estructura del Proyecto

```
CookHub/
├── ENUNCIADO.md              # Descripción detallada del proyecto
├── README.md                 # Este archivo
├── backend/                  # API REST Python/Flask
│   ├── app.py               # Punto de entrada del servidor
│   ├── requirements.txt     # Dependencias de Python
│   ├── vistas/              # Endpoints REST
│   │   ├── __init__.py
│   │   └── vistas.py        # Controladores de la API
│   └── data/                # Datos mock (temporales)
│       ├── __init__.py
│       └── mock_data.py     # Datos de prueba
└── frontend/                # SPA Angular 17
    ├── package.json         # Dependencias de Node.js
    ├── angular.json         # Configuración de Angular
    ├── tsconfig.json        # Configuración de TypeScript
    ├── tsconfig.app.json    # Configuración específica de la app
    └── src/                 # Código fuente
        ├── index.html       # Página principal
        ├── main.ts          # Bootstrap de Angular
        ├── styles.css       # Estilos globales
        ├── favicon.ico      # Icono de la aplicación
        ├── assets/          # Recursos estáticos
        └── app/             # Componentes de Angular
            ├── app.component.ts
            ├── app.component.html
            ├── app.component.css
            ├── receta/      # Modelos y servicios de receta
            └── ingrediente/ # Modelos y servicios de ingrediente
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8+ y Node.js 18+

### Configuración del Backend (Puerto 5001)

- Ubicarse en la carpeta del proyecto: `cd backend`
- Crear el entorno virtual: `python -m venv venv`
- Activar el entorno virtual:
  * En **Windows**: `.\venv\Scripts\activate`
  * En **Mac/Linux**: `source venv/bin/activate`
- Instalar dependencias: `pip install -r requirements.txt`
- Ejecutar el backend: `python app.py`

Esto levantará la aplicación en el puerto **5001**.

### 📹 Videos de instalación

-   [Instalación en VS
    Code](https://uniandes.sharepoint.com/:v:/s/misw4101-202111-sesiones/EfYfRQUCN5BevxTiYxStj_gBsGkROrGvkQTRrwNdzPFqpQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=gYsQfL)
-   [Instalación en
    PyCharm](https://uniandes.sharepoint.com/:v:/s/misw4101-202111-sesiones/ETBIH-8YfKZVItds4QRXjz8Bp744bjx2ozC3Zz5k9bnEMg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=s1PjRp)


### Configuración del Frontend (Puerto 4200)

- Ubicarse en la carpeta del proyecto: `cd frontend`
- Instalar dependencias: `npm install`
- Ejecutar la aplicación: `npm start`

Esto levantará la aplicación en el puerto **4200**.


## 📚 Para los Estudiantes

**IMPORTANTE:** Este proyecto usa datos mock. Los estudiantes deben implementar:

- **Persistencia real:** Reemplazar datos mock con base de datos
- **Servicios backend:** Implementar lógica de negocio real
- **Validaciones avanzadas:** Mejorar validaciones del backend
- **Cálculo de reportes:** Implementar lógica real de estadísticas

### 📋 API Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/recetas` | Listar todas las recetas |
| POST | `/api/recetas` | Crear nueva receta |
| GET | `/api/recetas/{id}` | Obtener receta por ID |
| PUT | `/api/recetas/{id}` | Actualizar receta |
| DELETE | `/api/recetas/{id}` | Eliminar receta |
| GET | `/api/ingredientes` | Listar todos los ingredientes |
| POST | `/api/ingredientes` | Crear nuevo ingrediente |
| GET | `/api/ingredientes/{id}` | Obtener ingrediente por ID |
| PUT | `/api/ingredientes/{id}` | Actualizar ingrediente |
| DELETE | `/api/ingredientes/{id}` | Eliminar ingrediente |
| GET | `/api/reportes/ingredientes` | Generar reporte de popularidad |

### 🐛 Solución de Problemas Comunes

#### Backend no inicia
- Verificar que Python 3.8+ esté instalado
- Activar el entorno virtual
- Instalar dependencias: `pip install -r requirements.txt`

#### Frontend no carga
- Verificar que Node.js 18+ esté instalado
- Limpiar caché: `npm cache clean --force`
- Reinstalar: `rm -rf node_modules && npm install`

### Ejecutar tests en el backend

Dentro del folder `backend`, 

Para ejecutar todos los tests:

`python -m unittest discover tests -v`


Para ejecutar todos los tests de un modulo específico:

`python -m unittest tests/<test_module.py> -v `

**🎓 ¡Éxito en su proyecto!**