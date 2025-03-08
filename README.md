# Leitor Doc PyZerox

[![Docker Pulls](https://img.shields.io/docker/pulls/andersonlemes/leitor_doc_pyzerox)](https://hub.docker.com/r/andersonlemes/leitor_doc_pyzerox)
[![Docker Image Size](https://img.shields.io/docker/image-size/andersonlemes/leitor_doc_pyzerox)](https://hub.docker.com/r/andersonlemes/leitor_doc_pyzerox)

Convert documents to Markdown format through a simple API service.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker run -d -p 5000:5000 andersonlemes/leitor_doc_pyzerox:latest
```

### API Usage

Convert a document to Markdown:

```bash
curl -X POST \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  --data-binary "@your_document.xlsx" \
  http://localhost:5000/convert
```

Especificar o provedor de IA:

```bash
curl -X POST \
  -H "Content-Type: application/pdf" \
  --data-binary "@your_document.pdf" \
  "http://localhost:5000/convert?ai_provider=gemini"
```

## ✨ Features

- Convert multiples files to Markdown (PDF, PowerPoint, Word, Excel, Images, Audio, HTML, CSV, JSON, XML and ZIP).
- OCR for PDF files.
- Simple REST API interface
- Docker support
- Easy deployment with Docker Stack
- **Novo:** Suporte a múltiplos provedores de IA (OpenAI, Gemini, Claude, DeepSeek, Grok e Llama local)

## 🤖 Provedores de IA Suportados

Leitor Doc PyZerox agora suporta vários provedores de IA para processamento OCR e conversão de documentos:

1. **OpenAI (Padrão)** - GPT-4o Mini ou outros modelos da OpenAI
2. **Google Gemini** - Excelente alternativa com boa relação custo-benefício
3. **Anthropic Claude** - Excelente para compreensão de documentos e processamento multimodal
4. **DeepSeek** - Bom desempenho em processamento de documentos
5. **Grok (xAI)** - Alternativa competitiva
6. **Llama Local** - Execute modelos localmente para privacidade total

## 🛠️ Installation

### Using Docker Hub

1. Pull the image:

```bash
docker pull andersonlemes/leitor_doc_pyzerox:latest
```

2. Run the container:

```bash
docker run -d -p 5000:5000 andersonlemes/leitor_doc_pyzerox:latest
```

## 💻 Usage

### API Endpoints

#### Convert Document

```bash
curl -X POST \
 -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
 --data-binary "@your_document.xlsx" \
 http://localhost:5000/convert?ocr=true/false&ai_provider=openai
```

Parâmetros de consulta:
- `ocr` - Ativar/desativar OCR para PDFs (padrão: true)
- `ai_provider` - Provedor de IA a ser usado: openai, gemini, anthropic, deepseek, grok, llama_local (padrão: openai)

## 📦 Deployment

### Docker Compose para cada Provedor

#### OpenAI (Padrão)

```yaml
version: "3.7"
services:
  leitor_doc_pyzerox:
    image: andersonlemes/leitor_doc_pyzerox:latest
    environment:
      - AI_PROVIDER=openai
      - OPENAI_API_KEY=sk-your-api-key
      - OPENAI_MODEL=gpt-4o-mini
      - WORKERS=4
      - TIMEOUT=0
    ports:
      - "5000:5000"
```

#### Google Gemini

```yaml
version: "3.7"
services:
  leitor_doc_pyzerox:
    image: andersonlemes/leitor_doc_pyzerox:latest
    build:
      context: .
      args:
        - INSTALL_GEMINI=true
    environment:
      - AI_PROVIDER=gemini
      - GEMINI_API_KEY=your-gemini-api-key
      - GEMINI_MODEL=gemini-1.5-pro
      - WORKERS=4
      - TIMEOUT=0
    ports:
      - "5000:5000"
```

#### Anthropic Claude

```yaml
version: "3.7"
services:
  leitor_doc_pyzerox:
    image: andersonlemes/leitor_doc_pyzerox:latest
    build:
      context: .
      args:
        - INSTALL_ANTHROPIC=true
    environment:
      - AI_PROVIDER=anthropic
      - ANTHROPIC_API_KEY=your-anthropic-api-key
      - ANTHROPIC_MODEL=claude-3-sonnet-20240229
      - WORKERS=4
      - TIMEOUT=0
    ports:
      - "5000:5000"
```

#### DeepSeek

```yaml
version: "3.7"
services:
  leitor_doc_pyzerox:
    image: andersonlemes/leitor_doc_pyzerox:latest
    build:
      context: .
      args:
        - INSTALL_DEEPSEEK=true
    environment:
      - AI_PROVIDER=deepseek
      - DEEPSEEK_API_KEY=your-deepseek-api-key
      - DEEPSEEK_MODEL=deepseek-vl
      - WORKERS=4
      - TIMEOUT=0
    ports:
      - "5000:5000"
```

#### Grok

```yaml
version: "3.7"
services:
  leitor_doc_pyzerox:
    image: andersonlemes/leitor_doc_pyzerox:latest
    build:
      context: .
      args:
        - INSTALL_GROK=true
    environment:
      - AI_PROVIDER=grok
      - GROK_API_KEY=your-grok-api-key
      - GROK_MODEL=grok-2
      - WORKERS=4
      - TIMEOUT=0
    ports:
      - "5000:5000"
```

#### Llama Local

```yaml
version: "3.7"
services:
  leitor_doc_pyzerox:
    image: andersonlemes/leitor_doc_pyzerox:latest
    build:
      context: .
      args:
        - INSTALL_LLAMA=true
        # Descomente para habilitar suporte a CUDA (GPU)
        # - CUDA_VERSION=11.8
    environment:
      - AI_PROVIDER=llama_local
      - LLAMA_MODEL_PATH=/app/models/llama-3-8b.gguf
      - LLAMA_N_CTX=4096
      - LLAMA_N_GPU_LAYERS=-1
      - WORKERS=4
      - TIMEOUT=0
    volumes:
      # Monte seu modelo local no contêiner
      - ./models:/app/models
    ports:
      - "5000:5000"
    deploy:
      resources:
        reservations:
          # Descomente para utilizar GPU
          # devices:
          #  - driver: nvidia
          #    count: 1
          #    capabilities: [gpu]
```

### Docker Stack Deployment

Deploy using [Docker Stack](stack.yml):

```bash
docker stack deploy --prune --resolve-image always -c stack.yml leitor_doc_pyzerox
```

## 🦙 Usando modelos Llama localmente

Para usar modelos Llama localmente:

1. Baixe um modelo GGUF compatível (recomendamos Llama 3 8B ou maior)
2. Coloque o modelo na pasta `/models` do seu projeto
3. Configure seu `docker-compose.yml` conforme o exemplo acima
4. Inicie o contêiner com `docker-compose up -d`

Os modelos Llama requerem uma GPU para melhor desempenho. Descomente as configurações de GPU no arquivo Docker Compose para habilitar o suporte a CUDA.

## 🧪 Comparação dos Modelos

| Modelo | Desempenho em OCR | Custo | Privacidade | Multimodal | Recomendação |
|--------|-------------------|-------|------------|------------|--------------|
| OpenAI GPT-4o Mini | Excelente | Médio | Baixa | Sim | Ótimo desempenho geral |
| Claude 3 Sonnet | Excelente | Médio | Baixa | Sim | Melhor para documentos complexos |
| Gemini 1.5 Pro | Muito Bom | Baixo | Baixa | Sim | Melhor custo-benefício |
| DeepSeek VL | Bom | Baixo | Baixa | Sim | Alternativa econômica |
| Grok-2 | Bom | Médio | Baixa | Não | Bom para textos |
| Llama 3 (local) | Razoável | Grátis | Alta | Não | Melhor para privacidade |

## 🔧 Development

1. Clone the repository
2. Build the Docker image locally
3. Run tests
4. Submit pull requests

## 📝 License

[MIT License](https://opensource.org/licenses/MIT)

---

Made with ❤️ by Anderson Lemes
