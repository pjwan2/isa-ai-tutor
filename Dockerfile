# Use a stable Python base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🌟 Crucial: Copy the pre-built index, data, and code
COPY ./app ./app
COPY ./data ./data
COPY ./faiss_index ./faiss_index
COPY ./main.py .

# Expose port for FastAPI
EXPOSE 8080

# Launch the FastAPI app
CMD ["uvicorn", "app.main_api:app", "--host", "0.0.0.0", "--port", "8080"]