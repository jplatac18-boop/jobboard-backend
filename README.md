README definitivo – jobboard-backend

Job Board Backend
Backend de la plataforma Job Board, una API REST para gestionar ofertas de trabajo, empresas, candidatos y postulaciones, preparada para entorno de producción con Django, Django REST Framework y PostgreSQL.

La API está pensada para integrarse con un frontend SPA (React + TypeScript + Tailwind) y cubrir el flujo completo: empresas publican ofertas, candidatos se registran y postulan, y un administrador puede moderar la actividad.

Características principales
Autenticación y autorización con JWT (login, registro, endpoint para obtener datos del usuario autenticado).

Gestión completa de usuarios con modelo personalizado (users.User) y roles diferenciados (candidato, empresa, admin).

CRUD de ofertas de trabajo (Job), perfiles de empresa (CompanyProfile) y postulaciones (Application).

Paginación y filtros en listados de ofertas y postulaciones, optimizados con índices en PostgreSQL.

Configuración de entornos separada (base.py, development.py, production.py) y variables de entorno para credenciales sensibles.

Seguridad preparada para producción: SECRET_KEY externa, HSTS, redirección a HTTPS, cookies de sesión y CSRF seguras, CSP con django-csp y URL de admin no trivial.

Observabilidad en desarrollo con django-debug-toolbar para analizar consultas SQL y evitar problemas de rendimiento.

Arquitectura de la solución
La arquitectura sigue un modelo de tres capas:

Frontend: SPA en React + TypeScript + Tailwind (proyecto jobboard-frontend), que consume la API mediante HTTP/JSON.

Backend: Django + Django REST Framework (jobboard-backend), encargado de la lógica de negocio, autenticación, autorización, validaciones y serialización de datos.

Base de datos: PostgreSQL, con índices diseñados para soportar búsquedas y listados frecuentes (ofertas activas, postulaciones por candidato y empresa).

Se recomienda exportar y añadir al repositorio (carpeta docs/) al menos:

Un diagrama de arquitectura (Frontend → API Django → PostgreSQL).

Un diagrama de modelo de datos (User, CompanyProfile, CandidateProfile, Job, Application y sus relaciones).

Modelo de datos (resumen)
Entidades principales del backend:

User: usuario base del sistema (candidato, empresa o admin), con email, contraseña hasheada, nombre completo, rol y flags de actividad.

CandidateProfile: datos del candidato (teléfono, ubicación, resumen, CV, habilidades).

CompanyProfile: datos públicos de la empresa (nombre, descripción, sitio web, ubicación, logo, sector).

Job: oferta de trabajo publicada por una empresa, con título, descripción, ubicación, salario opcional, nivel/modadlidad, estado (is_active) y fechas de publicación/creación.

Application: postulación de un candidato a una oferta, con estado (PENDING, ACCEPTED, REJECTED), carta de presentación opcional y timestamps.

Se han añadido índices en campos clave como:

Job.is_active, Job.company, Job.location, Job.created_at, con índices compuestos para filtros habituales (por ejemplo, ofertas activas por ubicación o por empresa).

Application.job, Application.candidate, Application.status, Application.created_at, con índices compuestos para listar postulaciones por oferta, candidato y estado de forma eficiente.

Stack tecnológico
Lenguaje: Python 3.x

Framework web: Django 6

API REST: Django REST Framework

Autenticación: JWT con djangorestframework-simplejwt

Base de datos: PostgreSQL

Gestión de variables de entorno: python-dotenv

Seguridad adicional: django-csp (Content Security Policy)

Depuración en desarrollo: django-debug-toolbar

Requisitos previos
Antes de ejecutar el proyecto en local necesitas:

Python 3.x instalado.

PostgreSQL instalado y con un usuario con permisos para crear bases de datos.

Git para clonar el repositorio.

(Opcional) Un entorno virtual de Python (recomendado).

Configuración del entorno
Clonar el repositorio:

bash
git clone https://github.com/tu-usuario/jobboard-backend.git
cd jobboard-backend
Crear y activar entorno virtual (ejemplo con venv):

bash
python -m venv venv
# Windows (PowerShell)
.\venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
Instalar dependencias:

bash
pip install -r requirements.txt
Crear base de datos en PostgreSQL (ejemplo):

sql
CREATE DATABASE jobboard_db;
CREATE USER jobboard_user WITH PASSWORD 'tu_password_segura';
GRANT ALL PRIVILEGES ON DATABASE jobboard_db TO jobboard_user;
Crear archivo .env en la raíz del proyecto (junto a manage.py):

text
# Entorno
DJANGO_ENV=development

# Clave secreta (usa una clave larga y aleatoria)
SECRET_KEY=pon_aqui_una_clave_larga_y_segura

# Base de datos
DB_NAME=jobboard_db
DB_USER=jobboard_user
DB_PASSWORD=tu_password_segura
DB_HOST=localhost
DB_PORT=5432
Para producción, se recomienda definir estas variables directamente en el entorno del servidor (no usar .env plano) y cambiar DJANGO_ENV=production.

Cómo ejecutar en local
Con el entorno virtual activado y el .env configurado:

Aplicar migraciones:

bash
python manage.py migrate
Crear superusuario (para acceder al panel de administración):

bash
python manage.py createsuperuser
Levantar el servidor de desarrollo:

bash
python manage.py runserver
El backend quedará disponible en:

http://127.0.0.1:8000/ (raíz).

Panel de administración (ruta personalizada): http://127.0.0.1:8000/super-panel-2025/.

Endpoints principales (resumen)
Los endpoints siguen el prefijo /api/ para recursos y /api/auth/ para autenticación:

Autenticación

POST /api/auth/register/ – Registro de usuario (candidato o empresa).

POST /api/auth/login/ – Obtención de tokens JWT (access y refresh).

POST /api/auth/refresh/ – Renovación de token de acceso.

GET /api/auth/me/ – Datos del usuario autenticado.

Ofertas de trabajo (Jobs)

GET /api/jobs/ – Listado paginado de ofertas activas.

POST /api/jobs/ – Crear oferta (empresa autenticada).

GET /api/jobs/{id}/ – Detalle de oferta.

PUT/PATCH /api/jobs/{id}/ – Actualizar oferta propia.

DELETE /api/jobs/{id}/ – Cerrar/eliminar oferta.

Postulaciones (Applications)

POST /api/applications/ – Crear postulación para una oferta.

GET /api/applications/ – Listado de postulaciones (filtrado según rol: candidato/empresa).

PATCH /api/applications/{id}/ – Actualizar estado (empresa).

Empresas (Companies)

GET /api/companies/ – Listado de empresas.

GET /api/companies/{id}/ – Detalle de empresa.

PUT/PATCH /api/companies/{id}/ – Actualizar perfil de empresa propia.

(La implementación concreta de rutas puede variar según los routers de DRF; se recomienda documentar en la wiki o añadir enlaces a la documentación interactiva si se usa Swagger/Redoc).

Entornos y seguridad
El proyecto está preparado para separar claramente desarrollo y producción:

base.py: configuración común (apps, middlewares, base de datos, DRF, etc.).

development.py: DEBUG=True, toolbar de depuración, flags de seguridad relajados para trabajar en local.

production.py: DEBUG=False, ALLOWED_HOSTS configurado, HSTS (SECURE_HSTS_SECONDS), SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, CSP (django-csp) y cabeceras de seguridad activas.

En producción, se recomienda:

Servir siempre sobre HTTPS.

Configurar las variables de entorno (SECRET_KEY, datos de DB, DJANGO_ENV=production) en el proveedor de hosting.

Usar un servidor WSGI/ASGI de producción (por ejemplo, gunicorn/uvicorn) detrás de un proxy inverso (Nginx, etc.).

Desarrollo y depuración
En entorno de desarrollo:

django-debug-toolbar está disponible en http://127.0.0.1:8000/__debug__/ (se inyecta automáticamente en las páginas HTML), permitiendo ver:

Número de consultas SQL por request.

Tiempo de ejecución de cada consulta (útil para detectar problemas de N+1).

Información sobre cache, señales y configuración.

Se recomienda revisar especialmente los endpoints de listados (/api/jobs/, /api/applications/) y aplicar select_related / prefetch_related según evolucione el modelo de datos.

Cómo contribuir / flujo de trabajo con Git
Para mantener un historial limpio y profesional:

Usar main como rama estable.

Para nuevas funcionalidades, crear ramas de feature a partir de main, por ejemplo:

feature/auth-api

feature/jobs-filtering

feature/company-dashboard

Mantener commits pequeños y descriptivos, usando el imperativo:

feat: add job list endpoint

fix: validate application status transitions

chore: configure csp middleware

