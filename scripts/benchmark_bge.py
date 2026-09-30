import os
import psutil
import time
from sentence_transformers import SentenceTransformer

def benchmark_bge():
    print("--- BENCHMARKING BAAI/bge-m3 ---")
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)
    print(f"Memory before loading: {mem_before:.2f} MB")
    
    start_time = time.time()
    try:
        # BGE-M3 is 2.2GB+. This will download if not cached, which may hang without HF_TOKEN
        # If cached, it will load. We'll set a timeout or just observe memory.
        print("Loading BAAI/bge-m3...")
        model = SentenceTransformer("BAAI/bge-m3")
        mem_after = process.memory_info().rss / (1024 * 1024)
        print(f"Memory after loading: {mem_after:.2f} MB")
        
        # Test inference
        inf_start = time.time()
        emb = model.encode(["Testing inference latency for BGE-M3 model on CPU."])
        inf_end = time.time()
        print(f"Inference latency: {(inf_end - inf_start)*1000:.2f} ms")
        
    except Exception as e:
        print(f"FAILED to load BGE-M3: {e}")
        print(f"Current Memory usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    benchmark_bge()
