import numpy as np
import pandas as pd
from scipy import stats

def perform_advanced_statistical_analysis(results_df):
    analysis_results = {}
    numeric_cols = [
        'execution_time', 'energy_consumption', 'carbon_footprint',
        'peak_cpu_usage', 'peak_memory_usage', 'power_efficiency',
        'memory_efficiency', 'energy_per_operation'
    ]
    available_cols = [col for col in numeric_cols if col in results_df.columns]
    correlation_matrix = results_df[available_cols].corr()
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    if len(results_df) > 2:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(results_df[available_cols])
        pca = PCA()
        pca_result = pca.fit_transform(scaled_data)
        analysis_results['pca'] = {
            'explained_variance_ratio': pca.explained_variance_ratio_,
            'cumulative_variance': np.cumsum(pca.explained_variance_ratio_),
            'components': pca.components_
        }
    def classify_performance(row):
        energy_rank = results_df['energy_consumption'].rank(pct=True).loc[row.name]
        time_rank = results_df['execution_time'].rank(pct=True).loc[row.name]
        carbon_rank = results_df['carbon_footprint'].rank(pct=True).loc[row.name]
        avg_rank = (energy_rank + carbon_rank + time_rank * 0.5) / 2.5
        if avg_rank <= 0.25:
            return 'Excellent'
        elif avg_rank <= 0.5:
            return 'Good'
        elif avg_rank <= 0.75:
            return 'Average'
        else:
            return 'Poor'
    results_df['performance_tier'] = results_df.apply(classify_performance, axis=1)
    if len(results_df) > 2:
        categories = results_df['category'].unique()
        if len(categories) > 1:
            category_groups = [results_df[results_df['category'] == cat]['energy_consumption'].values 
                             for cat in categories if len(results_df[results_df['category'] == cat]) > 0]
            if len(category_groups) > 1:
                try:
                    from scipy.stats import f_oneway, kruskal
                    f_stat, p_value_anova = f_oneway(*category_groups)
                    h_stat, p_value_kruskal = kruskal(*category_groups)
                    analysis_results['statistical_tests'] = {
                        'anova': {'f_statistic': f_stat, 'p_value': p_value_anova},
                        'kruskal_wallis': {'h_statistic': h_stat, 'p_value': p_value_kruskal}
                    }
                except:
                    analysis_results['statistical_tests'] = None
    results_df['energy_time_ratio'] = results_df['energy_consumption'] / results_df['execution_time']
    results_df['carbon_energy_ratio'] = results_df['carbon_footprint'] / results_df['energy_consumption']
    results_df['efficiency_index'] = 1 / (results_df['energy_consumption'] * results_df['execution_time'])
    rankings = {}
    ranking_criteria = {
        'energy_consumption': 'ascending',
        'carbon_footprint': 'ascending', 
        'execution_time': 'ascending',
        'efficiency_index': 'descending',
        'power_efficiency': 'descending'
    }
    for metric, direction in ranking_criteria.items():
        if metric in results_df.columns:
            if direction == 'ascending':
                rankings[metric] = results_df.nsmallest(len(results_df), metric)['algorithm'].tolist()
            else:
                rankings[metric] = results_df.nlargest(len(results_df), metric)['algorithm'].tolist()
    outliers = {}
    for col in ['energy_consumption', 'execution_time', 'carbon_footprint']:
        if col in results_df.columns:
            Q1 = results_df[col].quantile(0.25)
            Q3 = results_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers[col] = results_df[
                (results_df[col] < lower_bound) | (results_df[col] > upper_bound)
            ]['algorithm'].tolist()
    analysis_results.update({
        'correlation_matrix': correlation_matrix,
        'rankings': rankings,
        'outliers': outliers,
        'performance_tiers': results_df['performance_tier'].value_counts().to_dict(),
        'efficiency_metrics': {
            'energy_time_ratio': results_df['energy_time_ratio'].describe(),
            'carbon_energy_ratio': results_df['carbon_energy_ratio'].describe(),
            'efficiency_index': results_df['efficiency_index'].describe()
        }
    })
    return analysis_results

def generate_smart_recommendations(results_df, analysis_results, region, use_case="general"):
    recommendations = []
    if 'efficiency_index' in results_df.columns:
        best_overall = results_df.loc[results_df['efficiency_index'].idxmax(), 'algorithm']
        recommendations.append(f"**🏆 Best Overall**: {best_overall} offers the best balance of speed, energy efficiency, and low carbon impact.")
    best_energy = results_df.loc[results_df['energy_consumption'].idxmin(), 'algorithm']
    energy_saving = ((results_df['energy_consumption'].max() - results_df['energy_consumption'].min()) / 
                     results_df['energy_consumption'].max() * 100)
    recommendations.append(f"**⚡ Energy Champion**: {best_energy} can save up to {energy_saving:.1f}% energy compared to least efficient algorithms.")
    best_carbon = results_df.loc[results_df['carbon_footprint'].idxmin(), 'algorithm']
    carbon_saving = ((results_df['carbon_footprint'].max() - results_df['carbon_footprint'].min()) / 
                     results_df['carbon_footprint'].max() * 100)
    recommendations.append(f"**🌱 Climate Champion**: {best_carbon} reduces carbon emissions by up to {carbon_saving:.1f}% - crucial for {region}'s grid.")
    carbon_factors = {'India': 'high', 'China': 'high', 'US': 'medium', 'EU': 'medium', 'Japan': 'medium', 'Nordic': 'low'}
    carbon_level = carbon_factors.get(region, 'medium')
    if carbon_level == 'high':
        recommendations.append(f"**🌍 Regional Insight**: In {region}'s carbon-intensive grid, prioritize the fastest algorithms to minimize total emissions.")
    elif carbon_level == 'low':
        recommendations.append(f"**🌍 Regional Insight**: {region}'s clean grid allows focus on energy efficiency over pure speed.")
    if use_case == "real_time":
        fastest = results_df.loc[results_df['execution_time'].idxmin(), 'algorithm']
        recommendations.append(f"**⚡ Real-time Systems**: {fastest} recommended for latency-critical applications.")
    elif use_case == "batch_processing":
        recommendations.append(f"**📊 Batch Processing**: Prioritize {best_energy} for large-scale batch operations to minimize operational costs.")
    elif use_case == "edge_devices":
        if 'memory_efficiency' in results_df.columns:
            best_memory = results_df.loc[results_df['memory_efficiency'].idxmin(), 'algorithm']
            recommendations.append(f"**📱 Edge Devices**: {best_memory} offers best memory efficiency for resource-constrained environments.")
    if analysis_results and 'performance_tiers' in analysis_results:
        tiers = analysis_results['performance_tiers']
        excellent_count = tiers.get('Excellent', 0)
        if excellent_count > 1:
            recommendations.append(f"**📈 Multiple Options**: {excellent_count} algorithms show excellent performance - choose based on specific constraints.")
    if analysis_results and 'outliers' in analysis_results:
        energy_outliers = analysis_results['outliers'].get('energy_consumption', [])
        if energy_outliers:
            recommendations.append(f"**⚠️ Avoid for Energy**: {', '.join(energy_outliers)} show unusually high energy consumption.")
    complexity_guidance = {
        'small_data': "For small datasets (< 1000 elements), simpler algorithms may outperform complex ones due to overhead.",
        'large_data': "For large datasets (> 10000 elements), algorithm complexity becomes the dominant factor.",
        'variable_data': "For variable data sizes, consider adaptive algorithms that switch strategies based on input size."
    }
    data_size = results_df['data_size'].iloc[0] if 'data_size' in results_df.columns else 1000
    if data_size < 1000:
        recommendations.append(f"**📊 Data Size**: {complexity_guidance['small_data']}")
    elif data_size > 10000:
        recommendations.append(f"**📊 Data Size**: {complexity_guidance['large_data']}")
    else:
        recommendations.append(f"**📊 Data Size**: {complexity_guidance['variable_data']}")
    return recommendations

def create_executive_summary(results_df, analysis_results, region):
    summary = {}
    total_algorithms = len(results_df)
    categories = results_df['category'].unique()
    energy_spread = (results_df['energy_consumption'].max() - results_df['energy_consumption'].min()) / results_df['energy_consumption'].mean() * 100
    time_spread = (results_df['execution_time'].max() - results_df['execution_time'].min()) / results_df['execution_time'].mean() * 100
    energy_champion = results_df.loc[results_df['energy_consumption'].idxmin(), 'algorithm']
    speed_champion = results_df.loc[results_df['execution_time'].idxmin(), 'algorithm']
    carbon_champion = results_df.loc[results_df['carbon_footprint'].idxmin(), 'algorithm']
    if 'efficiency_index' in results_df.columns:
        efficiency_champion = results_df.loc[results_df['efficiency_index'].idxmax(), 'algorithm']
    else:
        efficiency_champion = energy_champion
    summary = {
        'total_algorithms': total_algorithms,
        'categories_tested': list(categories),
        'region': region,
        'key_findings': {
            'energy_spread': f"{energy_spread:.1f}%",
            'time_spread': f"{time_spread:.1f}%",
            'energy_champion': energy_champion,
            'speed_champion': speed_champion,
            'carbon_champion': carbon_champion,
            'efficiency_champion': efficiency_champion
        },
        'statistical_significance': analysis_results.get('statistical_tests', {}).get('anova', {}).get('p_value', None) if analysis_results else None,
        'performance_distribution': analysis_results.get('performance_tiers', {}) if analysis_results else {}
    }
    return summary
