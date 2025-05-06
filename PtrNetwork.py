import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.optim as optim
import networkx as nx
from torch_geometric.utils import from_networkx
from torch_geometric.nn import GATConv
from torch_geometric.nn import GATConv

class PointerNetGNN(nn.Module):
    def __init__(self, input_dim=2, hidden_dim=128):
        super().__init__()
        self.encoder = GATConv(input_dim, hidden_dim)
        self.decoder = nn.Linear(hidden_dim, 1)  # Scores for selection

    def forward(self, data):
        x = self.encoder(data.x, data.edge_index)  # GNN encoding
        logits = self.decoder(x).squeeze(-1)  # [num_nodes]
        probs = torch.softmax(logits, dim=0)
        return probs  # Probabilities for RL sampling