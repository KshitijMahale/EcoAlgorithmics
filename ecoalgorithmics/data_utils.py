import random
import numpy as np
from collections import defaultdict

def generate_enhanced_test_data(size, data_type='random', seed=None):
    if seed:
        random.seed(seed)
        np.random.seed(seed)
    if data_type == 'random':
        return [random.randint(1, size * 10) for _ in range(size)]
    elif data_type == 'sorted':
        return list(range(1, size + 1))
    elif data_type == 'reverse':
        return list(range(size, 0, -1))
    elif data_type == 'nearly_sorted':
        data = list(range(1, size + 1))
        for _ in range(max(1, size // 20)):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            data[i], data[j] = data[j], data[i]
        return data
    elif data_type == 'duplicates':
        unique_vals = [random.randint(1, size//5) for _ in range(max(1, size//5))]
        return [random.choice(unique_vals) for _ in range(size)]
    elif data_type == 'gaussian':
        mean = size * 5
        std = size * 2
        return [max(1, int(np.random.normal(mean, std))) for _ in range(size)]
    elif data_type == 'bimodal':
        half = size // 2
        peak1 = [random.randint(1, size//4) for _ in range(half)]
        peak2 = [random.randint(3*size//4, size) for _ in range(size - half)]
        combined = peak1 + peak2
        random.shuffle(combined)
        return combined

def generate_enhanced_graph_data(size, graph_type='random', seed=None):
    if seed:
        random.seed(seed)
        np.random.seed(seed)
    if graph_type == 'random':
        graph = defaultdict(dict)
        nodes = list(range(size))
        for i in range(size - 1):
            weight = random.randint(1, 50)
            graph[i][i + 1] = weight
            graph[i + 1][i] = weight
        num_edges = min(size * 2, size * (size - 1) // 4)
        for _ in range(num_edges):
            u, v = random.sample(nodes, 2)
            if v not in graph[u]:
                weight = random.randint(1, 100)
                graph[u][v] = weight
                graph[v][u] = weight
        return dict(graph)
    elif graph_type == 'small_world':
        graph = defaultdict(dict)
        for i in range(size):
            for j in range(1, min(4, size//2) + 1):
                neighbor = (i + j) % size
                weight = random.randint(1, 20)
                graph[i][neighbor] = weight
                graph[neighbor][i] = weight
        for _ in range(size // 4):
            u, v = random.sample(range(size), 2)
            if v not in graph[u]:
                weight = random.randint(1, 10)
                graph[u][v] = weight
                graph[v][u] = weight
        return dict(graph)
    elif graph_type == 'scale_free':
        graph = defaultdict(dict)
        degrees = defaultdict(int)
        for i in range(min(3, size)):
            for j in range(i + 1, min(3, size)):
                weight = random.randint(1, 30)
                graph[i][j] = weight
                graph[j][i] = weight
                degrees[i] += 1
                degrees[j] += 1
        for new_node in range(3, size):
            total_degree = sum(degrees.values())
            connections_made = 0
            target_connections = min(3, new_node)
            for existing_node in range(new_node):
                if connections_made >= target_connections:
                    break
                if total_degree > 0:
                    prob = degrees[existing_node] / total_degree
                    if random.random() < prob * 3:
                        weight = random.randint(1, 40)
                        graph[new_node][existing_node] = weight
                        graph[existing_node][new_node] = weight
                        degrees[new_node] += 1
                        degrees[existing_node] += 1
                        connections_made += 1
        return dict(graph)
    elif graph_type == 'grid':
        side = int(np.sqrt(size))
        actual_size = side * side
        graph = defaultdict(dict)
        for i in range(side):
            for j in range(side):
                node = i * side + j
                if j < side - 1:
                    right = i * side + (j + 1)
                    weight = random.randint(1, 15)
                    graph[node][right] = weight
                    graph[right][node] = weight
                if i < side - 1:
                    down = (i + 1) * side + j
                    weight = random.randint(1, 15)
                    graph[node][down] = weight
                    graph[down][node] = weight
                if i < side - 1 and j < side - 1 and random.random() < 0.3:
                    diag = (i + 1) * side + (j + 1)
                    weight = random.randint(1, 25)
                    graph[node][diag] = weight
                    graph[diag][node] = weight
        return dict(graph)
    elif graph_type == 'complete':
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == j:
                    row.append(0)
                else:
                    row.append(random.randint(10, 200))
            matrix.append(row)
        for k in range(size):
            for i in range(size):
                for j in range(size):
                    if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                        matrix[i][j] = matrix[i][k] + matrix[k][j]
        return matrix
