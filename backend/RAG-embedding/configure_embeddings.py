#!/usr/bin/env python3
"""
Interactive script to configure embedding providers
"""

import os
from embedding_config import use_config, get_embedding_config, set_embedding_provider

def show_current_config():
    """Display current embedding configuration"""
    config = get_embedding_config()
    provider = config["provider"]
    provider_config = config["providers"][provider]
    
    print(f"\n📋 Current Configuration:")
    print(f"🤖 Provider: {provider}")
    print(f"⚙️  Settings: {provider_config}")

def configure_openai():
    """Configure OpenAI embedding provider"""
    print("\n🔧 Configuring OpenAI Embeddings...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("💡 To set it:")
        print("   Windows: set OPENAI_API_KEY=your_api_key_here")
        print("   Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ OpenAI API key found")
    
    # Choose model
    models = {
        "1": ("text-embedding-3-small", "1536 dimensions, fast, cost-effective"),
        "2": ("text-embedding-3-large", "3072 dimensions, highest quality"),
        "3": ("text-embedding-ada-002", "1536 dimensions, legacy model")
    }
    
    print("\n📋 Available OpenAI models:")
    for key, (model, desc) in models.items():
        print(f"  {key}. {model} - {desc}")
    
    choice = input("\nSelect model (1-3, default=1): ").strip() or "1"
    
    if choice in models:
        model_name, _ = models[choice]
        set_embedding_provider("openai", model=model_name)
        print(f"✅ Configured OpenAI with model: {model_name}")
        return True
    else:
        print("❌ Invalid choice")
        return False

def configure_huggingface():
    """Configure HuggingFace embedding provider"""
    print("\n🔧 Configuring HuggingFace Embeddings...")
    
    # Check if sentence-transformers is installed
    try:
        import sentence_transformers
        print("✅ sentence-transformers library found")
    except ImportError:
        print("❌ sentence-transformers not installed!")
        print("💡 Install it with: pip install sentence-transformers")
        return False
    
    # Choose model
    models = {
        "1": ("all-MiniLM-L6-v2", "384 dimensions, fast, good for most tasks"),
        "2": ("all-mpnet-base-v2", "768 dimensions, best quality, slower"),
        "3": ("paraphrase-MiniLM-L6-v2", "384 dimensions, good for paraphrases"),
        "4": ("all-distilroberta-v1", "768 dimensions, RoBERTa-based")
    }
    
    print("\n📋 Available HuggingFace models:")
    for key, (model, desc) in models.items():
        print(f"  {key}. {model} - {desc}")
    
    choice = input("\nSelect model (1-4, default=1): ").strip() or "1"
    
    if choice in models:
        model_name, _ = models[choice]
        set_embedding_provider("huggingface", model_name=model_name)
        print(f"✅ Configured HuggingFace with model: {model_name}")
        print("📥 Note: Model will be downloaded on first use")
        return True
    else:
        print("❌ Invalid choice")
        return False

def configure_dummy():
    """Configure dummy embedding provider"""
    print("\n🔧 Configuring Dummy Embeddings...")
    
    dimensions = input("Enter embedding dimension (default=512): ").strip()
    try:
        dim = int(dimensions) if dimensions else 512
        if dim < 1:
            raise ValueError("Dimension must be positive")
        
        set_embedding_provider("dummy", dimension=dim)
        print(f"✅ Configured dummy embeddings with {dim} dimensions")
        return True
    except ValueError as e:
        print(f"❌ Invalid dimension: {e}")
        return False

def main():
    """Main configuration interface"""
    print("🚀 Embedding Provider Configuration")
    print("=" * 40)
    
    while True:
        show_current_config()
        
        print("\n🔧 Configuration Options:")
        print("1. Use OpenAI embeddings (requires API key)")
        print("2. Use HuggingFace embeddings (local, requires library)")
        print("3. Use dummy embeddings (for testing)")
        print("4. Use preset configurations")
        print("5. Test current configuration")
        print("0. Exit")
        
        choice = input("\nSelect option (0-5): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            configure_openai()
        elif choice == "2":
            configure_huggingface()
        elif choice == "3":
            configure_dummy()
        elif choice == "4":
            print("\n📋 Preset Configurations:")
            print("1. development - Fast dummy embeddings for testing")
            print("2. openai - High-quality OpenAI embeddings")
            print("3. local - Local HuggingFace embeddings")
            
            preset = input("Select preset (1-3): ").strip()
            presets = {"1": "development", "2": "openai", "3": "local"}
            
            if preset in presets:
                use_config(presets[preset])
            else:
                print("❌ Invalid preset")
        elif choice == "5":
            test_configuration()
        else:
            print("❌ Invalid option")

def test_configuration():
    """Test the current embedding configuration"""
    print("\n🧪 Testing current configuration...")
    
    try:
        from Embedding_C.embedding_providers import get_embedding_provider
        
        config = get_embedding_config()
        provider_type = config["provider"]
        provider_config = config["providers"][provider_type]
        
        print(f"🔄 Initializing {provider_type} provider...")
        provider = get_embedding_provider(provider_type, **provider_config)
        
        print(f"📐 Embedding dimension: {provider.get_dimension()}")
        
        test_text = "This is a test sentence for embedding generation."
        print(f"🔄 Generating embedding for: '{test_text}'")
        
        embedding = provider.embed_text(test_text)
        
        print(f"✅ Success! Generated {len(embedding)}-dimensional embedding")
        print(f"📊 Sample values: {embedding[:5]}...")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()