#!/usr/bin/env python3
"""
Simple analysis of memorial highway factors using existing merged data.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Output directory
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"

# States with merged data
states = ['california', 'florida', 'michigan', 'indiana', 'nebraska', 'wisconsin', 'minnesota', 'utah', 'connecticut', 'montana']

def load_merged_data(state):
    """Load merged data for a state."""
    file_path = os.path.join(output_dir, f"{state}_merged_data.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            print(f"Loaded {state}: {len(df)} counties")
            return df
        except Exception as e:
            print(f"Error loading {state}: {e}")
            return None
    else:
        print(f"No merged data found for {state}")
        return None

def analyze_factors(df, state):
    """Analyze factors for a single state."""
    if df is None or len(df) == 0:
        return None
    
    # Clean column names
    df.columns = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_') for col in df.columns]
    
    # Identify highway count column
    highway_cols = [col for col in df.columns if 'highway_count' in col.lower()]
    if not highway_cols:
        # Try other patterns
        highway_cols = [col for col in df.columns if 'highway' in col.lower() and 'count' in col.lower()]
    
    if not highway_cols:
        print(f"  No highway count column found in {state}")
        return None
    
    highway_col = highway_cols[0]
    
    # Identify numeric columns (excluding highway count and identifiers)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col != highway_col and not any(x in col.lower() for x in ['geoid', 'fips', 'county'])]
    
    print(f"  Analyzing {len(numeric_cols)} demographic variables vs {highway_col}")
    
    # Analyze correlations
    correlations = []
    for col in numeric_cols:
        try:
            # Remove missing values
            valid_data = df[[col, highway_col]].dropna()
            if len(valid_data) > 2:
                corr, p_value = stats.pearsonr(valid_data[col], valid_data[highway_col])
                if not np.isnan(corr) and not np.isnan(p_value):
                    correlations.append({
                        'state': state,
                        'variable': col,
                        'correlation': corr,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'n': len(valid_data)
                    })
        except:
            continue
    
    return pd.DataFrame(correlations)

def analyze_cross_state_patterns(all_correlations):
    """Find patterns across states."""
    if len(all_correlations) == 0:
        return None
    
    # Group by variable
    variable_stats = all_correlations.groupby('variable').agg({
        'correlation': ['mean', 'std', 'count'],
        'p_value': 'mean',
        'significant': 'sum'
    }).round(4)
    
    variable_stats.columns = ['avg_correlation', 'std_correlation', 'states_analyzed', 'avg_p_value', 'states_significant']
    variable_stats = variable_stats.reset_index()
    
    # Filter for variables analyzed in multiple states
    consistent_vars = variable_stats[variable_stats['states_analyzed'] >= 3].copy()
    consistent_vars = consistent_vars.sort_values('states_significant', ascending=False)
    
    return consistent_vars

def create_visualizations(all_correlations, consistent_vars):
    """Create visualizations."""
    if len(all_correlations) == 0:
        return
    
    # 1. Top consistent variables across states
    top_vars = consistent_vars.head(8)
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    for i, (idx, row) in enumerate(top_vars.iterrows()):
        if i >= len(axes):
            break
        
        var_data = all_correlations[all_correlations['variable'] == row['variable']]
        
        if len(var_data) > 0:
            axes[i].bar(range(len(var_data)), var_data['correlation'])
            axes[i].set_xticks(range(len(var_data)))
            axes[i].set_xticklabels(var_data['state'], rotation=45, ha='right', fontsize=8)
            axes[i].set_title(f'{row["variable"].replace("_", " ").title()}\n({row["states_significant"]}/{row["states_analyzed"]} states)', fontsize=10)
            axes[i].set_ylabel('Correlation')
            axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            # Color by significance
            for j, (idx2, row2) in enumerate(var_data.iterrows()):
                if row2['significant']:
                    axes[i].get_children()[j].set_color('green')
                else:
                    axes[i].get_children()[j].set_color('gray')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cross_state_factor_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: cross_state_factor_comparison.png")
    
    # 2. Correlation distribution for top variables
    fig, ax = plt.subplots(figsize=(12, 8))
    
    top_5_vars = top_vars.head(5)['variable'].tolist()
    data_for_plot = all_correlations[all_correlations['variable'].isin(top_5_vars)]
    
    if len(data_for_plot) > 0:
        # Create box plot
        data_for_plot.boxplot(column='correlation', by='variable', ax=ax)
        ax.set_title('Distribution of Correlations by Variable')
        ax.set_ylabel('Correlation Coefficient')
        ax.set_xlabel('Variable')
        plt.suptitle('')  # Remove default title
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'correlation_distribution_by_variable.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: correlation_distribution_by_variable.png")
    
    # 3. State comparison: average highway count vs key demographics
    # This would require loading the actual merged data again
    # For now, create a summary table
    
    return top_vars

def main():
    """Main analysis function."""
    print("=== Memorial Highway Factors Analysis ===")
    
    # Load all merged data
    all_data = {}
    for state in states:
        df = load_merged_data(state)
        if df is not None:
            all_data[state] = df
    
    # Analyze each state
    all_correlations = []
    for state, df in all_data.items():
        print(f"\nAnalyzing {state}...")
        correlations = analyze_factors(df, state)
        if correlations is not None and len(correlations) > 0:
            all_correlations.append(correlations)
    
    if len(all_correlations) == 0:
        print("No correlations found across states")
        return
    
    # Combine all correlations
    all_correlations_df = pd.concat(all_correlations, ignore_index=True)
    
    # Analyze cross-state patterns
    consistent_vars = analyze_cross_state_patterns(all_correlations_df)
    
    if consistent_vars is None or len(consistent_vars) == 0:
        print("No consistent patterns found across states")
        return
    
    print("\n=== Variables Consistently Correlated with Highway Counts ===")
    print(consistent_vars.head(10).to_string(index=False))
    
    # Create visualizations
    top_vars = create_visualizations(all_correlations_df, consistent_vars)
    
    # Save results
    all_correlations_df.to_csv(os.path.join(output_dir, 'all_state_demographic_correlations.csv'), index=False)
    consistent_vars.to_csv(os.path.join(output_dir, 'consistent_demographic_factors.csv'), index=False)
    
    print(f"\n=== Analysis Complete ===")
    print(f"Files saved:")
    print(f"  - all_state_demographic_correlations.csv")
    print(f"  - consistent_demographic_factors.csv")
    print(f"  - cross_state_factor_comparison.png")
    print(f"  - correlation_distribution_by_variable.png")
    
    # Print key findings
    print(f"\n=== Key Findings ===")
    print(f"Top 5 variables most consistently correlated with highway counts:")
    for i, (idx, row) in enumerate(consistent_vars.head(5).iterrows()):
        print(f"{i+1}. {row['variable'].replace('_', ' ').title()}:")
        print(f"   Average correlation: {row['avg_correlation']:.3f}")
        print(f"   States with significant correlation: {row['states_significant']}/{row['states_analyzed']}")

if __name__ == "__main__":
    main()