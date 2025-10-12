"""
Configuration for embedding providers
"""

# Default embedding configuration
EMBEDDING_CONFIG = {
    # Provider type: "dummy", "openai", "huggingface"
    "provider": "dummy",
    
    # Provider-specific configurations
    "providers": {
        "dummy": {
            "dimension": 512
        },
        "openai": {
            "model": "text-embedding-3-small",  # or "text-embedding-3-large", "text-embedding-ada-002"
            # api_key will be read from environment variable OPENAI_API_KEY
        },
        "huggingface": {
            "model_name": "all-MiniLM-L6-v2"  # Fast and good quality
            # Other options: "all-mpnet-base-v2" (better quality, slower)
        }
    }
}

def get_embedding_config():
    """Get the current embedding configuration"""
    return EMBEDDING_CONFIG

def set_embedding_provider(provider_type: str, **kwargs):
    """Set the embedding provider and its configuration"""
    EMBEDDING_CONFIG["provider"] = provider_type
    if kwargs:
        EMBEDDING_CONFIG["providers"][provider_type].update(kwargs)

# Example configurations for different use cases:

# For development/testing (fast, no API required)
DEVELOPMENT_CONFIG = {
    "provider": "dummy",
    "providers": {"dummy": {"dimension": 384}}
}

# For production with OpenAI (high quality, requires API key)
OPENAI_CONFIG = {
    "provider": "openai",
    "providers": {"openai": {"model": "text-embedding-3-small"}}
}

# For local processing (good quality, no API required, but needs model download)
LOCAL_CONFIG = {
    "provider": "huggingface",
    "providers": {"huggingface": {"model_name": "all-MiniLM-L6-v2"}}
}

def use_config(config_name: str):
    """Switch to a predefined configuration"""
    configs = {
        "development": DEVELOPMENT_CONFIG,
        "openai": OPENAI_CONFIG,
        "local": LOCAL_CONFIG
    }
    
    if config_name in configs:
        EMBEDDING_CONFIG.update(configs[config_name])
        print(f"✅ Switched to {config_name} configuration")
        print(f"🤖 Provider: {EMBEDDING_CONFIG['provider']}")
    else:
        print(f"❌ Unknown configuration: {config_name}")
        print(f"Available: {list(configs.keys())}")

if __name__ == "__main__":
    print("Current configuration:")
    print(f"Provider: {EMBEDDING_CONFIG['provider']}")
    print(f"Config: {EMBEDDING_CONFIG['providers'][EMBEDDING_CONFIG['provider']]}")