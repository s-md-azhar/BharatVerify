import os
import torch
from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbedderService:
    _instance = None
    
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.device = settings.EMBEDDING_DEVICE
        if self.device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
        print(f"Loading embedding model {model_name} on {self.device}...")
        # Using a smaller model by default for memory constrained env if BGE-M3 is too large.
        # But per requirements we use BAAI/bge-m3, it fits in 6GB if we don't load LLM at the same time.
        self.model = SentenceTransformer(model_name, device=self.device)
        print("Embedding model loaded.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            # Fallback to paraphrase-multilingual-MiniLM-L12-v2 if BGE-M3 is causing OOM in demo. 
            # We'll try BGE-M3 first but can be overridden.
            model_name = settings.EMBEDDING_MODEL
            cls._instance = cls(model_name)
        return cls._instance

    def compute_similarity(self, text1: str, text2: str) -> float:
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
            
        embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
        cosine_score = torch.nn.functional.cosine_similarity(embeddings[0].unsqueeze(0), embeddings[1].unsqueeze(0))
        return cosine_score.item()

def get_embedding_similarity(text1: str, text2: str) -> float:
    embedder = EmbedderService.get_instance()
    return embedder.compute_similarity(text1, text2)
