import json
import torch
import numpy as np
import os
import sys
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.matching.pytorch_model import IdentityMatcherMLP
from scripts.train_matcher import IdentityPairsDataset

def evaluate_model():

    test_dataset = IdentityPairsDataset("datasets/synthetic/test_pairs.json", use_embeddings=True)
    
    model = IdentityMatcherMLP(input_dim=10, hidden_dim=32)
    model.load_state_dict(torch.load("model_artifacts/matcher_v1.pth", weights_only=True))
    model.eval()
    
    y_true = []
    y_pred_probs = []
    y_pred_classes = []
    
    import time
    start_time = time.time()
    print("Evaluating model...")
    with torch.no_grad():
        for i in range(len(test_dataset)):
            X, y = test_dataset[i]
            logit = model(X.unsqueeze(0)).squeeze()
            prob = torch.sigmoid(logit).item()
            
            y_true.append(y.item())
            y_pred_probs.append(prob)
            y_pred_classes.append(1 if prob >= 0.5 else 0)

    acc = accuracy_score(y_true, y_pred_classes)
    prec = precision_score(y_true, y_pred_classes)
    rec = recall_score(y_true, y_pred_classes)
    f1 = f1_score(y_true, y_pred_classes)
    roc_auc = roc_auc_score(y_true, y_pred_probs)
    cm = confusion_matrix(y_true, y_pred_classes)
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
    
    end_time = time.time()
    latency_ms = ((end_time - start_time) / len(test_dataset)) * 1000
    
    metrics = {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "roc_auc": roc_auc,
        "fpr": fpr,
        "fnr": fnr,
        "latency_ms": latency_ms,
        "confusion_matrix": cm.tolist()
    }
    
    print(f"Results:")
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"FPR: {fpr:.4f}")
    print(f"FNR: {fnr:.4f}")
    print(f"Latency per sample: {latency_ms:.2f} ms")
    print(f"Confusion Matrix:\n{cm}")
    
    os.makedirs("datasets/benchmark", exist_ok=True)
    with open("datasets/benchmark/evaluation.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print("Saved evaluation report to datasets/benchmark/evaluation.json")

if __name__ == "__main__":
    evaluate_model()
