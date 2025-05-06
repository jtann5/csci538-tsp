import torch.optim as optim
import torch
import matplotlib.pyplot as plt
import torch.optim as optim
import networkx as nx
from torch_geometric.utils import from_networkx
import torch.nn as nn
from torch_geometric.nn import GATConv
import torch.nn.functional as F

class TSPAgent:
    def __init__(self, model, lr=1e-3, device='cpu', entropy_weight=0.01):
        # Automatically assign device to 'cuda' if available, else 'cpu'
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)  # Move the model to the correct device
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.entropy_weight = entropy_weight  # Regularization term

    def sample_solution(self, data):
        probs = self.model(data)
        dist = torch.distributions.Categorical(probs)
        tour = []
        log_probs = []
        visited = set()

        for _ in range(len(probs)):
            choice = dist.sample()
            while int(choice) in visited:
                choice = dist.sample()
            visited.add(int(choice))
            tour.append(int(choice))
            log_probs.append(dist.log_prob(choice))

        log_probs = torch.stack(log_probs).to(self.device)  # Ensure log_probs are on the correct device
        entropy = dist.entropy().mean()  # Mean entropy for regularization
        return tour, log_probs, entropy

    def compute_tour_length(self, tour, coords):
        length = 0.0
        for i in range(len(tour)):
            a = coords[tour[i]]
            b = coords[tour[(i + 1) % len(tour)]]
            length += torch.norm(a - b)
        return length

    def train_step(self, data):
        self.model.train()
        self.optimizer.zero_grad()
        tour, log_probs, entropy = self.sample_solution(data)
        coords = data.x
        reward = -self.compute_tour_length(tour, coords)

        # Debugging: Print the reward and tour length
        #if reward < 0:
            #print(f"Negative reward (which is correct): {reward}")
        print(f"Current reward: {reward.item()}")

        # REINFORCE loss with entropy regularization
        loss = -reward * log_probs.sum() + self.entropy_weight * entropy
        loss.backward()

        # Gradient clipping to avoid exploding gradients
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)

        self.optimizer.step()
        return tour, -reward.item()