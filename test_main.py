from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_translate_happy_path():
    # mock model+tokenizer so we don't download real model
    with patch("main.get_model_and_tokenizer") as mock_get:
        mock_tokenizer = type("T", (), {
            "decode": lambda self, x, skip_special_tokens=True: "שלום",
            "__call__": lambda self, text, **kw: {"input_ids": [[1,2,3]]}
        })()
        mock_model = type("M", (), {
            "generate": lambda self, **kw: [[1,2,3]]
        })()
        mock_get.return_value = (mock_tokenizer, mock_model)

        resp = client.post("/translate", json={
            "source_lang": "en",
            "target_lang": "he",
            "text": "hello"
        })
    assert resp.status_code == 200
    assert resp.json()["translation"] == "שלום"


def test_translate_missing_text():
    resp = client.post("/translate", json={
        "source_lang": "en",
        "target_lang": "he",
        "text": ""
    })
    assert resp.status_code == 400


def test_translate_unsupported_lang_pair():
    resp = client.post("/translate", json={
        "source_lang": "ru",
        "target_lang": "he",
        "text": "привет"
    })
    assert resp.status_code == 400
    assert "Unsupported language pair" in resp.json()["detail"]


def test_translate_internal_error():
    # make translate_text blow up
    with patch("main.translate_text", side_effect=Exception("boom")):
        resp = client.post("/translate", json={
            "source_lang": "en",
            "target_lang": "he",
            "text": "hello"
        })
    assert resp.status_code == 500
    assert resp.json()["detail"] == "Translation failed"
