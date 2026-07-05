FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy all interface Python modules. The .dockerignore excludes .venv,
# __pycache__, tests, *.db, and .env so only source modules are included.
COPY *.py ./

EXPOSE 8501
CMD ["uv", "run", "--no-sync", "streamlit", "run", "app.py", \
     "--server.port", "8501", "--server.address", "0.0.0.0"]
