# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# ✅ Copy backend requirements from repo root context
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy backend app code from repo root context
COPY backend/app ./app

# ✅ Copy curated open-data pack
COPY data/processed /data/processed

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
