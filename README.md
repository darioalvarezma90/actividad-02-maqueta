# Actividad 02 - Maqueta IncluTech

Sitio académico de **Diseñar para compartir**, desarrollado con FastAPI y Jinja2.

## Publicar en Koyeb (opción principal)

El servicio usa el Dockerfile incluido. FastAPI sirve las seis páginas, el formulario
y `/assets/`; no necesita Firebase, base de datos ni almacenamiento persistente.

En Koyeb crea un Web Service desde este repositorio de GitHub con estos valores:

| Parámetro | Valor |
| --- | --- |
| Repositorio | `darioalvarezma90/actividad-02-maqueta` |
| Rama | `main` |
| Builder | Dockerfile |
| Dockerfile / contexto | `Dockerfile` / raíz del repositorio |
| Instancia | Free |
| Región | Washington, D.C. (`was`) o Frankfurt (`fra`) |
| Variable de entorno | `PORT=8080` |
| Puerto público del servicio | `8080`, protocolo HTTP |
| Ruta | `/` hacia el puerto `8080` |
| Health check | HTTP, puerto `8080`, ruta `/` |
| Comando | Usar el CMD del Dockerfile (`python main.py`) |

La instancia Free tiene 512 MB de RAM, está limitada a una por organización y se
suspende tras una hora sin tráfico. Si no aparece Free, revisa si ya existe otra
instancia gratuita; no selecciones un tamaño de pago como sustituto.

Koyeb proporciona una URL HTTPS `*.koyeb.app`. Con el despliegue automático activo,
los pushes posteriores a `main` construyen y publican una nueva versión.

Documentación: [GitHub y Dockerfile](https://www.koyeb.com/docs/build-and-deploy/deploy-with-git),
[instancia gratuita](https://www.koyeb.com/docs/reference/instances).

## Ejecutar con Docker

Requiere Docker Desktop con contenedores Linux y Docker Compose.

```powershell
docker compose up -d --build --wait
docker compose ps
```

Abre http://localhost:8080. El contenedor usa Python 3.11, escucha en el puerto
interno 8080 y se ejecuta como usuario sin privilegios. Compose comprueba la
respuesta de `/`, utiliza un sistema de archivos de solo lectura y permite
escribir temporales en `/tmp`.

```powershell
docker compose logs --tail=100 web
docker compose down
```

Para cambiar únicamente el puerto publicado:

```powershell
$env:HOST_PORT = "8081"
docker compose up -d --build --wait
```

También puedes copiar `.env.example` a `.env` y configurar `HOST_PORT` y
`BIND_ADDRESS`. Compose lee ese archivo; el servicio Python no lo carga.
La interfaz predeterminada es `127.0.0.1`.

## Ejecutar en Windows sin Docker

Utiliza Python 3.11 o posterior. El contenedor permite verificar con Python 3.11.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Abre http://127.0.0.1:8000. Si ejecutas `python main.py`, el servicio escucha en
`0.0.0.0` y usa la variable `PORT`, con 8080 como valor predeterminado. Cloud Run
inyecta esa variable automáticamente.

## Alternativa: Firebase y Cloud Run

Requisitos:

- Proyecto `actividad02001` con facturación vinculada (plan Blaze).
- Google Cloud CLI (`gcloud`) y Firebase CLI (`firebase`) instalados y autenticados.
- Permisos para habilitar APIs, construir imágenes y desplegar Cloud Run y Hosting.

Blaze permite cuotas gratuitas, pero no garantiza que el despliegue sea gratuito.
El límite de instancias que sigue limita el escalado; no establece un tope de gasto.

Desde la raíz del repositorio, inicia sesión cuando sea necesario:

```powershell
gcloud auth login
firebase login
```

Habilita las APIs necesarias:

```powershell
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --project actividad02001
```

En proyectos nuevos, la cuenta de servicio usada por Cloud Build necesita el rol
`roles/run.builder`. Consulta los requisitos oficiales y concede ese rol a la
cuenta de construcción del proyecto si todavía no lo tiene.

Construye y despliega el backend. `--source .` usa el Dockerfile incluido:

```powershell
gcloud run deploy inclutech-api --source . --project actividad02001 --region us-central1 --allow-unauthenticated --port 8080 --min-instances 0 --max-instances 1 --memory 512Mi --cpu 1
```

Comprueba la URL que devuelve Cloud Run antes de publicar Hosting. Después:

```powershell
firebase deploy --only hosting --project actividad02001
```

La URL prevista de Hosting es https://actividad02001.web.app; estará disponible
con la aplicación después de completar ambos despliegues. Para actualizar código
Python o plantillas repite el despliegue de Cloud Run. Para actualizar recursos
de `public/assets`, repite ambos despliegues para conservarlos sincronizados.

`.dockerignore` limita el contexto de Docker y `.gcloudignore` limita los archivos
que se suben a Cloud Build. `.env`, `.venv`, `.git`, registros, pruebas y herramientas
locales quedan fuera. Hosting publica exclusivamente el directorio `public`.

### Si Google devuelve BILLING_DISABLED

Comprueba en la consola que el proyecto tenga una cuenta de facturación vinculada
**y que esa cuenta esté activa**. Una cuenta cerrada puede seguir vinculada al
proyecto y bloquear Artifact Registry. Reactiva la cuenta o vincula otra activa,
espera a que se propague el cambio y repite el despliegue de Cloud Run. Publica
Hosting únicamente después de verificar el backend.

## Comprobación

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas revisan las seis páginas, navegación, referencias de accesibilidad,
validación del formulario, conservación de respuestas, escape de HTML, límites
de solicitudes y recursos estáticos. No sustituyen una auditoría WCAG.

Tras desplegar, comprueba `/`, `/servicios`, `/modelo`, `/oportunidades`, `/contacto`
y `/accesibilidad`, además de `/assets/styles.css`, `/assets/site.js` y
`/assets/favicon.svg`. Envía una postulación inválida y una válida. Una ruta
inexistente debe devolver 404.

## Alcance

La postulación es demostrativa: nombre ficticio, área de interés y modalidad.
No hay vacantes reales, envío de correo, base de datos ni almacenamiento persistente.
La aplicación no escribe los datos del formulario en registros o archivos.
El proveedor de hosting puede conservar sus propios registros de acceso.

## Referencias

- [Firebase Hosting con Cloud Run](https://firebase.google.com/docs/hosting/cloud-run)
- [Desplegar Cloud Run desde código fuente y permisos necesarios](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [Instalar Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install-sdk)
- [Firebase CLI](https://firebase.google.com/docs/cli)
