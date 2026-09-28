from html.parser import HTMLParser

import pytest
from fastapi.testclient import TestClient

from main import app, PAGES

client = TestClient(app)


class PageStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.labels = []
        self.h1 = 0
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, "Duplicate id"
            self.ids.add(attrs["id"])
        self.h1 += tag == "h1"
        self.references.extend(attrs.get("aria-describedby", "").split())
        if tag == "label":
            self.labels.append(attrs["for"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))


@pytest.mark.parametrize("path", PAGES)
def test_pages_have_valid_navigation_and_structure(path):
    response = client.get(path)
    assert response.status_code == 200
    assert '<html lang="es-MX">' in response.text
    page = PageStructure()
    page.feed(response.text)
    assert page.h1 == 1
    assert all(ref in page.ids for ref in page.references + page.labels)
    for link in page.links:
        if link.startswith("/"):
            assert link.split("#")[0] in PAGES
        elif link.startswith("#"):
            assert link[1:] in page.ids


def test_errors_are_linked_and_valid_fields_preserved():
    response = client.post("/oportunidades", data={"nombre": "Alex", "perfil": "desconocido", "modalidad": "remota"})
    assert response.status_code == 422
    assert 'value="Alex"' in response.text
    assert 'value="remota" selected' in response.text
    assert 'href="#perfil"' in response.text
    assert 'id="perfil-error"' in response.text
    assert 'aria-invalid="true"' in response.text
    page = PageStructure()
    page.feed(response.text)
    assert all(ref in page.ids for ref in page.references)


def test_valid_post_is_explicitly_a_demo_and_does_not_echo_name():
    response = client.post("/oportunidades", data={"nombre": "Nombre privado", "perfil": "pruebas", "modalidad": "hibrida"})
    assert response.status_code == 200
    assert "Has completado la demostración" in response.text
    assert "No se guardó una candidatura" in response.text
    assert "Nombre privado" not in response.text
    assert response.headers["cache-control"] == "no-store"


def test_untrusted_input_is_escaped():
    response = client.post("/oportunidades", data={"nombre": '<script>alert(1)</script>', "perfil": "", "modalidad": ""})
    assert response.status_code == 422
    assert '<script>alert(1)</script>' not in response.text
    assert '&lt;script&gt;' in response.text


def test_oversized_request_has_readable_error():
    response = client.post("/oportunidades", data={"nombre": "a" * 9000})
    assert response.status_code == 413
    assert "demasiado extensa" in response.text


def test_too_many_fields_and_wrong_content_type_are_handled():
    response = client.post("/oportunidades", data={f"f{i}": "x" for i in range(21)})
    assert response.status_code == 400
    assert client.post("/oportunidades", json={"nombre": "Alex"}).status_code == 415


def test_static_assets_and_missing_page():
    for path in ("/assets/styles.css", "/assets/site.js", "/assets/favicon.svg"):
        assert client.get(path).status_code == 200
    response = client.get("/no-existe")
    assert response.status_code == 404
    assert "Página no encontrada" in response.text
