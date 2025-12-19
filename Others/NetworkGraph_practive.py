"""/*
Network Graph Fraud Detection Example
-------------------------------------
We'll use Python (NetworkX and Matplotlib) to visualize a graph of "card transactions".
Each node is a customer or merchant; each edge is a transaction.

Fraud detection (simplest method shown here): We look for "anomalous" patterns.
E.g., a customer suddenly sending $$ to a never-used merchant, or a fast sequence of new connections.

This is a *toy example* to help you understand:
- How financial networks can be represented as graphs.
- How you might detect suspicious behavior.
*/"""

"""// STEP 0: Required packages: networkx, matplotlib, random
// If experimenting in Python, you'd first do: pip install networkx matplotlib"""

import networkx as nx
import matplotlib.pyplot as plt
import random

# STEP 1: Build a simple transaction network with customers & merchants
G = nx.Graph()
customers = ['Alice', 'Bob', 'Carol', 'Dave']
merchants = ['StoreA', 'StoreB', 'StoreC', 'WeirdShop']

for customer in customers:
    for merchant in merchants[:3]:  # Most customers use known stores
        if random.random() > 0.4:   # Not every customer visits every store
            amount = random.randint(20, 200)
            G.add_edge(customer, merchant, amount=amount, time=random.randint(1,10), fraud=False)

# Let's inject some fraud: Dave suddenly sends money to WeirdShop (very rare!)
G.add_edge('Dave', 'WeirdShop', amount=1000, time=11, fraud=True)

# STEP 2: Plot the network
pos = nx.spring_layout(G, seed=42)
edge_colors = ['red' if G[u][v].get('fraud', False) else 'black' for u, v in G.edges()]
labels = {}
for u,v in G.edges():
    labels[(u,v)] = f"${G[u][v]['amount']}"

nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color=edge_colors, node_size=1500, font_size=12)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Transaction Network (Red = Potential Fraud!)")
plt.show()

# STEP 3: Simple Fraud Detection Algorithm
# We'll flag transactions if:
#  - High dollar amount to a "new" merchant for that customer
#  - Or to a merchant that is "unusual" (few customers go there)

def detect_fraud(G):
    fraud_suspects = []
    for u, v, data in G.edges(data=True):
        # Only consider customer -> merchant edges
        if u in customers and v in merchants:
            is_new = G.number_of_edges(u, v) == 1
            high_amt = data['amount'] > 500
            merchant_popularity = G.degree(v)
            # If large transfer and to a rarely used store, flag it
            if high_amt and merchant_popularity < 2:
                fraud_suspects.append((u, v, data['amount']))
    return fraud_suspects

suspects = detect_fraud(G)
print("Potential Fraudulent Transactions Detected:")
for u, v, amt in suspects:
    print(f" - {u} sent ${amt} to {v}")

# ALGORITHM SUMMARY:
# 1. Build a network graph of users & merchants, each edge = transaction.
# 2. Find rare patterns: very high transaction, or first-time visits, to odd merchants.
# 3. Flag those for human or advanced ML review.

# IN PRACTICE:
# - Sophisticated algorithms use features: transaction speed, geography, network patterns (e.g., money loops), etc.
# - Graph-based ML (like DeepWalk, GCNs), or unsupervised anomaly detection, is often used at scale.
# - This code is a "feel" for the basics. Try adding more customers/merchants, or experiment!

