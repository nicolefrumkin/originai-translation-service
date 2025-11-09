# originai-translation-service
A Dockerized REST API for translating text using Helsinki-NLP MarianMT models. Supports Hebrew → Russian and English → Hebrew translations with Hugging Face Transformers.


## Build and run
``` bash
docker build -t translator-api .
docker run -p 8000:8000 translator-api
```

After running, open your browser or use curl:
``` bash 
POST http://localhost:8000/translate
Content-Type: application/json

{
  "source_lang": "he",
  "target_lang": "ru",
  "text": "שלום עולם"
}
```

You’ll get a JSON response:

``` json 
{"translation": "Привет, мир"}
```