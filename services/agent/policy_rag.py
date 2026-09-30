import os
import json
import faiss
import numpy as np
from services.matching.embedder import EmbedderService

class PolicyRAG:
    _instance = None
    
    def __init__(self):
        self.embedder = EmbedderService.get_instance()
        self.dimension = self.embedder.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self._load_policies()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def _load_policies(self):
        # We define some dummy KYC policies to simulate a policy document
        policies = [
            "If the name matches exactly but DOB is missing, route to MANUAL REVIEW.",
            "If the address score is below 0.4 and name score is below 0.6, auto-reject.",
            "If face match is below threshold but above 0.5, require secondary ID.",
            "Aadhaar cards without a clear face photo are automatically rejected.",
            "Transliteration mismatches up to 2 characters are acceptable without penalty.",
            "Any discrepancy in gender requires manual review."
        ]
        
        embeddings = self.embedder.model.encode(policies, convert_to_numpy=True)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.documents = policies
        print(f"Loaded {len(policies)} policy chunks into FAISS.")
        
    def retrieve_policy(self, query: str, top_k: int = 2):
        query_emb = self.embedder.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_emb)
        distances, indices = self.index.search(query_emb, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results

def get_policy_context(query: str) -> str:
    rag = PolicyRAG.get_instance()
    docs = rag.retrieve_policy(query)
    return " ".join(docs)
