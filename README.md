# OriginAI Translation Service
A Dockerized REST API for translating text using Helsinki-NLP MarianMT models. Supports Hebrew → Russian and English → Hebrew translations with Hugging Face Transformers.

## Features
* App is built in a Docker container
* It preloads the model upon startup to avoid slowing down or racing
* Uses a lock to make loaded models thread safe
* It limits user input
* It checks whether user filled the correct request
* It raises errors such as 400 for value erros and 500 for any other case

## Build and run
``` bash
docker build -t originai-translator .
docker run -p 8000:8000 originai-translator
```


After running, open a second terminal and send a post request:
``` bash 
$r = Invoke-RestMethod -Uri "http://localhost:8000/translate" `
>>   -Method POST `
>>   -Headers @{ "Content-Type" = "application/json" } `
>>   -Body '{"source_lang": "en", "target_lang": "he", "text": "This is a test, my name is Nicole"}'
$r.translation
```
Or use the Swagger UI:
```bash
http://localhost:8000/docs
```

You’ll get a JSON response:

``` json 
{
  "translation": "זה מבחן, קוראים לי ניקול."
}
```

## Testing
Run with the following command after building:
``` bash
docker run -it --rm originai-translator pytest -v -W ignore::DeprecationWarning
```