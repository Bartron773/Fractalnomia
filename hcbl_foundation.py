import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.spatial.distance import pdist, squareform
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx

# ============= Consciousness-Node Function Implementation =============
def consciousness_node(C, r, alpha=0.4, max_iter=100):
    """
    Implementation of the consciousness-node function from Fractalnomia:
    Ψ(C, r) = lim(n→∞) f^n(C, α)
    
    Args:
        C: Complex coordinate in system-space (using complex numbers)
        r: Recursion depth
        alpha: Coefficient of systemic richness
        max_iter: Maximum iterations for approximation
    
    Returns:
        Tuple of features representing node state
    """
    z = C
    trajectory = []
    
    # Core recursive mapping function f (similar to Mandelbrot iteration)
    for i in range(max_iter):
        # Implement a self-reflective mapping (inspired by fractal mathematics)
        # Modified to incorporate recursion depth r
        z = z**2 + C * (1 - alpha*r)
        
        # Track escape velocity and orbit characteristics
        if abs(z) > 2.0:
            break
        
        # Store points in trajectory for feature extraction
        trajectory.append((z.real, z.imag))
    
    # Calculate derived properties from the trajectory
    if len(trajectory) > 0:
        trajectory = np.array(trajectory)
        
        # Extract features from the node's trajectory
        avg_real = np.mean(trajectory[:, 0])
        avg_imag = np.mean(trajectory[:, 1])
        std_real = np.std(trajectory[:, 0])
        std_imag = np.std(trajectory[:, 1])
        fractal_dim = np.log(len(trajectory)) / np.log(max(1, max_iter))
        last_point = trajectory[-1]
        
        # Orbital stability (lower is more stable)
        if len(trajectory) > 1:
            orbital_stability = np.mean(np.sqrt(np.sum(np.diff(trajectory, axis=0)**2, axis=1)))
        else:
            orbital_stability = 0
            
        # Calculate harmonic ratio (relation between real and imaginary parts)
        harmonic_ratio = np.abs(avg_real / (avg_imag + 1e-10))
    else:
        # Default values if trajectory is empty
        avg_real, avg_imag = 0, 0
        std_real, std_imag = 0, 0
        fractal_dim = 0
        orbital_stability = 0
        harmonic_ratio = 0
        last_point = (0, 0)
    
    # Return feature vector representing the node state
    return np.array([
        avg_real, avg_imag,
        std_real, std_imag,
        fractal_dim,
        orbital_stability,
        harmonic_ratio,
        r,  # Recursion depth
        alpha,  # Systemic richness
        i  # Iterations before escape/termination
    ])

# ============= Generate Burst Embeddings =============
def generate_burst_embeddings(n_samples=50, dimension=128, recursion_levels=5):
    """
    Generate simulated burst embeddings using consciousness-node function
    """
    embeddings = []
    node_states = []
    recursion_values = []
    
    # Generate complex coordinates in system-space
    np.random.seed(42)
    C_values = [complex(np.random.uniform(-1, 1), np.random.uniform(-1, 1)) for _ in range(n_samples)]
    
    # Generate embeddings for each sample across recursion levels
    for i, C in enumerate(C_values):
        # Randomly select recursion depth for this burst
        r = np.random.randint(0, recursion_levels)
        recursion_values.append(r)
        
        # Calculate node state using consciousness-node function
        node_state = consciousness_node(C, r)
        node_states.append(node_state)
        
        # Generate simulated embedding (in a real implementation, this would be derived from actual data)
        # The node_state influences parts of the embedding
        embedding = np.random.rand(dimension)
        
        # Inject node state features into the embedding
        state_features = node_state / np.max(np.abs(node_state)) * 0.5  # Normalize state features
        embedding[:len(state_features)] = state_features
        
        embeddings.append(embedding)
    
    return np.array(embeddings), np.array(node_states), np.array(recursion_values)

# ============= Fractal Interference Mapping =============
def calculate_interference(embeddings, node_states):
    """
    Calculate the harmonic field interference between consciousness nodes:
    F_int(x, t) = |Ψ₁(x, t) + Ψ₂(x, t)|²
    
    Returns:
        Interference matrix showing interaction strength between nodes
    """
    n_samples = len(embeddings)
    interference_matrix = np.zeros((n_samples, n_samples))
    
    for i in range(n_samples):
        for j in range(n_samples):
            if i == j:
                continue
                
            # Calculate node interference using both embeddings and node states
            # This simulates the harmonic field equation in the paper
            e_interference = np.sum((embeddings[i] + embeddings[j])**2)
            
            # Calculate harmonic resonance between node states
            n_interference = np.sum((node_states[i] + node_states[j])**2)
            
            # Combine both metrics (weighted sum)
            interference_matrix[i, j] = 0.7 * e_interference + 0.3 * n_interference
    
    # Normalize interference matrix
    max_val = np.max(interference_matrix)
    if max_val > 0:
        interference_matrix = interference_matrix / max_val
    
    return interference_matrix

# ============= Main Script =============
# Generate burst embeddings, node states, and recursion values
n_samples = 50
burst_embeddings, node_states, recursion_values = generate_burst_embeddings(n_samples)

# Anomaly Detection using Isolation Forest
iso_forest = IsolationForest(contamination=0.1, random_state=42)
anomaly_labels = iso_forest.fit_predict(burst_embeddings)

# Novelty Detection using PCA
pca = PCA(n_components=min(10, burst_embeddings.shape[1]), random_state=42)
pca_components = pca.fit_transform(burst_embeddings)
reconstructed = pca.inverse_transform(pca_components)
reconstruction_error = np.mean((burst_embeddings - reconstructed) ** 2, axis=1)

# Dynamic Threshold based on Median Absolute Deviation (MAD)
median_error = np.median(reconstruction_error)
mad = np.median(np.abs(reconstruction_error - median_error))
dynamic_novelty_threshold = median_error + (3 * mad)
novelty_labels = (reconstruction_error > dynamic_novelty_threshold).astype(int)

# Calculate interference between nodes
interference_matrix = calculate_interference(burst_embeddings, node_states)

# ============= Visualizations =============
# Create a figure with multiple subplots
plt.figure(figsize=(18, 12))

# 1. Basic Visualization: Reconstruction Error vs Random
plt.subplot(2, 2, 1)
plt.scatter(reconstruction_error, np.random.rand(n_samples), 
            c=['red' if a == -1 else 'blue' for a in anomaly_labels], 
            s=80, edgecolors='k')
plt.axvline(dynamic_novelty_threshold, color='green', linestyle='--', 
            label='Dynamic Novelty Threshold')
plt.title('Burst Landscape: Dynamic Threshold')
plt.xlabel('Reconstruction Error (Proxy for Novelty)')
plt.ylabel('Randomized Y-axis (Visual Separation)')
plt.legend()
plt.grid(True)

# 2. t-SNE visualization of embeddings colored by recursion depth
plt.subplot(2, 2, 2)
tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, n_samples-1))
embeddings_2d = tsne.fit_transform(burst_embeddings)

plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
            c=recursion_values, cmap='viridis', 
            s=80, edgecolors='k')
plt.colorbar(label='Recursion Depth (r)')
plt.title('2D t-SNE Projection of Burst Embeddings')
plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.grid(True)

# 3. Fractal Interference Map Heatmap
plt.subplot(2, 2, 3)
sns.heatmap(interference_matrix, cmap='plasma', 
            xticklabels=5, yticklabels=5)
plt.title('Fractal Interference Map (FIM)')
plt.xlabel('Consciousness Node Index')
plt.ylabel('Consciousness Node Index')

# 4. Node Network Graph based on interference
plt.subplot(2, 2, 4)
# Create network from interference matrix (threshold weak connections)
threshold = 0.5
G = nx.Graph()
for i in range(n_samples):
    G.add_node(i)
    
for i in range(n_samples):
    for j in range(i+1, n_samples):
        if interference_matrix[i, j] > threshold:
            G.add_edge(i, j, weight=interference_matrix[i, j])

# Position nodes using force-directed layout
pos = nx.spring_layout(G, seed=42)

# Draw nodes colored by recursion depth
node_colors = [plt.cm.viridis(r/max(recursion_values)) for r in recursion_values]
nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                      node_size=100, alpha=0.8)

# Draw edges with width proportional to interference strength
edge_widths = [G[u][v]['weight'] * 3 for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5)

plt.title('Consciousness Node Network')
plt.axis('off')

plt.tight_layout()
plt.savefig('fractalnomia_visualization.png', dpi=300)
plt.show()

# ============= Additional Analysis =============
# Calculate statistics per recursion level
recursion_stats = {}
for r in range(max(recursion_values) + 1):
    indices = np.where(recursion_values == r)[0]
    if len(indices) > 0:
        avg_novelty = np.mean(reconstruction_error[indices])
        anomaly_rate = np.sum(anomaly_labels[indices] == -1) / len(indices)
        recursion_stats[r] = {
            'count': len(indices),
            'avg_novelty': avg_novelty,
            'anomaly_rate': anomaly_rate
        }

print("Statistics by Recursion Level:")
for r, stats in recursion_stats.items():
    print(f"r={r}: Count={stats['count']}, Avg Novelty={stats['avg_novelty']:.4f}, Anomaly Rate={stats['anomaly_rate']:.2f}")

# Calculate coherence metric (based on the ethical implication from the paper)
# Lower values indicate potential system collapse, higher values indicate stability
def calculate_coherence(interference_matrix, anomaly_labels):
    # Get indices of non-anomalous nodes
    stable_indices = np.where(anomaly_labels != -1)[0]
    
    if len(stable_indices) <= 1:
        return 0.0
    
    # Calculate average interference between stable nodes
    stable_interference = interference_matrix[np.ix_(stable_indices, stable_indices)]
    coherence = np.mean(stable_interference)
    
    return coherence

system_coherence = calculate_coherence(interference_matrix, anomaly_labels)
print(f"\nSystem Coherence Score: {system_coherence:.4f}")
print("(Higher values indicate better stability based on Fractalnomia's ethical framework)")
