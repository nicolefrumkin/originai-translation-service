from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import MarianTokenizer, MarianMTModel

app = FastAPI()

MODEL_MAP = {
    ("he", "ru"): "Helsinki-NLP/opus-mt-he-ru",
    ("en", "he"): "Helsinki-NLP/opus-mt-en-he",
}

_loaded_models = {}

def get_model_and_tokenizer(src_lang, tgt_lang):
    key = (src_lang, tgt_lang)
    model_name = MODEL_MAP.get(key)
    if model_name is None:
        raise ValueError(f"Unsupported language pair: {src_lang} → {tgt_lang}")

    if model_name not in _loaded_models:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        _loaded_models[model_name] = (tokenizer, model)

    return _loaded_models[model_name]


def translate_text(src_lang: str, tgt_lang: str, text: str) -> str:
    tokenizer, model = get_model_and_tokenizer(src_lang, tgt_lang)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = model.generate(**inputs)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text


class TranslateRequest(BaseModel):
    source_lang: str
    target_lang: str
    text: str


class TranslateResponse(BaseModel):
    translation: str


@app.post("/translate", response_model=TranslateResponse)
def translate_endpoint(req: TranslateRequest):
    if not req.source_lang or not req.target_lang:
        raise HTTPException(status_code=400, detail="source_lang and target_lang are required")

    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")

    try:
        result = translate_text(req.source_lang, req.target_lang, req.text)
        return TranslateResponse(translation=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:

        raise HTTPException(status_code=500, detail="Translation failed")