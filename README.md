# Actividad 02 - Maqueta IncluTech

Propuesta de sitio web para **Diseñar para compartir**, basada en el modelo de negocio inclusivo de empleados de IncluTech.

## Ejecutar con Docker

Requiere Docker Engine y Docker Compose. En Windows, inicia Docker Desktop con contenedores Linux.

Desde la carpeta del proyecto:

```powershell
docker compose up -d --build --wait
```

Abre http://localhost:8080. El puerto externo es 8080 para poder mantener abierta la ejecución local en el puerto 8000.

```powershell
# Estado y comprobación de salud
docker compose ps

# Consultar los registros
docker compose logs --tail=100 web

# Detener y retirar los contenedores de este proyecto
docker compose down
```

Para cambiar el puerto en PowerShell:

```powershell
$env:HOST_PORT = "8081"
docker compose up -d --build --wait
```

El contenedor utiliza Python 3.12, instala `requirements.txt` y ejecuta Uvicorn en el puerto interno 8000. Incluye las plantillas y los recursos estáticos. Se ejecuta con un usuario sin privilegios y comprueba periódicamente que la página de inicio responde. No necesita base de datos ni volúmenes persistentes. Al modificar el código, vuelve a ejecutar el comando con `--build`.

`.dockerignore` limita el contexto de construcción al código y los recursos de la aplicación. El documento Word, las capturas, el entorno virtual y los archivos personales no se incluyen en la imagen.

### Desplegar en un servidor con Docker

Copia los archivos del proyecto al servidor y ejecuta el mismo comando de Compose. La configuración predeterminada publica el puerto solo en la interfaz local; puede colocarse detrás de un proxy inverso con dominio y HTTPS. Si necesitas acceso directo desde otras máquinas, configura `BIND_ADDRESS=0.0.0.0` en el entorno del servidor y habilita el puerto externo en su firewall. `HOST_PORT` controla ese puerto, no el puerto interno de Uvicorn.

Si el proveedor solicita únicamente un Dockerfile, selecciona este archivo y configura el puerto de la aplicación en **8000**. El despliegue con Docker y el despliegue nativo en Vercel descrito más abajo son alternativas independientes.

También puedes ejecutar la imagen sin Compose:

```powershell
docker build -t inclutech-maqueta:local .
docker run -d --name inclutech-maqueta --restart unless-stopped -p 127.0.0.1:8080:8000 inclutech-maqueta:local
```

Usa una sola de las dos opciones a la vez para evitar ocupar el mismo puerto. Con la opción sin Compose, detén y retira el contenedor con `docker stop inclutech-maqueta` y `docker rm inclutech-maqueta`.

Referencia: [FastAPI en contenedores Docker](https://fastapi.tiangolo.com/deployment/docker/).

## Ejecutar en Windows

Requiere Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Visitar http://127.0.0.1:8000. También se puede crear el entorno con la ruta completa a un ejecutable Python 3.12 instalado.

## Publicar en Vercel Hobby

1. Subir los archivos del proyecto a un repositorio de GitHub. `.gitignore` excluye el entorno virtual, temporales y configuración local.
2. En Vercel, elegir **Add New → Project** e importar el repositorio desde el espacio personal con plan Hobby.
3. Usar la raíz del repositorio como **Root Directory** y **FastAPI** como framework. Mantener comandos y carpeta de salida predeterminados. No configurar un servidor Uvicorn permanente.
4. Desplegar. Vercel detecta `main.py` y su instancia `app`; `pyproject.toml` declara `main:app` y Python 3.12.
5. Abrir la URL de producción sin sesión iniciada o en una ventana privada. Revisar que la protección del despliegue no impida el acceso del profesor.
6. Comprobar las seis páginas, estilos, formulario inválido y confirmación válida en esa URL antes de usarla en el reporte.

No requiere variables de entorno, base de datos, correo ni almacenamiento persistente. Los recursos estáticos usan `/assets`; las plantillas se resuelven desde la ubicación de `main.py`.

La propuesta académica no realiza operaciones comerciales. Hobby está destinado al uso personal no comercial y sujeto a cuotas. El despliegue público no se ha realizado como parte de la preparación local.

Documentación:
- https://vercel.com/docs/frameworks/backend/fastapi
- https://vercel.com/docs/plans/hobby
- https://fastapi.tiangolo.com/advanced/templates/

## Comprobación local

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas revisan navegación, referencias de accesibilidad, validación, conservación de respuestas, escape de HTML, límites de solicitudes y recursos estáticos. No sustituyen pruebas con lectores de pantalla ni una auditoría WCAG.

## Alcance

- Inicio, servicios, modelo, oportunidades, contacto y accesibilidad.
- Postulación demostrativa: nombre ficticio, área de interés y modalidad.
- Validación en servidor, errores enlazados a los campos y confirmación explícita.
- Sin vacantes reales, correos, persistencia ni contacto comercial ficticio.
- Sin analítica, fuentes externas, cookies o servicios de terceros integrados.

El hosting puede mantener sus propios registros de acceso; la aplicación no escribe los datos del formulario en logs o archivos.

Consultar [PROPUESTA.md](PROPUESTA.md) para el concepto y las evidencias POUR previstas.

