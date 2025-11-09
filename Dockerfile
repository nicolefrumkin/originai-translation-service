FROM python:3.11-slim

WORKDIR /app

COPY main.py .

RUN pip install --no-cache-dir fastapi uvicorn transformers torch sentencepiece sacremoses

# Expose the FastAPI default port
EXPOSE 8000

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
