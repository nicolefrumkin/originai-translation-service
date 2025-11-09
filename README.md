# originai-translation-service
A Dockerized REST API for translating text using Helsinki-NLP MarianMT models. Supports Hebrew → Russian and English → Hebrew translations with Hugging Face Transformers.


## Build and run
``` bash
docker build -t originai-translator .
docker run -p 8000:8000 originai-translator
```

After running, open a second terminal and write:
``` bash 
$r = Invoke-RestMethod -Uri "http://localhost:8000/translate" `
>>   -Method POST `
>>   -Headers @{ "Content-Type" = "application/json" } `
>>   -Body '{"source_lang": "en", "target_lang": "he", "text": "This is a test, my name is Nicole"}'
$r.translation
```
Or open the browser at the address:
```bash
http://localhost:8000/docs
```

You’ll get a JSON response:

``` json 
{"translation": "Привет, мир"}
```

## Testing
Run with:
``` bash
pytest -q
```