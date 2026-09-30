import torch
import torch.nn as nn

class IdentityMatcherMLP(nn.Module):
    def __init__(self, input_dim: int = 10, hidden_dim: int = 32):
        super(IdentityMatcherMLP, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, 1)  # Output logit
        )

    def forward(self, x):
        return self.network(x)

def get_feature_vector(source, target, use_embeddings=False) -> list:
    """Extracts exactly 10 features for the PyTorch MLP."""
    from services.matching.normalize import normalize_text, normalize_address, normalize_date
    from services.matching.features import compute_all_features
    from services.matching.embedder import get_embedding_similarity
    
    sn = normalize_text(source.get("name", ""))
    tn = normalize_text(target.get("name", ""))
    name_feats = compute_all_features(sn, tn)
    
    sfn = normalize_text(source.get("father_name", ""))
    tfn = normalize_text(target.get("father_name", ""))
    fname_feats = compute_all_features(sfn, tfn)
    
    sa = normalize_address(source.get("address", ""))
    ta = normalize_address(target.get("address", ""))
    addr_feats = compute_all_features(sa, ta)
    
    sd = normalize_date(source.get("dob", ""))
    td = normalize_date(target.get("dob", ""))
    dob_exact = 1.0 if sd == td and sd != "" else 0.0
    
    spin = source.get("pin", "")
    tpin = target.get("pin", "")
    pin_exact = 1.0 if spin == tpin and spin != "" else 0.0

    name_emb = 0.0
    addr_emb = 0.0
    if use_embeddings:
        name_emb = get_embedding_similarity(sn, tn)
        addr_emb = get_embedding_similarity(sa, ta)
        
    return [
        name_feats["fuzzy"],
        name_feats["token"],
        name_feats["ngram"],
        name_emb,
        fname_feats["fuzzy"],
        addr_feats["fuzzy"],
        addr_feats["token"],
        addr_emb,
        dob_exact,
        pin_exact
    ]
