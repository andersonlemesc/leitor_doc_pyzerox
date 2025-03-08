FROM python:3.13-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  FLASK_APP=main.py \
  FLASK_ENV=production \
  WORKERS=4 \
  TIMEOUT=120 \
  AI_PROVIDER=openai

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  poppler-utils\
  graphicsmagick \
  ghostscript \
  build-essential \
  git \
  cmake \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p uploads models && chmod 777 uploads models

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies and gunicorn
# Força a instalação das dependências principais sem as opcionais
RUN pip install --no-cache-dir -r requirements.txt

# Argumento para instalar dependências para modelos específicos
ARG INSTALL_LLAMA=false
ARG CUDA_VERSION=none

# Instalar llama-cpp-python se necessário com suporte a CUDA (opcional)
RUN if [ "$INSTALL_LLAMA" = "true" ] && [ "$CUDA_VERSION" != "none" ]; then \
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --no-cache-dir llama-cpp-python; \
  elif [ "$INSTALL_LLAMA" = "true" ]; then \
    pip install --no-cache-dir llama-cpp-python; \
  fi

# Argumentos para instalar bibliotecas específicas de cada provedor
ARG INSTALL_ANTHROPIC=true
ARG INSTALL_GEMINI=true
ARG INSTALL_GROK=false

# Instala bibliotecas adicionais conforme necessário
RUN if [ "$INSTALL_ANTHROPIC" = "true" ]; then pip install --no-cache-dir anthropic>=0.8.0; fi && \
    if [ "$INSTALL_GEMINI" = "true" ]; then pip install --no-cache-dir google-generativeai>=0.3.0; fi

# Copy the rest of the application
COPY . .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run gunicorn with environment variables
CMD gunicorn --bind 0.0.0.0:5000 --workers ${WORKERS} --timeout ${TIMEOUT} main:app

