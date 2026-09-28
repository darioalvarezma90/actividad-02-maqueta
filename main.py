"""Maqueta académica de IncluTech. No almacena ni transmite postulaciones."""
from urllib.parse import parse_qs

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from settings import BASE_DIR, HOST, PORT, LOG_LEVEL

BASE = BASE_DIR
app = FastAPI(title="IncluTech", docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/assets", StaticFiles(directory=BASE / "assets"), name="assets")
templates = Jinja2Templates(directory=BASE / "templates")

PAGES = {
    "/": ("inicio", "Inicio"),
    "/servicios": ("servicios", "Servicios"),
    "/modelo": ("modelo", "Nuestro modelo"),
    "/oportunidades": ("oportunidades", "Trabaja con nosotros"),
    "/contacto": ("contacto", "Contacto"),
    "/accesibilidad": ("accesibilidad", "Accesibilidad"),
}

PROFILES = {
    "documentos": "Documentos accesibles",
    "pruebas": "Pruebas de accesibilidad",
    "calidad": "Control de calidad digital",
    "explorar": "Quiero explorar mis opciones",
}


@app.middleware("http")
async def response_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.method == "POST":
        response.headers["Cache-Control"] = "no-store"
    return response


def render(request, page, title, status_code=200, **context):
    return templates.TemplateResponse(
        request=request,
        name=f"{page}.html",
        context={"page": page, "title": title, "profiles": PROFILES, **context},
        status_code=status_code,
    )


@app.get("/", response_class=HTMLResponse)
@app.get("/servicios", response_class=HTMLResponse)
@app.get("/modelo", response_class=HTMLResponse)
@app.get("/oportunidades", response_class=HTMLResponse)
@app.get("/contacto", response_class=HTMLResponse)
@app.get("/accesibilidad", response_class=HTMLResponse)
async def pages(request: Request):
    page, title = PAGES[request.url.path]
    return render(request, page, title, errors={}, values={}, success=False)


@app.post("/oportunidades", response_class=HTMLResponse)
async def application_demo(request: Request):
    # Limit the body before parsing. No database, file writes, email or outbound API.
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > 8192:
            return render(request, "error", "Solicitud demasiado extensa", 413,
                          message="La solicitud es demasiado extensa. Regresa al formulario y utiliza textos más breves.")
    if request.headers.get("content-type", "").split(";")[0] != "application/x-www-form-urlencoded":
        return render(request, "error", "Formato no compatible", 415,
                      message="Utiliza el formulario de la página de oportunidades para completar la demostración.")
    try:
        raw = parse_qs(body.decode("utf-8", errors="replace"), max_num_fields=20)
    except ValueError:
        return render(request, "error", "Solicitud no válida", 400,
                      message="La solicitud contiene demasiados campos. Vuelve al formulario para intentarlo otra vez.")
    values = {key: raw.get(key, [""])[0].strip() for key in ("nombre", "perfil", "modalidad")}
    errors = {}
    if not 2 <= len(values["nombre"]) <= 60:
        errors["nombre"] = "Escribe un nombre de ejemplo de entre 2 y 60 caracteres."
    if values["perfil"] not in PROFILES:
        errors["perfil"] = "Elige un área de interés de la lista."
    if values["modalidad"] not in ("remota", "hibrida", "cualquiera"):
        errors["modalidad"] = "Elige una modalidad para continuar."
    return render(request, "oportunidades", "Revisa tu postulación" if errors else "Demostración completada",
                  422 if errors else 200, errors=errors, values=values, success=not errors)


@app.exception_handler(404)
async def not_found(request: Request, exc):
    return render(request, "error", "Página no encontrada", 404,
                  message="Esta página no está disponible. Puedes volver al inicio o explorar nuestros servicios.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL)