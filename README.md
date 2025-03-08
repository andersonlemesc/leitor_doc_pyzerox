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

#### Parâmetros de consulta:
- `ocr` - Ativar/desativar OCR para PDFs (padrão: true)
- `ai_provider` - Provedor de IA a ser usado: openai, gemini, anthropic, llama_local (padrão: openai)

#### Provedores e suporte a OCR/imagens:
- **OpenAI**: Suporta OCR e processamento de imagens (`ocr=true`)
- **Gemini**: Suporta OCR e processamento de imagens (`ocr=true`)
- **Anthropic Claude**: Suporta OCR e processamento de imagens (`ocr=true`)
- **Llama Local**: Suporte limitado, melhor para texto (`ocr=false`)

#### Exemplos por tipo de documento:

##### PDF (com OCR - OpenAI, Gemini, Claude)
```bash
curl -X POST \
  -H "Content-Type: application/pdf" \
  --data-binary "@seu_documento.pdf" \
  "http://localhost:5000/convert?ocr=true&ai_provider=openai"
```

##### Excel
```bash
curl -X POST \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  --data-binary "@seu_documento.xlsx" \
  "http://localhost:5000/convert?ai_provider=openai"
```

##### Word
```bash
curl -X POST \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  --data-binary "@seu_documento.docx" \
  "http://localhost:5000/convert?ai_provider=gemini"
```

##### PowerPoint
```bash
curl -X POST \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation" \
  --data-binary "@sua_apresentacao.pptx" \
  "http://localhost:5000/convert?ai_provider=anthropic"
```

##### Imagem (JPEG)
```bash
curl -X POST \
  -H "Content-Type: image/jpeg" \
  --data-binary "@sua_imagem.jpg" \
  "http://localhost:5000/convert?ai_provider=openai"
```

##### Imagem (PNG)
```bash
curl -X POST \
  -H "Content-Type: image/png" \
  --data-binary "@sua_imagem.png" \
  "http://localhost:5000/convert?ai_provider=gemini"
```

##### HTML
```bash
curl -X POST \
  -H "Content-Type: text/html" \
  --data-binary "@seu_arquivo.html" \
  "http://localhost:5000/convert?ai_provider=openai"
```

##### CSV
```bash
curl -X POST \
  -H "Content-Type: text/csv" \
  --data-binary "@seus_dados.csv" \
  "http://localhost:5000/convert?ai_provider=openai"
```

##### JSON
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data-binary "@seus_dados.json" \
  "http://localhost:5000/convert?ai_provider=openai"
```

##### XML
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  --data-binary "@seus_dados.xml" \
  "http://localhost:5000/convert?ai_provider=openai"
```

##### ZIP (contendo múltiplos arquivos)
```bash
curl -X POST \
  -H "Content-Type: application/zip" \
  --data-binary "@seus_arquivos.zip" \
  "http://localhost:5000/convert?ai_provider=openai"
```

## ✨ Features

- Convert multiples files to Markdown (PDF, PowerPoint, Word, Excel, Images, Audio, HTML, CSV, JSON, XML and ZIP).
- OCR for PDF files (com OpenAI, Gemini e Claude).
- Simple REST API interface
- Docker support
- Easy deployment with Docker Stack
- **Novo:** Suporte a múltiplos provedores de IA (OpenAI, Gemini, Claude e Llama local)

## 🤖 Provedores de IA Suportados

Leitor Doc PyZerox agora suporta vários provedores de IA para processamento OCR e conversão de documentos:

1. **OpenAI (Padrão)** - GPT-4o Mini ou outros modelos da OpenAI - Suporta OCR e processamento de imagens
2. **Google Gemini** - Excelente alternativa com boa relação custo-benefício - Suporta OCR e processamento de imagens
3. **Anthropic Claude** - Excelente para compreensão de documentos e processamento multimodal - Suporta OCR e processamento de imagens
4. **Llama Local** - Execute modelos localmente para privacidade total - Melhor para processamento de texto

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

O endpoint principal para conversão de documentos é:

```
POST /convert
```

Este endpoint aceita vários tipos de documentos e os converte para Markdown.

##### Parâmetros de consulta:
- `ocr` - Ativar/desativar OCR para PDFs (padrão: true)
  - Use `ocr=true` para OpenAI, Gemini e Claude (suportam processamento de imagens)
  - Use `ocr=false` para Llama (apenas processamento de texto)
- `ai_provider` - Provedor de IA a ser usado (padrão: openai)
  - Valores aceitos: openai, gemini, anthropic, llama_local

##### Tipos de documentos suportados:
- PDF: `application/pdf`
- Excel: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Word: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- PowerPoint: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- Imagens: `image/jpeg`, `image/png`, `image/gif`
- HTML: `text/html`
- CSV: `text/csv`
- JSON: `application/json`
- XML: `application/xml`
- ZIP: `application/zip`
- Texto: `text/plain`

##### Exemplo de resposta:
```json
{
  "content": "# Título do Documento\n\nConteúdo convertido em Markdown...",
  "format": "pdf",
  "ocr": true,
  "ai_provider": "openai"
}
```

#### Health Check

```
GET /health
```

Retorna o status de saúde da API:

```json
{
  "status": "healthy"
}
```

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

| Modelo | Desempenho em OCR | Processamento de Imagens | Custo | Privacidade | Recomendação |
|--------|-------------------|-------------------------|-------|------------|--------------|
| OpenAI GPT-4o Mini | Excelente | Sim | Médio | Baixa | Ótimo desempenho geral |
| Claude 3 Sonnet | Excelente | Sim | Médio | Baixa | Melhor para documentos complexos |
| Gemini 1.0 Pro | Muito Bom | Sim | Baixo | Baixa | Melhor custo-benefício |
| Llama 3 (local) | Razoável | Não | Grátis | Alta | Melhor para privacidade |

## 🔧 Development

1. Clone the repository
2. Build the Docker image locally
3. Run tests
4. Submit pull requests

## 📝 License

[MIT License](https://opensource.org/licenses/MIT)

---

Made with ❤️ by Anderson Lemes
