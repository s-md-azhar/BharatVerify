import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.matching.pytorch_model import IdentityMatcherMLP, get_feature_vector
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pickle

class IdentityPairsDataset(Dataset):
    def __init__(self, data, use_embeddings=False):
        self.data = data
        self.use_embeddings = use_embeddings
        self.features = []
        self.labels = []
        print(f"Extracting features for {len(self.data)} pairs (embeddings={use_embeddings})...")
        for idx, item in enumerate(self.data):
            feat = get_feature_vector(item["source"], item["application"], use_embeddings=use_embeddings)
            self.features.append(feat)
            self.labels.append(float(item["label"]))
            
            if (idx + 1) % 500 == 0:
                print(f"Processed {idx + 1}/{len(self.data)}...")

    def __len__(self):
        return len(self.features)
        
    def __getitem__(self, idx):
        return torch.tensor(self.features[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.float32)

def train_model():
    # Using fallback model for training to avoid OOM and excessive download times on 8GB RAM machine.
    os.environ["EMBEDDING_MODEL"] = "paraphrase-multilingual-MiniLM-L12-v2"
    with open("datasets/synthetic/train_pairs.json", 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    with open("datasets/synthetic/val_pairs.json", 'r', encoding='utf-8') as f:
        val_data = json.load(f)
        
    train_dataset = IdentityPairsDataset(train_data, use_embeddings=True)
    val_dataset = IdentityPairsDataset(val_data, use_embeddings=True)
    
    # Fit Scaler
    scaler = StandardScaler()
    train_dataset.features = scaler.fit_transform(train_dataset.features).tolist()
    val_dataset.features = scaler.transform(val_dataset.features).tolist()
    
    os.makedirs("model_artifacts", exist_ok=True)
    with open("model_artifacts/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    
    model = IdentityMatcherMLP(input_dim=10, hidden_dim=64) # Increased hidden dim
    
    # Class weighting for BCE
    pos_count = sum(train_dataset.labels)
    neg_count = len(train_dataset.labels) - pos_count
    pos_weight = torch.tensor([neg_count / max(pos_count, 1)])
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    
    optimizer = optim.AdamW(model.parameters(), lr=0.005, weight_decay=1e-3)
    
    epochs = 40
    best_val_loss = float('inf')
    
    print("Starting training...")
    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for X, y in train_loader:
            optimizer.zero_grad()
            outputs = model(X).squeeze()
            loss = criterion(outputs, y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * X.size(0)
            
        train_loss /= len(train_loader.dataset)
        
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X, y in val_loader:
                outputs = model(X).squeeze()
                loss = criterion(outputs, y)
                val_loss += loss.item() * X.size(0)
        val_loss /= len(val_loader.dataset)
        
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            os.makedirs("model_artifacts", exist_ok=True)
            torch.save(model.state_dict(), "model_artifacts/matcher_v1.pth")
            print("Saved new best model!")

if __name__ == "__main__":
    train_model()
