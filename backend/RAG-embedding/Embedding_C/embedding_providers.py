"""
Embedding providers for different APIs
"""
import os
import requests
import json
from typing import List, Optional

class EmbeddingProvider:
    """Base class for embedding providers"""
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        raise NotImplementedError
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        raise NotImplementedError

class DummyEmbeddingProvider(EmbeddingProvider):
    """Dummy provider for testing - generates random-like embeddings"""
    
    def __init__(self, dimension: int = 512):
        self.dimension = dimension
    
    def embed_text(self, text: str) -> List[float]:
        """Generate dummy embedding based on text hash"""
        import hashlib
        import random
        
        # Use text hash as seed for reproducible "embeddings"
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        # Generate normalized random vector
        embedding = [random.uniform(-1, 1) for _ in range(self.dimension)]
        
        # Normalize to unit vector (optional)
        norm = sum(x*x for x in embedding) ** 0.5
        if norm > 0:
            embedding = [x/norm for x in embedding]
        
        return embedding
    
    def get_dimension(self) -> int:
        return self.dimension

class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1/embeddings"
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "input": text,
            "model": self.model
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result["data"][0]["embedding"]
    
    def get_dimension(self) -> int:
        # Model dimensions
        dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536
        }
        return dimensions.get(self.model, 1536)

class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    """HuggingFace embedding provider using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
        except ImportError:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding using HuggingFace model"""
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def get_dimension(self) -> int:
        # Common model dimensions
        dimensions = {
            "all-MiniLM-L6-v2": 384,
            "all-mpnet-base-v2": 768,
            "all-distilroberta-v1": 768,
            "paraphrase-MiniLM-L6-v2": 384
        }
        return dimensions.get(self.model_name, 384)

def get_embedding_provider(provider_type: str = "dummy", **kwargs) -> EmbeddingProvider:
    """Factory function to get embedding provider"""
    
    providers = {
        "dummy": DummyEmbeddingProvider,
        "openai": OpenAIEmbeddingProvider,
        "huggingface": HuggingFaceEmbeddingProvider
    }
    
    if provider_type not in providers:
        raise ValueError(f"Unknown provider: {provider_type}. Available: {list(providers.keys())}")
    
    return providers[provider_type](**kwargs)

# Example usage and testing
if __name__ == "__main__":
    # Test dummy provider
    print("Testing Dummy Provider...")
    dummy_provider = get_embedding_provider("dummy", dimension=128)
    embedding = dummy_provider.embed_text("Hello world")
    print(f"Dimension: {dummy_provider.get_dimension()}")
    print(f"Sample embedding (first 10): {embedding[:10]}")
    
    # Test HuggingFace provider (if available)
    try:
        print("\nTesting HuggingFace Provider...")
        hf_provider = get_embedding_provider("huggingface")
        embedding = hf_provider.embed_text("Hello world")
        print(f"Dimension: {hf_provider.get_dimension()}")
        print(f"Sample embedding (first 10): {embedding[:10]}")
    except ImportError as e:
        print(f"HuggingFace provider not available: {e}")