FROM python:3.11-slim

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY src/     ./src/
COPY agents/  ./agents/
COPY tools/   ./tools/
COPY data/    ./data/

# expose port
EXPOSE 8000

# start API
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
