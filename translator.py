from transformers import MarianTokenizer, MarianMTModel

def translate_text(src_lang, tgt_lang, text):
    '''
    loads the correct Helsinki-NLP model (Helsinki-NLP/opus-mt-he-ru or Helsinki-NLP/opus-mt-en-he)
    Uses Hugging Face transformers (MarianTokenizer, MarianMTModel)
    Returns the translated text as a string
    '''
    # map language pairs to model names
    model_map = {
        ("he", "ru"): "Helsinki-NLP/opus-mt-he-ru",
        ("en", "he"): "Helsinki-NLP/opus-mt-en-he"
    }

    # validate input
    model_name = model_map.get((src_lang, tgt_lang))
    if model_name is None:
        raise ValueError(f"Unsupported language pair: {src_lang} → {tgt_lang}")
    
    # load model and tokenizer
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # tokenize and translate
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = model.generate(**inputs)

    # decode and return translated text
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text

if __name__ == "__main__":
    print("Hebrew → Russian:", translate_text("he", "ru", "שלום עולם"))
    print("English → Hebrew:", translate_text("en", "he", "Good morning"))
