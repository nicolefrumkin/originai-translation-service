FROM python:3.11-slim

WORKDIR /app

COPY . . 

RUN pip install -r requirements.txt
# pre-download models:
RUN python - << 'PY'
from transformers import MarianMTModel, MarianTokenizer
for m in ["Helsinki-NLP/opus-mt-en-he", "Helsinki-NLP/opus-mt-he-ru"]:
    MarianTokenizer.from_pretrained(m)
    MarianMTModel.from_pretrained(m)
PY

# Expose the FastAPI default port
EXPOSE 8000

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
