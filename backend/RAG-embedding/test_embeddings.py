"""
Test script to demonstrate embedding differences
"""

from Embedding_C.embedding_providers import get_embedding_provider
import numpy as np

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot_product / (norm_a * norm_b) if norm_a * norm_b > 0 else 0

def test_embeddings():
    """Test different embedding providers"""
    
    # Test texts
    texts = {
        "clustering": "clustering algorithm for data analysis",
        "machine_learning": "machine learning and artificial intelligence",
        "cooking": "pizza recipe with tomatoes and cheese",
        "clustering2": "k-means clustering method"
    }
    
    print("🧪 TESTING EMBEDDING QUALITY")
    print("=" * 50)
    
    # Test dummy embeddings
    print("\n🤖 DUMMY EMBEDDINGS:")
    dummy_provider = get_embedding_provider("dummy", dimension=384)
    
    dummy_embeddings = {}
    for name, text in texts.items():
        dummy_embeddings[name] = dummy_provider.embed_text(text)
    
    # Calculate similarities
    sim_cluster_ml = cosine_similarity(dummy_embeddings["clustering"], dummy_embeddings["machine_learning"])
    sim_cluster_cooking = cosine_similarity(dummy_embeddings["clustering"], dummy_embeddings["cooking"])
    sim_cluster_cluster2 = cosine_similarity(dummy_embeddings["clustering"], dummy_embeddings["clustering2"])
    
    print(f"Clustering ↔ Machine Learning: {sim_cluster_ml:.3f}")
    print(f"Clustering ↔ Cooking:         {sim_cluster_cooking:.3f}")
    print(f"Clustering ↔ K-means:         {sim_cluster_cluster2:.3f}")
    print("❌ Random similarities - no semantic understanding")
    
    # Test HuggingFace if available
    try:
        print("\n🤗 HUGGINGFACE EMBEDDINGS:")
        hf_provider = get_embedding_provider("huggingface", model_name="all-MiniLM-L6-v2")
        
        hf_embeddings = {}
        for name, text in texts.items():
            hf_embeddings[name] = hf_provider.embed_text(text)
        
        # Calculate similarities
        sim_cluster_ml = cosine_similarity(hf_embeddings["clustering"], hf_embeddings["machine_learning"])
        sim_cluster_cooking = cosine_similarity(hf_embeddings["clustering"], hf_embeddings["cooking"])
        sim_cluster_cluster2 = cosine_similarity(hf_embeddings["clustering"], hf_embeddings["clustering2"])
        
        print(f"Clustering ↔ Machine Learning: {sim_cluster_ml:.3f}")
        print(f"Clustering ↔ Cooking:         {sim_cluster_cooking:.3f}")
        print(f"Clustering ↔ K-means:         {sim_cluster_cluster2:.3f}")
        print("✅ Semantic similarities - understands meaning!")
        
    except ImportError:
        print("\n🤗 HUGGINGFACE EMBEDDINGS:")
        print("❌ sentence-transformers not installed")
        print("💡 Install with: pip install sentence-transformers")
        print("Expected results:")
        print("Clustering ↔ Machine Learning: ~0.65 (related)")
        print("Clustering ↔ Cooking:         ~0.15 (unrelated)")
        print("Clustering ↔ K-means:         ~0.85 (very related)")
    
    print("\n📊 INTERPRETATION:")
    print("• Higher similarity (closer to 1.0) = more related")
    print("• Lower similarity (closer to 0.0) = less related")
    print("• Real embeddings capture semantic relationships")
    print("• Dummy embeddings are just consistent random numbers")

if __name__ == "__main__":
    test_embeddings()