"""
Providers de IA para Leitor Doc PyZerox
Este módulo gerencia diferentes provedores de IA que podem ser usados para o processamento OCR e conversão de documentos.
"""
import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

# Importações específicas para cada provedor com tratamento de erros
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from google.generativeai import configure as gemini_configure
    from google.generativeai import GenerativeModel
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import deepseek
    DEEPSEEK_AVAILABLE = True 
except ImportError:
    DEEPSEEK_AVAILABLE = False

try:
    # Grok API não está disponível publicamente ainda
    # Por enquanto, marcamos como indisponível
    # import grok_ai
    GROK_AVAILABLE = False
except ImportError:
    GROK_AVAILABLE = False

class AIProvider(ABC):
    """Classe base abstrata para provedores de IA"""
    
    @abstractmethod
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """
        Processa um documento usando o modelo de IA
        
        Args:
            text: Texto extraído do documento
            images: Lista de caminhos para imagens (opcional)
            prompt: Instruções específicas para o processamento
            
        Returns:
            Texto processado em formato markdown
        """
        pass
    
    @staticmethod
    def get_provider(provider_type: str = None) -> 'AIProvider':
        """
        Factory method para criar a instância do provedor apropriado
        
        Args:
            provider_type: Tipo de provedor a ser usado (openai, gemini, anthropic, etc.)
            
        Returns:
            Uma instância do provedor de IA apropriado
        """
        provider_type = provider_type or os.environ.get('AI_PROVIDER', 'openai').lower()
        
        if provider_type == 'openai':
            if not OPENAI_AVAILABLE:
                raise ImportError("A biblioteca OpenAI não está instalada. Instale com 'pip install openai'.")
            return OpenAIProvider()
        elif provider_type == 'gemini':
            if not GEMINI_AVAILABLE:
                raise ImportError("A biblioteca Google Generative AI não está instalada. Instale com 'pip install google-generativeai>=0.3.0'.")
            return GeminiProvider()
        elif provider_type == 'anthropic':
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("A biblioteca Anthropic não está instalada. Instale com 'pip install anthropic>=0.8.0'.")
            return AnthropicProvider()
        elif provider_type == 'deepseek':
            if not DEEPSEEK_AVAILABLE:
                raise ImportError("A biblioteca DeepSeek não está instalada. Instale com 'pip install deepseek'.")
            return DeepSeekProvider()
        elif provider_type == 'grok':
            raise NotImplementedError(
                "O provedor Grok não está disponível porque a API oficial não está "
                "disponível publicamente. Por favor, use outro provedor como OpenAI, Gemini ou Claude."
            )
        elif provider_type == 'llama_local':
            if not LLAMA_AVAILABLE:
                raise ImportError("A biblioteca Llama CPP não está instalada. Instale com 'pip install llama-cpp-python'.")
            return LlamaLocalProvider()
        else:
            raise ValueError(f"Provedor de IA não suportado: {provider_type}")


class OpenAIProvider(AIProvider):
    """Provedor usando a API da OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key)
        
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """Processa documento usando a API da OpenAI"""
        messages = [{"role": "system", "content": prompt or "Convert this document to markdown format."}]
        
        # Se tiver imagens, adiciona mensagem com as imagens
        if images and len(images) > 0:
            image_contents = []
            for img_path in images:
                with open(img_path, "rb") as img_file:
                    image_contents.append(
                        {
                            "type": "image_url", 
                            "image_url": {"url": f"data:image/jpeg;base64,{img_file.read().decode('latin1')}"}
                        }
                    )
            messages.append({"role": "user", "content": [{"type": "text", "text": text}, *image_contents]})
        else:
            messages.append({"role": "user", "content": text})
            
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        )
        
        return response.choices[0].message.content


class GeminiProvider(AIProvider):
    """Provedor usando a API do Google Gemini"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        gemini_configure(api_key=self.api_key)
        self.client = GenerativeModel(self.model)
    
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """Processa documento usando a API do Google Gemini"""
        system_prompt = prompt or "Convert this document to markdown format."
        
        # Se tiver imagens
        if images and len(images) > 0:
            image_parts = []
            for img_path in images:
                with open(img_path, "rb") as img_file:
                    image_parts.append({"mime_type": "image/jpeg", "data": img_file.read()})
            
            response = self.client.generate_content(
                [system_prompt, text, *image_parts],
                generation_config={"temperature": 0.1}
            )
        else:
            response = self.client.generate_content(
                [system_prompt, text],
                generation_config={"temperature": 0.1}
            )
        
        return response.text


class AnthropicProvider(AIProvider):
    """Provedor usando a API da Anthropic (Claude)"""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        # Importação dinâmica para evitar dependência desnecessária
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package não está instalado. Instale com 'pip install anthropic'")
    
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """Processa documento usando a API da Anthropic"""
        system_prompt = prompt or "Convert this document to markdown format."
        
        message_params = {
            "model": self.model,
            "system": system_prompt,
            "max_tokens": 4000,
            "temperature": 0.1,
        }
        
        if images and len(images) > 0:
            # Constrói mensagem com imagens
            content = [{"type": "text", "text": text}]
            
            for img_path in images:
                with open(img_path, "rb") as img_file:
                    import base64
                    img_b64 = base64.b64encode(img_file.read()).decode("utf-8")
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": img_b64
                        }
                    })
            
            message_params["messages"] = [{"role": "user", "content": content}]
        else:
            message_params["messages"] = [{"role": "user", "content": text}]
        
        response = self.client.messages.create(**message_params)
        return response.content[0].text


class DeepSeekProvider(AIProvider):
    """Provedor usando a API da DeepSeek"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-vl")
        # Importação dinâmica para evitar dependência desnecessária
        try:
            import deepseek
            from deepseek import DeepSeekAPIClient
            self.client = DeepSeekAPIClient(api_key=self.api_key)
        except ImportError:
            raise ImportError("deepseek package não está instalado. Instale com 'pip install deepseek'")
    
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """Processa documento usando a API da DeepSeek"""
        system_prompt = prompt or "Convert this document to markdown format."
        
        # Nota: A implementação exata depende da API da DeepSeek, que pode variar
        # Esta é uma implementação genérica baseada no padrão comum de APIs de IA
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if images and len(images) > 0:
            import base64
            image_contents = []
            
            for img_path in images:
                with open(img_path, "rb") as img_file:
                    img_b64 = base64.b64encode(img_file.read()).decode("utf-8")
                    image_contents.append({
                        "type": "image", 
                        "data": f"data:image/jpeg;base64,{img_b64}"
                    })
            
            messages.append({
                "role": "user", 
                "content": [{"type": "text", "data": text}, *image_contents]
            })
        else:
            messages.append({"role": "user", "content": text})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        )
        
        return response.choices[0].message.content


class GrokProvider(AIProvider):
    """Provedor de IA usando o modelo Grok da xAI"""
    
    def __init__(self):
        """
        Inicializa o provedor Grok
        
        Note:
            Atualmente, a API oficial do Grok não está disponível publicamente.
            Esta classe é um placeholder para implementação futura.
        """
        raise NotImplementedError(
            "O provedor Grok ainda não está implementado porque a API oficial não está "
            "disponível publicamente. Quando a API estiver disponível, esta classe será atualizada."
        )
    
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """
        Processa um documento usando o modelo Grok
        
        Esta função não está implementada porque a API oficial do Grok 
        não está disponível publicamente ainda.
        """
        raise NotImplementedError(
            "O provedor Grok ainda não está implementado porque a API oficial não está "
            "disponível publicamente. Por favor, use outro provedor como OpenAI, Gemini ou Claude."
        )


class LlamaLocalProvider(AIProvider):
    """Provedor usando o Llama rodando localmente via llama.cpp"""
    
    def __init__(self):
        self.model_path = os.getenv("LLAMA_MODEL_PATH", "/app/models/llama-3-8b.gguf")
        self.n_ctx = int(os.getenv("LLAMA_N_CTX", "4096"))
        self.n_gpu_layers = int(os.getenv("LLAMA_N_GPU_LAYERS", "-1"))
        self.seed = int(os.getenv("LLAMA_SEED", "42"))
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Modelo GGUF não encontrado em: {self.model_path}")
        
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            seed=self.seed
        )
    
    def process_document(self, text: str, images: Optional[List[str]] = None, prompt: str = "") -> str:
        """Processa documento usando o modelo Llama local"""
        system_prompt = prompt or "Convert this document to markdown format."
        
        # Llama local não processará imagens, então alertamos
        if images and len(images) > 0:
            print("Aviso: Llama local não suporta processamento de imagens. Ignorando imagens fornecidas.")
        
        prompt_template = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant\n"
        
        response = self.llm(
            prompt=prompt_template,
            max_tokens=2048,
            temperature=0.1,
            stop=["<|im_end|>"]
        )
        
        return response["choices"][0]["text"] 