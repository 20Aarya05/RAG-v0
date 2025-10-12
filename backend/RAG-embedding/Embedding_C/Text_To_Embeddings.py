import os
import json
from . import auto_chunk
from .embedding_providers import get_embedding_provider  
def text_to_embeddings(file_path, embeddings_dir="Embeddings", provider_type="dummy", **provider_kwargs):
    """
    Split a text file into chunks, create embeddings, and save them.
    
    Args:
        file_path (str): Path to the text file.
        embeddings_dir (str): Directory to save embeddings.
        provider_type (str): Type of embedding provider ("dummy", "openai", "huggingface")
        **provider_kwargs: Additional arguments for the embedding provider
    
    Returns:
        Path to saved embeddings file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Text file not found: {file_path}")
    
    os.makedirs(embeddings_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(embeddings_dir, f"{base_name}.json")

    print(f"🔄 Processing text file: {file_path}")
    print(f"🤖 Using embedding provider: {provider_type}")
    
    # Initialize embedding provider
    try:
        embedding_provider = get_embedding_provider(provider_type, **provider_kwargs)
        embedding_dimension = embedding_provider.get_dimension()
        print(f"📐 Embedding dimension: {embedding_dimension}")
    except Exception as e:
        print(f"❌ Error initializing embedding provider: {e}")
        print("🔄 Falling back to dummy provider...")
        embedding_provider = get_embedding_provider("dummy")
        embedding_dimension = embedding_provider.get_dimension()
    
    # 1️⃣ Split text into chunks
    chunks = auto_chunk.auto_chunk_text(file_path)
    print(f"📝 Created {len(chunks)} text chunks")

    embeddings_data = []

    # 2️⃣ Generate embeddings for each chunk
    for idx, chunk in enumerate(chunks):
        print(f"🔄 Processing chunk {idx + 1}/{len(chunks)}...")
        
        try:
            embedding = embedding_provider.embed_text(chunk)
        except Exception as e:
            print(f"⚠️ Error generating embedding for chunk {idx}: {e}")
            # Fallback to dummy embedding
            embedding = [0.0] * embedding_dimension

        embeddings_data.append({
            "chunk_index": idx,
            "text": chunk,
            "embedding": embedding,
            "chunk_length": len(chunk),
            "embedding_dimension": len(embedding)
        })

    # 3️⃣ Save embeddings to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Embeddings saved to: {os.path.abspath(output_path)}")
    return output_path
