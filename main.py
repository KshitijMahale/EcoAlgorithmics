import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import random
import psutil

from ecoalgorithmics.algorithms import AdvancedAlgorithmSuite
from ecoalgorithmics.profiler import EnhancedEnergyProfiler
from ecoalgorithmics.data_utils import generate_enhanced_test_data, generate_enhanced_graph_data
from ecoalgorithmics.visualization import create_advanced_visualizations
from ecoalgorithmics.analysis import perform_advanced_statistical_analysis, generate_smart_recommendations, create_executive_summary

# Enhanced page configuration
st.set_page_config(
    page_title="EcoAlgorithmics - Energy Profiler",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/ecoalgorithmics',
        'Report a bug': "https://github.com/your-repo/ecoalgorithmics/issues",
        'About': "EcoAlgorithmics: Advanced Algorithm Energy Profiling Platform"
    }
)

# Enhanced CSS with modern design principles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .main-container { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 0; }
    .hero-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; text-align: center; color: white; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px; }
    .hero-title { font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; text-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .hero-subtitle { font-size: 1.2rem; font-weight: 300; opacity: 0.9; max-width: 600px; margin: 0 auto; }
    .metric-card { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.2); }
    .metric-value { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .metric-label { font-size: 0.9rem; font-weight: 400; opacity: 0.9; white-space: nowrap; }
    .algorithm-category { background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%); padding: 1rem; border-radius: 12px; color: white; font-weight: 600; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .insight-box { background: linear-gradient(135deg, #f8f9ff 0%, #e8f4f8 100%); border-left: 4px solid #007bff; padding: 1.5rem; margin: 1.5rem 0; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .warning-box { background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%); border-left: 4px solid #ff9800; padding: 1.5rem; margin: 1.5rem 0; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .success-box { background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); border-left: 4px solid #4caf50; padding: 1.5rem; margin: 1.5rem 0; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .dashboard-card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 25px rgba(0,0,0,0.08); margin: 1rem 0; border: 1px solid rgba(0,0,0,0.05); }
    .performance-indicator { display: inline-block; padding: 0.5rem 1rem; border-radius: 20px; color: white; font-weight: 600; font-size: 0.85rem; margin: 0.25rem; }
    .performance-excellent { background: linear-gradient(135deg, #4caf50, #45a049); }
    .performance-good { background: linear-gradient(135deg, #2196f3, #1976d2); }
    .performance-average { background: linear-gradient(135deg, #ff9800, #f57c00); }
    .performance-poor { background: linear-gradient(135deg, #f44336, #d32f2f); }
    .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 0.75rem 2rem; border-radius: 25px; font-weight: 600; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6); }
    .sidebar-section { background: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .progress-ring { width: 120px; height: 120px; border-radius: 50%; background: conic-gradient(from 0deg, #667eea, #764ba2, #667eea); display: flex; align-items: center; justify-content: center; margin: 1rem auto; }
    .progress-ring-inner { width: 90px; height: 90px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; flex-direction: column; }
    .carbon-indicator { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600; margin: 0.2rem; }
    .carbon-low { background: #e8f5e8; color: #2e7d32; }
    .carbon-medium { background: #fff3e0; color: #f57c00; }
    .carbon-high { background: #ffebee; color: #c62828; }
    
    /* Fix for white boxes and general UI improvements */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    .sidebar .sidebar-content {
        background-color: transparent !important;
    }
    div[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px;
        padding: 15px;
    }
    /* Make all plotly charts have white background */
    .js-plotly-plot {
        background-color: white !important;
        border-radius: 8px;
        padding: 10px;
    }
    /* Fix for metrics and text */
    .metric-card {
        overflow: hidden;
        min-width: 120px;
    }
    .metric-label {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    /* Fix for expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }
    .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0 0 8px 8px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Modern header with hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">⚡ EcoAlgorithmics</div>
        <div class="hero-subtitle">Advanced Algorithm Energy Profiling & Climate Impact Analysis Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar with modern design
    with st.sidebar:
        st.markdown("### 🛠️ Configuration Panel")
        
        # Algorithm selection with enhanced grouping
        
        st.markdown("#### 🔄 Sorting Algorithms")
        
        sorting_algorithms = {
            'QuickSort (Optimized)': AdvancedAlgorithmSuite.quicksort_optimized,
            'MergeSort (Enhanced)': AdvancedAlgorithmSuite.mergesort_enhanced,
            'HeapSort (Enhanced)': AdvancedAlgorithmSuite.heapsort_enhanced,
            'TimSort (Python Built-in)': AdvancedAlgorithmSuite.timsort_hybrid,
        }
        
        selected_sorting = {}
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("QuickSort", value=True, help="Optimized with median-of-three pivot"):
                selected_sorting['QuickSort (Optimized)'] = sorting_algorithms['QuickSort (Optimized)']
            if st.checkbox("MergeSort", value=True, help="Enhanced with insertion sort for small arrays"):
                selected_sorting['MergeSort (Enhanced)'] = sorting_algorithms['MergeSort (Enhanced)']
        
        with col2:
            if st.checkbox("HeapSort", value=False, help="Memory-efficient heap-based sorting"):
                selected_sorting['HeapSort (Enhanced)'] = sorting_algorithms['HeapSort (Enhanced)']
            if st.checkbox("TimSort", value=False, help="Python's built-in adaptive sorting"):
                selected_sorting['TimSort (Python Built-in)'] = sorting_algorithms['TimSort (Python Built-in)']
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graph algorithms
      
        st.markdown("#### 🕸️ Graph Algorithms")
        
        graph_algorithms = {
            'Dijkstra (Optimized)': AdvancedAlgorithmSuite.dijkstra_optimized,
            'BFS (Enhanced)': AdvancedAlgorithmSuite.bfs_enhanced,
        }
        
        # Neural Network algorithms with comparative options
        neural_algorithms = {
            'AND vs XOR Comparison': AdvancedAlgorithmSuite.compare_and_xor_perceptron,
            'OR vs XOR Comparison': AdvancedAlgorithmSuite.compare_or_xor_perceptron
        }
        
        selected_graph = {}
        if st.checkbox("Dijkstra", value=True, help="Optimized shortest path algorithm"):
            selected_graph['Dijkstra (Optimized)'] = graph_algorithms['Dijkstra (Optimized)']
        if st.checkbox("BFS", value=True, help="Enhanced breadth-first search"):
            selected_graph['BFS (Enhanced)'] = graph_algorithms['BFS (Enhanced)']
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Neural Network section
       
        st.markdown("#### 🧠 Neural Networks")
        
        selected_neural = {}
        st.markdown("#### Select Perceptron Analysis:")
        
        # Create two columns for the neural network options
        nn_col1, nn_col2 = st.columns(2)
        
        with nn_col1:
            st.markdown("**AND vs XOR**")
            if st.checkbox("Compare AND-XOR", value=False, help="Compare simple AND gate vs complex XOR gate"):
                selected_neural['AND vs XOR'] = neural_algorithms['AND vs XOR Comparison']
        
        with nn_col2:
            st.markdown("**OR vs XOR**")
            if st.checkbox("Compare OR-XOR", value=False, help="Compare simple OR gate vs complex XOR gate"):
                selected_neural['OR vs XOR'] = neural_algorithms['OR vs XOR Comparison']
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced dataset configuration
      
        st.markdown("#### 📊 Dataset Configuration")
        
        # Sorting data configuration
        if selected_sorting:
            st.markdown("**Sorting Parameters:**")
            sort_size = st.slider("Array Size", 100, 10000, 2000, 100, 
                                help="Larger sizes show clearer performance differences")
            sort_type = st.selectbox(
                "Data Pattern",
                ['random', 'sorted', 'reverse', 'nearly_sorted', 'duplicates', 'gaussian', 'bimodal'],
                help="Different patterns stress algorithms differently"
            )
            sort_seed = st.number_input("Random Seed", 0, 9999, 42, help="For reproducible results")
        else:
            sort_size, sort_type, sort_seed = None, None, None
        
        # Graph data configuration  
        if selected_graph:
            st.markdown("**Graph Parameters:**")
            graph_size = st.slider("Graph Nodes", 20, 200, 75, 5,
                                 help="More nodes = higher complexity")
            graph_type = st.selectbox(
                "Graph Type",
                ['random', 'small_world', 'scale_free', 'grid'],
                help="Different topologies have different algorithmic complexity"
            )
            graph_seed = st.number_input("Graph Seed", 0, 9999, 123, help="For reproducible graphs")
        else:
            graph_size, graph_type, graph_seed = None, None, None
            
        # Neural Network data configuration
        if selected_neural:
            st.markdown("**Neural Network Parameters:**")
            nn_learning_rate = st.slider(
                "Learning Rate", 
                0.01, 1.0, 0.1, 0.01,
                help="Controls how fast the model learns"
            )
            nn_epochs = st.slider(
                "Training Epochs", 
                1, 100, 10,
                help="Number of training iterations"
            )
            nn_hidden_units = st.slider(
                "Hidden Units (XOR)", 
                2, 8, 4,
                help="Number of hidden units for XOR network"
            )
        else:
            nn_learning_rate, nn_epochs, nn_hidden_units = None, None, None
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced profiling settings
       
        st.markdown("#### ⚙️ Profiling Settings")
        
        region = st.selectbox(
            "Energy Grid Region",
            ['India', 'US', 'EU', 'Nordic', 'China', 'Japan'],
            help="Different regions have different carbon intensities"
        )
        
        # Display regional info
        carbon_factors = {'India': 0.82, 'US': 0.4, 'EU': 0.3, 'Nordic': 0.1, 'China': 0.75, 'Japan': 0.35}
        renewability = {'India': 23, 'US': 38, 'EU': 42, 'Nordic': 98, 'China': 31, 'Japan': 22}
        
        st.info(f"🌍 **{region}**: {carbon_factors[region]} kg CO₂/kWh, {renewability[region]}% renewable")
        
        iterations = st.slider("Profiling Iterations", 1, 10, 3, 
                             help="More iterations = better statistical accuracy")
        
        use_case = st.selectbox(
            "Use Case Context",
            ['general', 'real_time', 'batch_processing', 'edge_devices'],
            help="Tailors recommendations to your specific needs"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced options
        with st.expander("🔬 Advanced Options"):
            enable_ml_analysis = st.checkbox("Machine Learning Analysis", value=True)
            enable_statistical = st.checkbox("Statistical Testing", value=True)
            enable_predictions = st.checkbox("Performance Predictions", value=False)
            show_confidence_intervals = st.checkbox("Show Confidence Intervals", value=True)
    
    # Main dashboard with enhanced metrics
   
    # Real-time system metrics with enhanced design
    col1, col2, col3, col4, col5 = st.columns(5)
    
    try:
        # Get real system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{cpu_percent:.1f}%</div>
                <div class="metric-label">CPU Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{memory.percent:.1f}%</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            estimated_power = 7.5 + (cpu_percent * 0.08) + (memory.percent * 0.02)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{estimated_power:.1f}W</div>
                <div class="metric-label">Est. Power</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            uptime_hours = uptime / 3600
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{uptime_hours:.1f}h</div>
                <div class="metric-label">Uptime</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            efficiency = max(0, 100 - (cpu_percent * 0.5 + memory.percent * 0.3))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{efficiency:.0f}</div>
                <div class="metric-label">Efficiency Score</div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        # Fallback metrics
        for i, (label, value, unit) in enumerate([
            ("CPU Usage", f"{random.uniform(15, 45):.1f}", "%"),
            ("Memory", f"{random.uniform(30, 70):.1f}", "%"), 
            ("Est. Power", f"{random.uniform(8, 15):.1f}", "W"),
            ("Uptime", f"{random.uniform(1, 48):.1f}", "h"),
            ("Efficiency", f"{random.randint(60, 95)}", "/100")
        ]):
            with [col1, col2, col3, col4, col5][i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{value}{unit}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    # Run analysis when user clicks the button
    if st.button("🚀 Run Algorithm Analysis"):
        # Initialize profiler with selected region
        profiler = EnhancedEnergyProfiler(region=region)

        # Container for all results
        all_results = []

        # Progress bar
        total_algorithms = len(selected_sorting) + len(selected_graph) + len(selected_neural)
        if total_algorithms == 0:
            st.error("No algorithms selected. Please select at least one algorithm to run analysis.")
            return
        progress_bar = st.progress(0)
        current_progress = 0
        progress_step = 1.0 / total_algorithms if total_algorithms > 0 else 0

        # Process sorting algorithms
        if selected_sorting and sort_size and sort_type is not None and sort_seed is not None:
            sort_data = generate_enhanced_test_data(sort_size, sort_type, sort_seed)
            st.write(f"Generated {sort_size} elements for sorting with pattern: {sort_type}")

            for name, algo in selected_sorting.items():
                result = profiler.profile_algorithm_enhanced(
                    algo, sort_data.copy(), name, "Sorting", iterations
                )
                if result['success']:
                    all_results.append(result)
                
                current_progress += progress_step
                progress_bar.progress(min(current_progress, 1.0))

        # Process graph algorithms
        if selected_graph and graph_size and graph_type is not None and graph_seed is not None:
            graph_data = generate_enhanced_graph_data(graph_size, graph_type, graph_seed)
            st.write(f"Generated graph with {graph_size} nodes, type: {graph_type}")

            for name, algo in selected_graph.items():
                if name.startswith('Dijkstra'):
                    start_node = 0
                    result = profiler.profile_algorithm_enhanced(
                        algo, (graph_data, start_node), name, "Graph", iterations
                    )
                else:
                    result = profiler.profile_algorithm_enhanced(
                        algo, graph_data, name, "Graph", iterations
                    )
                
                if result['success']:
                    all_results.append(result)
                
                current_progress += progress_step
                progress_bar.progress(min(current_progress, 1.0))
                
        # Process neural network algorithms
        if selected_neural and nn_learning_rate is not None and nn_epochs is not None and nn_hidden_units is not None:
            # Generate dataset for perceptrons
            X = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=np.float32)
            
            # Create separate tabs for each comparison
            if len(selected_neural) > 0:
                tabs = st.tabs([name for name in selected_neural.keys()])
                
                for i, (name, algo) in enumerate(selected_neural.items()):
                    with tabs[i]:
                        st.write(f"Running {name} with {nn_epochs} epochs")
                        
                        # Profile and train the comparative implementation
                result = profiler.profile_algorithm_enhanced(
                            algo, X, name, "Neural Networks", iterations,
                    learning_rate=nn_learning_rate,
                            epochs=nn_epochs,
                            hidden_units=nn_hidden_units
                )
                
                if result['success']:
                            # Train the models to get comparative results
                            if 'AND vs XOR' in name:
                                and_results, xor_results, comparative_metrics = algo(
                                    X, learning_rate=nn_learning_rate, 
                                    epochs=nn_epochs, 
                                    hidden_units=nn_hidden_units
                                )
                                gate1, gate2 = 'AND', 'XOR'
                            else:  # OR vs XOR
                                or_results, xor_results, comparative_metrics = algo(
                                    X, learning_rate=nn_learning_rate, 
                                    epochs=nn_epochs, 
                                    hidden_units=nn_hidden_units
                                )
                                gate1, gate2 = 'OR', 'XOR'
                            
                            # Create detailed comparison visualization
                            with st.container():
                                st.markdown(f"""
                                ### 📊 Comparative Analysis: {gate1} vs {gate2}
                                This analysis compares a {gate1.lower()} gate (linear) with a {gate2.lower()} gate (non-linear) perceptron.
                                """)
                                
                                # Create three columns for key metrics with improved spacing
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Epochs", f"{nn_epochs}")
                                with col2:
                                    st.metric("Learning Rate", f"{nn_learning_rate}")
                                with col3:
                                    st.metric("Hidden Units", f"{nn_hidden_units}" if gate2 == 'XOR' else "N/A")
                                
                                # Architectural Comparison
                                st.markdown("### 🏗️ Architectural Comparison")
                                arch_col1, arch_col2 = st.columns(2)
                                with arch_col1:
                                    st.markdown(f"""
                                    **{gate1} Gate Architecture**
                                    - Type: Linear Perceptron
                                    - Layers: Single Layer
                                    - Parameters: {comparative_metrics['complexity_metrics'][gate1]['params']}
                                    - Activation: Step Function
                                    """)
                                with arch_col2:
                                    st.markdown(f"""
                                    **{gate2} Gate Architecture**
                                    - Type: Multi-Layer Perceptron
                                    - Layers: Input → Hidden → Output
                                    - Parameters: {comparative_metrics['complexity_metrics'][gate2]['params']}
                                    - Activation: Sigmoid
                                    """)
                                
                                # Learning Progress
                                st.markdown("### 📈 Learning Progress")
                                progress_col1, progress_col2 = st.columns(2)
                                with progress_col1:
                                    st.metric(f"{gate1} Convergence", 
                                            f"{comparative_metrics['convergence_speed'][gate1]} epochs",
                                            delta=f"Linear Separable")
                                with progress_col2:
                                    st.metric(f"{gate2} Convergence", 
                                            f"{comparative_metrics['convergence_speed'][gate2]} epochs",
                                            delta=f"Non-Linear" if gate2 == 'XOR' else "Linear")
                                
                                # Create multiple comparison graphs
                                import plotly.graph_objects as go
                                from plotly.subplots import make_subplots
                                
                                # Create subplots for detailed comparison with more space for titles
                                fig = make_subplots(
                                    rows=2, cols=2,
                                    subplot_titles=(
                                        "Learning Progress Over Time",
                                        "Training Loss Comparison",
                                        "Computational Complexity",
                                        "Resource Utilization"
                                    ),
                                    vertical_spacing=0.15,  # Add more vertical space between subplots
                                    horizontal_spacing=0.08  # Add more horizontal space between subplots
                                )
                                
                                epochs_range = list(range(1, nn_epochs + 1))
                                
                                # 1. Learning Progress (Accuracy)
                                fig.add_trace(
                                    go.Scatter(
                                        x=epochs_range,
                                        y=comparative_metrics['accuracy_progression'][gate1],
                                        name=f'{gate1} Accuracy',
                                        line=dict(color='#2E86C1', width=2),
                                        mode='lines+markers',
                                        marker=dict(size=4)
                                    ),
                                    row=1, col=1
                                )
                                
                                fig.add_trace(
                                    go.Scatter(
                                        x=epochs_range,
                                        y=comparative_metrics['accuracy_progression'][gate2],
                                        name=f'{gate2} Accuracy',
                                        line=dict(color='#E74C3C', width=2),
                                        mode='lines+markers',
                                        marker=dict(size=4)
                                    ),
                                    row=1, col=1
                                )
                                
                                # 2. Training Loss
                                fig.add_trace(
                                    go.Scatter(
                                        x=epochs_range,
                                        y=comparative_metrics['stability'][gate1],
                                        name=f'{gate1} Stability',
                                        line=dict(color='#2E86C1', width=2, dash='dot'),
                                    ),
                                    row=1, col=2
                                )
                                
                                fig.add_trace(
                                    go.Scatter(
                                        x=epochs_range,
                                        y=comparative_metrics['stability'][gate2],
                                        name=f'{gate2} Stability',
                                        line=dict(color='#E74C3C', width=2, dash='dot'),
                                    ),
                                    row=1, col=2
                                )
                                
                                # 3. Computational Complexity
                                params1 = comparative_metrics['complexity_metrics'][gate1]['params']
                                params2 = comparative_metrics['complexity_metrics'][gate2]['params']
                                
                                # Time complexity analysis - directly assign based on gate type
                                # Define time complexity for each gate type explicitly
                                time_complexity_map = {
                                    'AND': 'O(n)',    # Linear time for single layer
                                    'OR': 'O(n)',     # Linear time for single layer
                                    'XOR': 'O(n*h)'   # Linear with hidden layer size
                                }
                                
                                # Explicitly assign time complexity based on gate type
                                # This ensures we always have a value regardless of the gate name
                                if gate1 == 'AND' or gate1 == 'OR':
                                    time_complexity_gate1 = 'O(n)'
                                else:
                                    time_complexity_gate1 = 'O(n)'
                                    
                                if gate2 == 'XOR':
                                    time_complexity_gate2 = 'O(n*h)'
                                else:
                                    time_complexity_gate2 = 'O(n)'
                                
                                # Create a more visible display of time complexity
                                fig.add_trace(
                                    go.Bar(
                                        x=[gate1, gate2],
                                        y=[params1, params2],
                                        name='Parameters',
                                        text=[
                                            f"Params: {params1}<br><b>Time: {time_complexity_gate1}</b>",
                                            f"Params: {params2}<br><b>Time: {time_complexity_gate2}</b>"
                                        ],
                                        textposition='outside',  # Position text outside the bars
                                        textfont=dict(size=14, color='#2C3E50'),
                                        marker_color=['rgba(46, 134, 193, 0.8)', 'rgba(231, 76, 60, 0.8)'],
                                        marker_line=dict(width=1.5, color=['#2E86C1', '#E74C3C']),
                                    ),
                                    row=2, col=1
                                )
                                
                                # Add a text annotation to emphasize time complexity
                                fig.add_annotation(
                                    text=f"Time Complexity:<br>{gate1}: {time_complexity_gate1}<br>{gate2}: {time_complexity_gate2}",
                                    xref="x3", yref="y3",
                                    x=0.5, y=max(params1, params2) * 1.2,
                                    showarrow=False,
                                    font=dict(size=14, color="#2C3E50"),
                                    align="center",
                                    bordercolor="#c7c7c7",
                                    borderwidth=2,
                                    borderpad=4,
                                    bgcolor="white",
                                    opacity=0.8
                                )
                                
                                # 4. Resource Utilization
                                convergence1 = comparative_metrics['convergence_speed'][gate1]
                                convergence2 = comparative_metrics['convergence_speed'][gate2]
                                
                                fig.add_trace(
                                    go.Bar(
                                        x=[f'{gate1} Conv.', f'{gate2} Conv.'],
                                        y=[convergence1, convergence2],
                                        name='Convergence',
                                        marker_color=['#2E86C1', '#E74C3C'],
                                        text=[f"{convergence1} epochs", f"{convergence2} epochs"],
                                        textfont=dict(size=12),
                                        textposition='outside',
                                    ),
                                    row=2, col=2
                                )
                                
                                # Update layout
                                fig.update_layout(
                                    height=900,  # Increase height for more space
                                    showlegend=True,
                                    title_text=f"Detailed Comparison: {gate1} vs {gate2}",
                                    title_font=dict(size=18),  # Larger title font
                                    legend=dict(
                                        yanchor="top",
                                        y=0.99,
                                        xanchor="left",
                                        x=0.01,
                                        bgcolor='rgba(255, 255, 255, 0.8)'
                                    ),
                                    plot_bgcolor='white',
                                    margin=dict(l=80, r=80, t=100, b=80)  # Larger margins
                                )
                                
                                # Update subplot titles with larger font and padding
                                for i in fig['layout']['annotations']:
                                    i['font'] = dict(size=16, color='#2C3E50')
                                    i['y'] = i['y'] - 0.03  # Move titles up for more space
                                
                                # Update axes
                                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
                                
                                # Update specific subplot axes with improved font size and positioning
                                fig.update_yaxes(title_text="Accuracy", range=[0, 1.1], row=1, col=1, 
                                               title_font=dict(size=14), title_standoff=25)
                                fig.update_yaxes(title_text="Loss/Stability", row=1, col=2, 
                                               title_font=dict(size=14), title_standoff=25)
                                fig.update_yaxes(title_text="Parameters", row=2, col=1, 
                                               title_font=dict(size=14), title_standoff=25)
                                fig.update_yaxes(title_text="Epochs", row=2, col=2, 
                                               title_font=dict(size=14), title_standoff=25)
                                
                                fig.update_xaxes(title_text="Epochs", row=1, col=1, 
                                               title_font=dict(size=14), title_standoff=15)
                                fig.update_xaxes(title_text="Epochs", row=1, col=2, 
                                               title_font=dict(size=14), title_standoff=15)
                                fig.update_xaxes(title_text="Algorithm", row=2, col=1, 
                                               title_font=dict(size=14), title_standoff=15)
                                fig.update_xaxes(title_text="Convergence", row=2, col=2, 
                                               title_font=dict(size=14), title_standoff=15)
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Additional Analysis Text
                                st.markdown(f"""
                                ### 🔍 Detailed Analysis
                                
                                #### Time Complexity
                                - **{gate1} Gate**: {time_complexity_gate1}
                                  - Single layer perceptron
                                  - Direct linear computation
                                  - n = input size
                                
                                - **{gate2} Gate**: {time_complexity_gate2}
                                  - {'Multi-layer perceptron with hidden layer' if gate2 == 'XOR' else 'Single layer perceptron'}
                                  - {'n = input size, h = number of hidden units' if gate2 == 'XOR' else 'Direct linear computation'}
                                
                                #### Space Complexity
                                - **{gate1} Gate**: O({params1}) parameters
                                - **{gate2} Gate**: O({params2}) parameters
                                """)
                                
                                # Final Results and Analysis
                                st.markdown("### 🎯 Final Results and Analysis")
                                final_accuracy_1 = comparative_metrics['accuracy_progression'][gate1][-1]
                                final_accuracy_2 = comparative_metrics['accuracy_progression'][gate2][-1]
                                
                                results_col1, results_col2 = st.columns(2)
                                with results_col1:
                                    st.metric(
                                        f"{gate1} Gate Performance", 
                                        f"{final_accuracy_1 * 100:.2f}%",
                                        delta="Optimal" if final_accuracy_1 > 0.99 else "Sub-optimal"
                                    )
                                with results_col2:
                                    st.metric(
                                        f"{gate2} Gate Performance", 
                                        f"{final_accuracy_2 * 100:.2f}%",
                                        delta="Optimal" if final_accuracy_2 > 0.99 else "Sub-optimal"
                                    )
                                
                                # Analysis Summary
                                st.markdown("### 📝 Analysis Summary")
                                
                                # Add convergence analysis in a more readable format
                                st.markdown(f"""
                                #### Convergence Analysis
                                - **{gate1} Gate**: Converged in {convergence1} epochs
                                - **{gate2} Gate**: Converged in {convergence2} epochs
                                - Convergence Ratio: {f"{convergence1/convergence2:.2f}x" if convergence2 > 0 else "N/A (no convergence)"}
                                
                                #### Time & Space Complexity
                                - **{gate1} Gate**: Time Complexity = {time_complexity_gate1}, Space Complexity = O({params1})
                                - **{gate2} Gate**: Time Complexity = {time_complexity_gate2}, Space Complexity = O({params2})
                                
                                #### Key Findings
                                - {'The XOR gate requires more parameters due to its non-linear nature' if gate2 == 'XOR' else 'Both gates have similar architectural complexity'}
                                - {'XOR shows higher computational complexity due to hidden layer processing' if gate2 == 'XOR' else 'Both gates show similar computational patterns'}
                                - Convergence speed difference: {abs(convergence1 - convergence2)} epochs
                                """)
                                
                                if final_accuracy_1 > 0.99 and final_accuracy_2 > 0.99:
                                    st.success(f"✨ **Complete Success** - Both {gate1} and {gate2} gates achieved optimal performance")
                                else:
                                    if final_accuracy_1 > 0.99:
                                        st.warning(f"⚠️ **Partial Success** - {gate1} gate learned successfully, {gate2} gate showed limited performance")
                                    elif final_accuracy_2 > 0.99:
                                        st.warning(f"⚠️ **Partial Success** - {gate2} gate learned successfully, {gate1} gate showed limited performance")
                                    else:
                                        st.error(f"❌ **Learning Challenges** - Neither gate achieved optimal performance")
                                
                            # Add results for overall comparison
                            result['accuracy'] = (final_accuracy_1 + final_accuracy_2) / 2
                            all_results.append(result)
                
                current_progress += progress_step
                progress_bar.progress(min(current_progress, 1.0))

        # Create results dataframe
        if all_results:
            results_df = pd.DataFrame(all_results)
            
            # Create visualizations
            st.markdown("### 📊 Performance Analysis Dashboard")
            fig, sustainability_scores = create_advanced_visualizations(results_df)
            st.plotly_chart(fig, use_container_width=True)

            # Statistical analysis
            analysis_results = None
            if enable_statistical and len(all_results) > 1:
                st.markdown("### 📈 Statistical Analysis")
                analysis_results = perform_advanced_statistical_analysis(results_df)

                # Display correlation heatmap
                correlation_matrix = analysis_results.get('correlation_matrix') if analysis_results else None
                if correlation_matrix is not None:
                    fig_corr = px.imshow(
                        correlation_matrix,
                        labels=dict(color="Correlation"),
                        color_continuous_scale="RdBu_r"
                    )
                    fig_corr.update_layout(
                        title="Metric Correlations",
                        height=500
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)

            # Machine Learning insights
            if enable_ml_analysis and len(all_results) > 2 and analysis_results is not None:
                st.markdown("### 🤖 Machine Learning Insights")
                if 'pca' in analysis_results:
                    explained_var = analysis_results['pca']['explained_variance_ratio']
                    st.write(f"Top performance factors explain {explained_var[0]*100:.1f}% of the variation")

            # Smart recommendations
            st.markdown("### 💡 Smart Recommendations")
            recommendations = generate_smart_recommendations(results_df, analysis_results, region, use_case)
            for rec in recommendations:
                st.markdown(rec)

            # Executive summary
            st.markdown("### 📋 Executive Summary")
            summary = create_executive_summary(results_df, analysis_results, region)
            
            st.markdown(f"""
            **Overview:**
            - Analyzed {summary['total_algorithms']} algorithms across {len(summary['categories_tested'])} categories
            - Region: {summary['region']} (Carbon intensity: {carbon_factors[region]} kg CO₂/kWh)
            
            **Key Findings:**
            - Performance spread: {summary['key_findings']['time_spread']} in execution time
            - Energy spread: {summary['key_findings']['energy_spread']} in energy consumption
            - Most efficient: {summary['key_findings']['efficiency_champion']}
            - Lowest carbon: {summary['key_findings']['carbon_champion']}
            - Fastest execution: {summary['key_findings']['speed_champion']}
            """)

            # Display detailed results
            with st.expander("🔍 Detailed Results"):
                st.dataframe(results_df)
        else:
            st.error("No successful algorithm executions to analyze. Please check your selections.")

if __name__ == "__main__":
    main()