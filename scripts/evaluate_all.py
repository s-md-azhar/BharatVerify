import json
import torch
import numpy as np
import os
import sys
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.matching.pytorch_model import IdentityMatcherMLP
from scripts.train_matcher import IdentityPairsDataset
from services.matching.baseline import match_fields_baseline
from services.matching.features import compute_all_features
import pickle

def exact_match(src, tgt):
    # Perfect match across all fields = MATCH, otherwise MISMATCH
    s_name = src.get("name", "").lower().strip()
    t_name = tgt.get("name", "").lower().strip()
    s_dob = src.get("dob", "").strip()
    t_dob = tgt.get("dob", "").strip()
    return 1 if (s_name == t_name and s_dob == t_dob) else 0

def fuzzy_match(src, tgt):
    res = match_fields_baseline(src, tgt)
    # Consider VERIFIED and REVIEW as potential positive if we threshold
    # For binary label, VERIFIED -> 1, REVIEW/MISMATCH -> 0
    return 1 if res["overall"] == "VERIFIED" else 0

def evaluate_all():
    os.environ["EMBEDDING_MODEL"] = "paraphrase-multilingual-MiniLM-L12-v2"
    print("Loading test dataset...")
    with open("datasets/synthetic/test_pairs.json", "r", encoding="utf-8") as f:
        test_pairs_raw = json.load(f)
        
    test_dataset = IdentityPairsDataset(test_pairs_raw, use_embeddings=True)
    
    scaler_path = "model_artifacts/scaler.pkl"
    if os.path.exists(scaler_path):
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)
        test_dataset.features = scaler.transform(test_dataset.features).tolist()
        
    model = IdentityMatcherMLP(input_dim=10, hidden_dim=64)
    model.load_state_dict(torch.load("model_artifacts/matcher_v1.pth", weights_only=True))
    model.eval()
    
    y_true = []
    
    preds_exact = []
    preds_fuzzy = []
    preds_pytorch = []
    probs_pytorch = []
    
    print("Evaluating models on", len(test_dataset), "pairs...")
    
    with torch.no_grad():
        for i in range(len(test_dataset)):
            X, y = test_dataset[i]
            y_true.append(y.item())
            
            raw_pair = test_pairs_raw[i]
            src = raw_pair["source"]
            tgt = raw_pair["application"]
            
            # Exact
            preds_exact.append(exact_match(src, tgt))
            
            # Fuzzy
            preds_fuzzy.append(fuzzy_match(src, tgt))
            
            # PyTorch
            logit = model(X.unsqueeze(0)).squeeze()
            prob = torch.sigmoid(logit).item()
            probs_pytorch.append(prob)
            preds_pytorch.append(1 if prob >= 0.5 else 0)

    def print_metrics(name, y_t, y_p, y_prob=None):
        acc = accuracy_score(y_t, y_p)
        prec = precision_score(y_t, y_p, zero_division=0)
        rec = recall_score(y_t, y_p, zero_division=0)
        f1 = f1_score(y_t, y_p, zero_division=0)
        roc = roc_auc_score(y_t, y_prob) if y_prob is not None else roc_auc_score(y_t, y_p)
        
        cm = confusion_matrix(y_t, y_p)
        if cm.shape == (2,2):
            tn, fp, fn, tp = cm.ravel()
        else:
            tn, fp, fn, tp = cm[0][0], 0, 0, 0 # fallback
            
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        print(f"\n--- {name} ---")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"ROC-AUC:   {roc:.4f}")
        print(f"FPR:       {fpr:.4f}")
        print(f"FNR:       {fnr:.4f}")

    print_metrics("A. Exact/Normalized Baseline", y_true, preds_exact)
    print_metrics("B. Fuzzy Matcher", y_true, preds_fuzzy)
    print_metrics("D. PyTorch Matcher", y_true, preds_pytorch, probs_pytorch)

if __name__ == "__main__":
    evaluate_all()
