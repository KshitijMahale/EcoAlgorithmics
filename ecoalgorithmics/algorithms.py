import heapq
from collections import deque
import numpy as np

class AdvancedAlgorithmSuite:
    """Enhanced algorithm implementations with optimizations"""
    @staticmethod
    def quicksort_optimized(arr):
        if len(arr) <= 10:
            return AdvancedAlgorithmSuite.insertion_sort(arr)
        first, middle, last = 0, len(arr) // 2, len(arr) - 1
        if arr[first] > arr[middle]:
            arr[first], arr[middle] = arr[middle], arr[first]
        if arr[middle] > arr[last]:
            arr[middle], arr[last] = arr[last], arr[middle]
        if arr[first] > arr[middle]:
            arr[first], arr[middle] = arr[middle], arr[first]
        pivot = arr[middle]
        left = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return (AdvancedAlgorithmSuite.quicksort_optimized(left) + equal + AdvancedAlgorithmSuite.quicksort_optimized(right))

    @staticmethod
    def insertion_sort(arr):
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    @staticmethod
    def timsort_hybrid(arr):
        return sorted(arr.copy())

    @staticmethod
    def heapsort_enhanced(arr):
        arr_copy = arr.copy()
        heapq.heapify(arr_copy)
        return [heapq.heappop(arr_copy) for _ in range(len(arr_copy))]

    @staticmethod
    def mergesort_enhanced(arr):
        if len(arr) <= 10:
            return AdvancedAlgorithmSuite.insertion_sort(arr)
        mid = len(arr) // 2
        left = AdvancedAlgorithmSuite.mergesort_enhanced(arr[:mid])
        right = AdvancedAlgorithmSuite.mergesort_enhanced(arr[mid:])
        return AdvancedAlgorithmSuite._merge_optimized(left, right)

    @staticmethod
    def _merge_optimized(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def dijkstra_optimized(graph, start, end=None):
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()
        previous = {node: None for node in graph}
        while pq:
            current_distance, current = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)
            if end and current == end:
                break
            for neighbor, weight in graph[current].items():
                if neighbor in visited:
                    continue
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        return distances, previous

    @staticmethod
    def bfs_enhanced(graph, start, target=None):
        visited = set()
        queue = deque([start])
        visited.add(start)
        path = {start: None}
        levels = {start: 0}
        while queue:
            current = queue.popleft()
            if target and current == target:
                break
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    path[neighbor] = current
                    levels[neighbor] = levels[current] + 1
        return visited, path, levels

    @staticmethod
    def perceptron_optimized(X, y, learning_rate=0.1, epochs=10):
        """
        Optimized perceptron implementation with energy-efficient computations
        
        Args:
            X (np.ndarray): Input features matrix
            y (np.ndarray): Target labels
            learning_rate (float): Learning rate for weight updates
            epochs (int): Number of training epochs
            
        Returns:
            tuple: (weights, bias, training_history)
        """
        # Initialize with zeros for minimal memory allocation
        weights = np.zeros(X.shape[1], dtype=np.float32)  # Use float32 for efficiency
        bias = 0.0
        history = {
            'errors': [],
            'weights': [],
            'accuracy': []
        }
        
        def step_function(x):
            return np.where(x >= 0, 1, 0)
        
        # Vectorized implementation for better performance
        for epoch in range(epochs):
            errors = 0
            predictions = step_function(np.dot(X, weights) + bias)
            error_vector = y - predictions
            
            # Batch update for better vectorization
            weights += learning_rate * np.dot(error_vector, X)
            bias += learning_rate * np.sum(error_vector)
            
            # Calculate metrics
            errors = np.sum(np.abs(error_vector))
            accuracy = np.mean(predictions == y)
            
            # Store training history
            history['errors'].append(errors)
            history['weights'].append(weights.copy())
            history['accuracy'].append(accuracy)
            
            # Early stopping if perfect accuracy achieved
            if errors == 0:
                break
                
        return weights, bias, history

    @staticmethod
    def predict_perceptron(X, weights, bias):
        """
        Make predictions using trained perceptron
        
        Args:
            X (np.ndarray): Input features
            weights (np.ndarray): Trained weights
            bias (float): Trained bias
            
        Returns:
            np.ndarray: Predictions
        """
        return np.where(np.dot(X, weights) + bias >= 0, 1, 0)

    @staticmethod
    def xor_perceptron_optimized(X, y, learning_rate=0.1, epochs=10, hidden_units=4):
        """
        Optimized XOR perceptron implementation with a hidden layer for non-linear separation
        
        Args:
            X (np.ndarray): Input features matrix
            y (np.ndarray): Target labels
            learning_rate (float): Learning rate for weight updates
            epochs (int): Number of training epochs
            hidden_units (int): Number of hidden layer neurons
            
        Returns:
            tuple: (weights1, weights2, bias1, bias2, training_history)
        """
        # Initialize weights with efficient float32 dtype
        weights1 = np.random.randn(X.shape[1], hidden_units).astype(np.float32) * 0.1
        weights2 = np.random.randn(hidden_units, 1).astype(np.float32) * 0.1
        bias1 = np.zeros(hidden_units, dtype=np.float32)
        bias2 = 0.0
        
        history = {
            'errors': [],
            'accuracy': []
        }
        
        def sigmoid(x):
            return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip for numerical stability
        
        def sigmoid_derivative(x):
            sx = sigmoid(x)
            return sx * (1 - sx)
        
        # Vectorized implementation for better performance
        for epoch in range(epochs):
            # Forward pass
            hidden_input = np.dot(X, weights1) + bias1
            hidden_output = sigmoid(hidden_input)
            output_input = np.dot(hidden_output, weights2) + bias2
            predictions = sigmoid(output_input)
            
            # Backward pass
            output_error = y.reshape(-1, 1) - predictions
            output_delta = output_error * sigmoid_derivative(output_input)
            
            hidden_error = np.dot(output_delta, weights2.T)
            hidden_delta = hidden_error * sigmoid_derivative(hidden_input)
            
            # Update weights and biases
            weights2 += learning_rate * np.dot(hidden_output.T, output_delta)
            bias2 += learning_rate * np.sum(output_delta)
            weights1 += learning_rate * np.dot(X.T, hidden_delta)
            bias1 += learning_rate * np.sum(hidden_delta, axis=0)
            
            # Calculate metrics
            errors = np.mean(np.abs(output_error))
            accuracy = np.mean((predictions >= 0.5) == y.reshape(-1, 1))
            
            history['errors'].append(errors)
            history['accuracy'].append(accuracy)
            
            # Early stopping if very high accuracy achieved
            if accuracy > 0.99:
                break
                
        return weights1, weights2, bias1, bias2, history

    @staticmethod
    def predict_xor_perceptron(X, weights1, weights2, bias1, bias2):
        """
        Make predictions using trained XOR perceptron
        
        Args:
            X (np.ndarray): Input features
            weights1 (np.ndarray): First layer weights
            weights2 (np.ndarray): Second layer weights
            bias1 (np.ndarray): First layer bias
            bias2 (float): Second layer bias
            
        Returns:
            np.ndarray: Predictions
        """
        hidden = 1 / (1 + np.exp(-np.clip(np.dot(X, weights1) + bias1, -500, 500)))
        output = 1 / (1 + np.exp(-np.clip(np.dot(hidden, weights2) + bias2, -500, 500)))
        return (output >= 0.5).astype(int)

    @staticmethod
    def or_perceptron_optimized(X, y, learning_rate=0.1, epochs=10):
        """
        Optimized OR perceptron implementation with energy-efficient computations
        
        Args:
            X (np.ndarray): Input features matrix
            y (np.ndarray): Target labels
            learning_rate (float): Learning rate for weight updates
            epochs (int): Number of training epochs
            
        Returns:
            tuple: (weights, bias, training_history)
        """
        # Initialize with zeros for minimal memory allocation
        weights = np.zeros(X.shape[1], dtype=np.float32)  # Use float32 for efficiency
        bias = 0.0
        history = {
            'errors': [],
            'weights': [],
            'accuracy': []
        }
        
        # Vectorized implementation for better performance
        for epoch in range(epochs):
            # Forward pass with efficient computation
            predictions = np.where(np.dot(X, weights) + bias >= 0, 1, 0)
            error_vector = y - predictions
            
            # Batch update for better vectorization
            weights += learning_rate * np.dot(error_vector, X)
            bias += learning_rate * np.sum(error_vector)
            
            # Calculate metrics
            errors = np.sum(np.abs(error_vector))
            accuracy = np.mean(predictions == y)
            
            # Store training history
            history['errors'].append(errors)
            history['weights'].append(weights.copy())
            history['accuracy'].append(accuracy)
            
            # Early stopping if perfect accuracy achieved
            if errors == 0:
                break
                
        return weights, bias, history

    @staticmethod
    def predict_or_perceptron(X, weights, bias):
        """
        Make predictions using trained OR perceptron
        
        Args:
            X (np.ndarray): Input features
            weights (np.ndarray): Trained weights
            bias (float): Trained bias
            
        Returns:
            np.ndarray: Predictions
        """
        return np.where(np.dot(X, weights) + bias >= 0, 1, 0)

    @staticmethod
    def and_perceptron_optimized(X, y, learning_rate=0.1, epochs=10):
        """
        Optimized AND perceptron implementation with energy-efficient computations
        
        Args:
            X (np.ndarray): Input features matrix
            y (np.ndarray): Target labels
            learning_rate (float): Learning rate for weight updates
            epochs (int): Number of training epochs
            
        Returns:
            tuple: (weights, bias, training_history)
        """
        # Initialize with zeros for minimal memory allocation
        weights = np.zeros(X.shape[1], dtype=np.float32)  # Use float32 for efficiency
        bias = 0.0
        history = {
            'errors': [],
            'weights': [],
            'accuracy': []
        }
        
        # Vectorized implementation for better performance
        for epoch in range(epochs):
            # Forward pass with efficient computation
            predictions = np.where(np.dot(X, weights) + bias >= 0, 1, 0)
            error_vector = y - predictions
            
            # Batch update for better vectorization
            weights += learning_rate * np.dot(error_vector, X)
            bias += learning_rate * np.sum(error_vector)
            
            # Calculate metrics
            errors = np.sum(np.abs(error_vector))
            accuracy = np.mean(predictions == y)
            
            # Store training history
            history['errors'].append(errors)
            history['weights'].append(weights.copy())
            history['accuracy'].append(accuracy)
            
            # Early stopping if perfect accuracy achieved
            if errors == 0:
                break
                
        return weights, bias, history

    @staticmethod
    def predict_and_perceptron(X, weights, bias):
        """
        Make predictions using trained AND perceptron
        
        Args:
            X (np.ndarray): Input features
            weights (np.ndarray): Trained weights
            bias (float): Trained bias
            
        Returns:
            np.ndarray: Predictions
        """
        return np.where(np.dot(X, weights) + bias >= 0, 1, 0)

    @staticmethod
    def compare_and_xor_perceptron(X, learning_rate=0.1, epochs=10, hidden_units=4):
        """
        Comparative implementation of AND vs XOR perceptrons to analyze their
        learning patterns and complexity differences.
        
        Args:
            X (np.ndarray): Input features matrix
            learning_rate (float): Learning rate for weight updates
            epochs (int): Number of training epochs
            hidden_units (int): Number of hidden units for XOR perceptron
            
        Returns:
            tuple: (and_results, xor_results, comparative_metrics)
            where results contain weights, biases, and history
        """
        # Generate target labels
        y_and = np.array([int(all(x)) for x in X], dtype=np.float32)
        y_xor = np.array([int(bool(x[0]) != bool(x[1])) for x in X], dtype=np.float32)
        
        # Initialize AND perceptron (single layer)
        weights_and = np.zeros(X.shape[1], dtype=np.float32)
        bias_and = 0.0
        history_and = {'errors': [], 'weights': [], 'accuracy': []}
        
        # Initialize XOR perceptron (with hidden layer)
        weights1_xor = np.random.randn(X.shape[1], hidden_units).astype(np.float32) * 0.1
        weights2_xor = np.random.randn(hidden_units, 1).astype(np.float32) * 0.1
        bias1_xor = np.zeros(hidden_units, dtype=np.float32)
        bias2_xor = 0.0
        history_xor = {'errors': [], 'weights': [], 'accuracy': []}
        
        # Comparative metrics
        comparative_metrics = {
            'convergence_speed': {'AND': 0, 'XOR': 0},
            'stability': {'AND': [], 'XOR': []},
            'accuracy_progression': {'AND': [], 'XOR': []},
            'complexity_metrics': {
                'AND': {'params': X.shape[1] + 1},  # weights + bias
                'XOR': {'params': (X.shape[1] * hidden_units + hidden_units) + (hidden_units + 1)}  # total params in both layers
            }
        }
        
        def sigmoid(x):
            return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        
        def sigmoid_derivative(x):
            sx = sigmoid(x)
            return sx * (1 - sx)
        
        # Train both perceptrons in parallel
        for epoch in range(epochs):
            # Train AND perceptron (simple)
            predictions_and = np.where(np.dot(X, weights_and) + bias_and >= 0, 1, 0)
            error_vector_and = y_and - predictions_and
            weights_and += learning_rate * np.dot(error_vector_and, X)
            bias_and += learning_rate * np.sum(error_vector_and)
            
            errors_and = np.sum(np.abs(error_vector_and))
            accuracy_and = np.mean(predictions_and == y_and)
            
            # Train XOR perceptron (complex)
            # Forward pass
            hidden_input = np.dot(X, weights1_xor) + bias1_xor
            hidden_output = sigmoid(hidden_input)
            output_input = np.dot(hidden_output, weights2_xor) + bias2_xor
            predictions_xor = sigmoid(output_input)
            
            # Backward pass
            output_error = y_xor.reshape(-1, 1) - predictions_xor
            output_delta = output_error * sigmoid_derivative(output_input)
            
            hidden_error = np.dot(output_delta, weights2_xor.T)
            hidden_delta = hidden_error * sigmoid_derivative(hidden_input)
            
            # Update XOR weights
            weights2_xor += learning_rate * np.dot(hidden_output.T, output_delta)
            bias2_xor += learning_rate * np.sum(output_delta)
            weights1_xor += learning_rate * np.dot(X.T, hidden_delta)
            bias1_xor += learning_rate * np.sum(hidden_delta, axis=0)
            
            errors_xor = np.mean(np.abs(output_error))
            accuracy_xor = np.mean((predictions_xor >= 0.5) == y_xor.reshape(-1, 1))
            
            # Store history
            history_and['errors'].append(errors_and)
            history_and['weights'].append(weights_and.copy())
            history_and['accuracy'].append(accuracy_and)
            
            history_xor['errors'].append(errors_xor)
            history_xor['weights'].append((weights1_xor.copy(), weights2_xor.copy()))
            history_xor['accuracy'].append(accuracy_xor)
            
            # Update comparative metrics
            comparative_metrics['accuracy_progression']['AND'].append(accuracy_and)
            comparative_metrics['accuracy_progression']['XOR'].append(accuracy_xor)
            comparative_metrics['stability']['AND'].append(np.std(predictions_and))
            comparative_metrics['stability']['XOR'].append(np.std(predictions_xor))
            
            # Check convergence
            if errors_and == 0 and comparative_metrics['convergence_speed']['AND'] == 0:
                comparative_metrics['convergence_speed']['AND'] = epoch + 1
            if accuracy_xor > 0.99 and comparative_metrics['convergence_speed']['XOR'] == 0:
                comparative_metrics['convergence_speed']['XOR'] = epoch + 1
        
        # Package results
        and_results = (weights_and, bias_and, history_and)
        xor_results = ((weights1_xor, weights2_xor), (bias1_xor, bias2_xor), history_xor)
        
        return and_results, xor_results, comparative_metrics
        
    @staticmethod
    def compare_or_xor_perceptron(X, learning_rate=0.1, epochs=10, hidden_units=4):
        """
        Comparative implementation of OR vs XOR perceptrons to analyze their
        learning patterns and complexity differences.
        
        Args:
            X (np.ndarray): Input features matrix
            learning_rate (float): Learning rate for weight updates
            epochs (int): Number of training epochs
            hidden_units (int): Number of hidden units for XOR perceptron
            
        Returns:
            tuple: (or_results, xor_results, comparative_metrics)
            where results contain weights, biases, and history
        """
        # Generate target labels
        y_or = np.array([int(any(x)) for x in X], dtype=np.float32)
        y_xor = np.array([int(bool(x[0]) != bool(x[1])) for x in X], dtype=np.float32)
        
        # Initialize OR perceptron (single layer)
        weights_or = np.zeros(X.shape[1], dtype=np.float32)
        bias_or = 0.0
        history_or = {'errors': [], 'weights': [], 'accuracy': []}
        
        # Initialize XOR perceptron (with hidden layer)
        weights1_xor = np.random.randn(X.shape[1], hidden_units).astype(np.float32) * 0.1
        weights2_xor = np.random.randn(hidden_units, 1).astype(np.float32) * 0.1
        bias1_xor = np.zeros(hidden_units, dtype=np.float32)
        bias2_xor = 0.0
        history_xor = {'errors': [], 'weights': [], 'accuracy': []}
        
        # Comparative metrics
        comparative_metrics = {
            'convergence_speed': {'OR': 0, 'XOR': 0},
            'stability': {'OR': [], 'XOR': []},
            'accuracy_progression': {'OR': [], 'XOR': []},
            'complexity_metrics': {
                'OR': {'params': X.shape[1] + 1},  # weights + bias
                'XOR': {'params': (X.shape[1] * hidden_units + hidden_units) + (hidden_units + 1)}  # total params in both layers
            }
        }
        
        def sigmoid(x):
            return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        
        def sigmoid_derivative(x):
            sx = sigmoid(x)
            return sx * (1 - sx)
        
        # Train both perceptrons in parallel
        for epoch in range(epochs):
            # Train OR perceptron (simple)
            predictions_or = np.where(np.dot(X, weights_or) + bias_or >= 0, 1, 0)
            error_vector_or = y_or - predictions_or
            weights_or += learning_rate * np.dot(error_vector_or, X)
            bias_or += learning_rate * np.sum(error_vector_or)
            
            errors_or = np.sum(np.abs(error_vector_or))
            accuracy_or = np.mean(predictions_or == y_or)
            
            # Train XOR perceptron (complex)
            # Forward pass
            hidden_input = np.dot(X, weights1_xor) + bias1_xor
            hidden_output = sigmoid(hidden_input)
            output_input = np.dot(hidden_output, weights2_xor) + bias2_xor
            predictions_xor = sigmoid(output_input)
            
            # Backward pass
            output_error = y_xor.reshape(-1, 1) - predictions_xor
            output_delta = output_error * sigmoid_derivative(output_input)
            
            hidden_error = np.dot(output_delta, weights2_xor.T)
            hidden_delta = hidden_error * sigmoid_derivative(hidden_input)
            
            # Update XOR weights
            weights2_xor += learning_rate * np.dot(hidden_output.T, output_delta)
            bias2_xor += learning_rate * np.sum(output_delta)
            weights1_xor += learning_rate * np.dot(X.T, hidden_delta)
            bias1_xor += learning_rate * np.sum(hidden_delta, axis=0)
            
            errors_xor = np.mean(np.abs(output_error))
            accuracy_xor = np.mean((predictions_xor >= 0.5) == y_xor.reshape(-1, 1))
            
            # Store history
            history_or['errors'].append(errors_or)
            history_or['weights'].append(weights_or.copy())
            history_or['accuracy'].append(accuracy_or)
            
            history_xor['errors'].append(errors_xor)
            history_xor['weights'].append((weights1_xor.copy(), weights2_xor.copy()))
            history_xor['accuracy'].append(accuracy_xor)
            
            # Update comparative metrics
            comparative_metrics['accuracy_progression']['OR'].append(accuracy_or)
            comparative_metrics['accuracy_progression']['XOR'].append(accuracy_xor)
            comparative_metrics['stability']['OR'].append(np.std(predictions_or))
            comparative_metrics['stability']['XOR'].append(np.std(predictions_xor))
            
            # Check convergence
            if errors_or == 0 and comparative_metrics['convergence_speed']['OR'] == 0:
                comparative_metrics['convergence_speed']['OR'] = epoch + 1
            if accuracy_xor > 0.99 and comparative_metrics['convergence_speed']['XOR'] == 0:
                comparative_metrics['convergence_speed']['XOR'] = epoch + 1
        
        # Package results
        or_results = (weights_or, bias_or, history_or)
        xor_results = ((weights1_xor, weights2_xor), (bias1_xor, bias2_xor), history_xor)
        
        return or_results, xor_results, comparative_metrics
        # Generate target labels for AND and OR gates
        y_and = np.array([int(all(x)) for x in X], dtype=np.float32)
        y_or = np.array([int(any(x)) for x in X], dtype=np.float32)
        
        # Initialize weights and biases for both gates
        weights_and = np.zeros(X.shape[1], dtype=np.float32)
        weights_or = np.zeros(X.shape[1], dtype=np.float32)
        bias_and = 0.0
        bias_or = 0.0
        
        # Training history for both gates
        history_and = {'errors': [], 'weights': [], 'accuracy': []}
        history_or = {'errors': [], 'weights': [], 'accuracy': []}
        
        # Comparative metrics
        comparative_metrics = {
            'convergence_speed': {'AND': 0, 'OR': 0},
            'stability': {'AND': [], 'OR': []},
            'accuracy_progression': {'AND': [], 'OR': []}
        }
        
        # Train both perceptrons in parallel
        for epoch in range(epochs):
            # AND gate training
            predictions_and = np.where(np.dot(X, weights_and) + bias_and >= 0, 1, 0)
            error_vector_and = y_and - predictions_and
            weights_and += learning_rate * np.dot(error_vector_and, X)
            bias_and += learning_rate * np.sum(error_vector_and)
            
            errors_and = np.sum(np.abs(error_vector_and))
            accuracy_and = np.mean(predictions_and == y_and)
            
            # OR gate training
            predictions_or = np.where(np.dot(X, weights_or) + bias_or >= 0, 1, 0)
            error_vector_or = y_or - predictions_or
            weights_or += learning_rate * np.dot(error_vector_or, X)
            bias_or += learning_rate * np.sum(error_vector_or)
            
            errors_or = np.sum(np.abs(error_vector_or))
            accuracy_or = np.mean(predictions_or == y_or)
            
            # Store training history
            history_and['errors'].append(errors_and)
            history_and['weights'].append(weights_and.copy())
            history_and['accuracy'].append(accuracy_and)
            
            history_or['errors'].append(errors_or)
            history_or['weights'].append(weights_or.copy())
            history_or['accuracy'].append(accuracy_or)
            
            # Update comparative metrics
            comparative_metrics['accuracy_progression']['AND'].append(accuracy_and)
            comparative_metrics['accuracy_progression']['OR'].append(accuracy_or)
            comparative_metrics['stability']['AND'].append(np.std(predictions_and))
            comparative_metrics['stability']['OR'].append(np.std(predictions_or))
            
            # Check for convergence
            if errors_and == 0 and comparative_metrics['convergence_speed']['AND'] == 0:
                comparative_metrics['convergence_speed']['AND'] = epoch + 1
            if errors_or == 0 and comparative_metrics['convergence_speed']['OR'] == 0:
                comparative_metrics['convergence_speed']['OR'] = epoch + 1
        
        # Package results
        and_results = (weights_and, bias_and, history_and)
        or_results = (weights_or, bias_or, history_or)
        
        return and_results, or_results, comparative_metrics
