FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
