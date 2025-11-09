from fastapi.testclient import TestClient
from main import app  # make sure this matches your filename

client = TestClient(app)


def test_translate_success():
    """Basic test that checks translation endpoint returns 200 and a translation field"""
    payload = {
        "source_lang": "en",
        "target_lang": "he",
        "text": "This is a test"
    }

    response = client.post("/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "translation" in data
    assert isinstance(data["translation"], str)
    assert len(data["translation"]) > 0


def test_missing_langs():
    """Should return 422 when missing source or target language"""
    response = client.post("/translate", json={"text": "Hello"})
    assert response.status_code == 422
    assert "source_lang" in response.text or "target_lang" in response.text


def test_empty_text():
    """Should return 400 for empty text"""
    payload = {"source_lang": "en", "target_lang": "he", "text": "   "}
    response = client.post("/translate", json=payload)
    assert response.status_code == 400
    assert "text must not be empty" in response.text


def test_unsupported_lang():
    """Should return 400 for unsupported language pair"""
    payload = {"source_lang": "fr", "target_lang": "ru", "text": "bonjour"}
    response = client.post("/translate", json=payload)
    assert response.status_code == 400
    assert "Unsupported language pair" in response.text
