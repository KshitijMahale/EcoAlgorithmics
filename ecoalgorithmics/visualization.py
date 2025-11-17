import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def create_advanced_visualizations(results_df):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Energy Consumption Analysis',
            'Carbon Footprint Comparison',
            'Resource Utilization Patterns',
            'Sustainability Score'
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.12
    )

    algorithms = results_df['algorithm'].tolist()
    colors = px.colors.qualitative.Set3

    # (1) Energy Consumption
    fig.add_trace(
        go.Bar(
            name='Energy (J)',
            x=algorithms,
            y=results_df['energy_consumption'],
            error_y=dict(
                type='data',
                array=results_df.get('energy_consumption_std', [0]*len(algorithms)),
                visible=True
            ),
            marker_color=[colors[i % len(colors)] for i in range(len(algorithms))],
            text=[f"{val:.4f}J" for val in results_df['energy_consumption']],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Energy: %{y:.4f}J<extra></extra>"
        ),
        row=1, col=1
    )

    # (2) Carbon Footprint
    fig.add_trace(
        go.Scatter(
            name='Carbon Impact',
            x=algorithms,
            y=results_df['carbon_footprint'],
            mode='markers+lines',
            marker=dict(
                size=[15 + val*1000 for val in results_df['carbon_footprint']],
                color=results_df['carbon_footprint'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="CO₂ Impact")
            ),
            line=dict(width=2, dash='dash'),
            hovertemplate="<b>%{x}</b><br>Carbon: %{y:.6f}g CO₂<extra></extra>"
        ),
        row=1, col=2
    )

    # (3) Resource Utilization (CPU + Memory)
    fig.add_trace(
        go.Bar(
            name='CPU Usage',
            x=algorithms,
            y=results_df['peak_cpu_usage'],
            marker_color='rgba(255, 99, 132, 0.7)',
            offsetgroup=1
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(
            name='Memory Usage',
            x=algorithms,
            y=results_df['peak_memory_usage'] / 10,
            marker_color='rgba(54, 162, 235, 0.7)',
            offsetgroup=2
        ),
        row=2, col=1
    )

    # (4) Sustainability Score
    sustainability_scores = []
    epsilon = 1e-10

    for _, row in results_df.iterrows():
        energy_range = results_df['energy_consumption'].max() - results_df['energy_consumption'].min()
        carbon_range = results_df['carbon_footprint'].max() - results_df['carbon_footprint'].min()
        time_range = results_df['execution_time'].max() - results_df['execution_time'].min()
        memory_range = results_df['peak_memory_usage'].max() - results_df['peak_memory_usage'].min()
        cpu_range = results_df['peak_cpu_usage'].max() - results_df['peak_cpu_usage'].min()

        energy_norm = (row['energy_consumption'] - results_df['energy_consumption'].min()) / (energy_range + epsilon)
        carbon_norm = (row['carbon_footprint'] - results_df['carbon_footprint'].min()) / (carbon_range + epsilon)
        time_norm = (row['execution_time'] - results_df['execution_time'].min()) / (time_range + epsilon)
        memory_norm = (row['peak_memory_usage'] - results_df['peak_memory_usage'].min()) / (memory_range + epsilon)
        cpu_norm = (row['peak_cpu_usage'] - results_df['peak_cpu_usage'].min()) / (cpu_range + epsilon)

        accuracy_bonus = row.get('accuracy', 0) * 10
        power_bonus = 0
        if 'power_efficiency' in row:
            power_range = results_df['power_efficiency'].max() - results_df['power_efficiency'].min()
            if power_range > epsilon:
                power_bonus = ((row['power_efficiency'] - results_df['power_efficiency'].min()) / power_range) * 5

        base_score = 100 - (
            energy_norm * 30 +
            carbon_norm * 25 +
            time_norm * 15 +
            memory_norm * 15 +
            cpu_norm * 15
        )

        final_score = base_score + accuracy_bonus + power_bonus
        sustainability_scores.append(max(0, min(100, final_score)))

    sustainability_colors = ['#4CAF50' if s > 70 else '#FF9800' if s > 40 else '#F44336' for s in sustainability_scores]

    fig.add_trace(
        go.Bar(
            name='Sustainability Score',
            x=algorithms,
            y=sustainability_scores,
            marker_color=sustainability_colors,
            text=[f"{s:.1f}" for s in sustainability_scores],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}/100<extra></extra>"
        ),
        row=2, col=2
    )

    # Layout updates
    fig.update_layout(
        height=900,
        showlegend=True,
        title_text="<b>Advanced Algorithm Performance Dashboard</b>",
        title_x=0.5,
        title_font_size=24,
        title_font_color='#000000',
        font=dict(family="Inter, Arial", size=12, color='#000000'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, color='#000000')
        )
    )

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=16, color='#000000', family='Arial, sans-serif', weight='bold')
        i['y'] = i['y'] - 0.03

    # Axis styling
    for i in range(1, 5):
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)',
                         title_font=dict(size=14, color='#000000'),
                         tickfont=dict(size=12, color='#000000'),
                         row=(i-1)//2 + 1, col=(i-1)%2 + 1)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)',
                         title_font=dict(size=14, color='#000000'),
                         tickfont=dict(size=12, color='#000000'),
                         row=(i-1)//2 + 1, col=(i-1)%2 + 1)

    return fig, sustainability_scores
