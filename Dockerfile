# Use a slim Python 3.10 image for performance
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (needed for some ML libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Expose FastAPI port
EXPOSE 8000

# Run the application using Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]