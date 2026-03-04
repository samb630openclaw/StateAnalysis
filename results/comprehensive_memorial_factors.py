#!/usr/bin/env python3
"""
Comprehensive analysis of factors contributing to memorial highway designations.
Looks for patterns across all 10 states with both demographic and highway data.
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

# Base directory for Capstone data
base_dir = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/"

# States with both demographic and highway data
states = [
    'california', 'florida', 'michigan', 'indiana', 'nebraska',
    'wisconsin', 'minnesota', 'utah', 'connecticut', 'montana'
]

def load_state_data(state):
    """Load demographic and highway data for a state."""
    state_dir = os.path.join(base_dir, state)
    
    # Find demographic file
    demo_file = None
    for file in os.listdir(state_dir):
        if 'demographic' in file.lower() or 'counties' in file.lower():
            demo_file = os.path.join(state_dir, file)
            break
    
    # Find highway file
    highway_file = None
    for file in os.listdir(state_dir):
        if 'highway' in file.lower() or 'memorial' in file.lower() or 'commemorative' in file.lower():
            if file.endswith('.csv') or file.endswith('.xlsx'):
                highway_file = os.path.join(state_dir, file)
                break
    
    if not demo_file or not highway_file:
        return None
    
    # Load data
    try:
        if demo_file.endswith('.csv'):
            demo_df = pd.read_csv(demo_file)
        else:
            demo_df = pd.read_excel(demo_file)
        
        if highway_file.endswith('.csv'):
            highway_df = pd.read_csv(highway_file)
        else:
            highway_df = pd.read_excel(highway_file)
        
        return {'state': state, 'demo': demo_df, 'highway': highway_df}
    except Exception as e:
        print(f"Error loading {state}: {e}")
        return None

def analyze_state_factors(state_data):
    """Analyze factors for a single state."""
    state = state_data['state']
    demo_df = state_data['demo']
    highway_df = state_data['highway']
    
    print(f"\n=== Analyzing {state.title()} ===")
    
    # Clean column names
    demo_df.columns = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_') for col in demo_df.columns]
    highway_df.columns = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_') for col in highway_df.columns]
    
    # Count highways per county
    if 'county' in highway_df.columns:
        highway_counts = highway_df.groupby('county').size().reset_index(name='highway_count')
    elif 'county_name' in highway_df.columns:
        highway_counts = highway_df.groupby('county_name').size().reset_index(name='highway_count')
    else:
        print(f"  No county column found in highway data for {state}")
        return None
    
    # Merge with demographic data
    if 'county' in demo_df.columns:
        merged = pd.merge(demo_df, highway_counts, on='county', how='inner')
    elif 'county_name' in demo_df.columns:
        merged = pd.merge(demo_df, highway_counts, on='county_name', how='inner')
    else:
        print(f"  No county column found in demographic data for {state}")
        return None
    
    if len(merged) == 0:
        print(f"  No matching counties found for {state}")
        return None
    
    print(f"  Merged data: {len(merged)} counties")
    
    # Identify numeric columns
    numeric_cols = merged.select_dtypes(include=[np.number]).columns.tolist()
    if 'highway_count' in numeric_cols:
        numeric_cols.remove('highway_count')
    
    # Analyze correlations with highway count
    correlations = []
    for col in numeric_cols:
        if col != 'highway_count':
            try:
                corr, p_value = stats.pearsonr(merged[col].dropna(), merged['highway_count'].loc[merged[col].notna()])
                if not np.isnan(corr) and not np.isnan(p_value):
                    correlations.append({
                        'state': state,
                        'variable': col,
                        'correlation': corr,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    })
            except:
                continue
    
    return {
        'state': state,
        'merged': merged,
        'correlations': pd.DataFrame(correlations),
        'highway_counts': highway_counts
    }

def analyze_cross_state_patterns(all_results):
    """Analyze patterns across all states."""
    print("\n=== Cross-State Pattern Analysis ===")
    
    # Combine all correlations
    all_correlations = pd.concat([r['correlations'] for r in all_results if r is not None], ignore_index=True)
    
    # Find variables that are consistently correlated across states
    variable_counts = all_correlations['variable'].value_counts()
    consistent_vars = []
    
    for var in variable_counts.index:
        var_corrs = all_correlations[all_correlations['variable'] == var]
        if len(var_corrs) >= 3:  # At least 3 states have this variable
            avg_corr = var_corrs['correlation'].mean()
            sig_count = var_corrs['significant'].sum()
            if sig_count >= 2:  # At least 2 states show significant correlation
                consistent_vars.append({
                    'variable': var,
                    'states_analyzed': len(var_corrs),
                    'states_significant': sig_count,
                    'avg_correlation': avg_corr,
                    'avg_p_value': var_corrs['p_value'].mean()
                })
    
    consistent_df = pd.DataFrame(consistent_vars)
    consistent_df = consistent_df.sort_values('states_significant', ascending=False)
    
    print("\nVariables consistently correlated with highway counts across states:")
    print(consistent_df.head(10).to_string(index=False))
    
    return consistent_df, all_correlations

def analyze_highway_types_by_demographics(all_results):
    """Analyze how highway types vary by demographic characteristics."""
    print("\n=== Highway Types vs Demographics ===")
    
    # For states with highway type information
    highway_type_analysis = []
    
    for result in all_results:
        if result is None:
            continue
            
        state = result['state']
        highway_df = result['highway'].copy()
        demo_df = result['demo'].copy()
        
        # Clean column names
        highway_df.columns = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_') for col in highway_df.columns]
        demo_df.columns = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_') for col in demo_df.columns]
        
        # Look for type columns
        type_cols = [col for col in highway_df.columns if 'type' in col or 'category' in col or 'subject' in col]
        
        if type_cols:
            type_col = type_cols[0]
            print(f"\n{state.title()} - Highway types found: {highway_df[type_col].unique()[:10]}")
            
            # Count highways by type
            type_counts = highway_df[type_col].value_counts()
            
            # Try to merge with demographics
            if 'county' in highway_df.columns and 'county' in demo_df.columns:
                # Group by county and type
                county_type_counts = highway_df.groupby(['county', type_col]).size().unstack(fill_value=0)
                county_type_counts.columns = [f"{col}_count" for col in county_type_counts.columns]
                county_type_counts = county_type_counts.reset_index()
                
                # Merge with demographics
                merged = pd.merge(demo_df, county_type_counts, on='county', how='inner')
                
                if len(merged) > 0:
                    # Analyze correlations between demographics and highway types
                    numeric_cols = merged.select_dtypes(include=[np.number]).columns.tolist()
                    numeric_cols = [col for col in numeric_cols if not col.endswith('_count')]
                    
                    for type_col_name in county_type_counts.columns:
                        if type_col_name.endswith('_count'):
                            for demo_col in numeric_cols:
                                try:
                                    corr, p_value = stats.pearsonr(merged[demo_col].dropna(), merged[type_col_name].loc[merged[demo_col].notna()])
                                    if not np.isnan(corr) and p_value < 0.05:
                                        highway_type_analysis.append({
                                            'state': state,
                                            'highway_type': type_col_name.replace('_count', ''),
                                            'demographic_variable': demo_col,
                                            'correlation': corr,
                                            'p_value': p_value
                                        })
                                except:
                                    continue
    
    return pd.DataFrame(highway_type_analysis)

def create_visualizations(all_results, consistent_vars, highway_type_analysis):
    """Create visualizations of key patterns."""
    output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"
    
    # 1. Cross-state correlation comparison
    all_correlations = pd.concat([r['correlations'] for r in all_results if r is not None], ignore_index=True)
    
    # Get top variables across states
    top_vars = consistent_vars['variable'].head(5).tolist()
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, var in enumerate(top_vars):
        if i >= len(axes):
            break
            
        var_data = all_correlations[all_correlations['variable'] == var]
        
        if len(var_data) > 0:
            axes[i].bar(range(len(var_data)), var_data['correlation'])
            axes[i].set_xticks(range(len(var_data)))
            axes[i].set_xticklabels(var_data['state'], rotation=45, ha='right')
            axes[i].set_title(f'{var.replace("_", " ").title()} Correlation by State')
            axes[i].set_ylabel('Correlation Coefficient')
            axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            # Color bars by significance
            for j, (idx, row) in enumerate(var_data.iterrows()):
                if row['significant']:
                    axes[i].get_children()[j].set_color('green')
                else:
                    axes[i].get_children()[j].set_color('gray')
    
    # Remove empty subplot
    if len(top_vars) < len(axes):
        fig.delaxes(axes[len(top_vars)])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cross_state_correlation_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nSaved: cross_state_correlation_comparison.png")
    
    # 2. Highway type analysis visualization
    if len(highway_type_analysis) > 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Group by highway type and demographic variable
        grouped = highway_type_analysis.groupby(['highway_type', 'demographic_variable'])['correlation'].mean().unstack(fill_value=0)
        
        if len(grouped) > 0:
            grouped.plot(kind='bar', ax=ax)
            ax.set_title('Highway Type vs Demographic Correlations')
            ax.set_ylabel('Average Correlation')
            ax.set_xlabel('Highway Type')
            ax.legend(title='Demographic Variable', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'highway_type_demographic_correlations.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Saved: highway_type_demographic_correlations.png")
    
    # 3. State comparison by key factors
    state_comparison = []
    for result in all_results:
        if result is None:
            continue
        
        state = result['state']
        merged = result['merged']
        
        if len(merged) > 0:
            # Calculate averages
            avg_highways = merged['highway_count'].mean()
            
            # Look for key demographic variables
            demo_vars = {}
            for col in merged.columns:
                if col in ['median_household_income', 'median_income', 'pct_college_educated', 
                          'pct_bachelors_or_higher', 'pct_hs_grad_or_higher', 'poverty_rate',
                          'pct_below_poverty_level', 'median_age', 'pct_white_alone',
                          'pct_black_alone', 'pct_asian_alone', 'pct_hispanic_alone',
                          'pct_two_or_more_races']:
                    if col in merged.columns:
                        demo_vars[col] = merged[col].mean()
            
            state_comparison.append({
                'state': state,
                'avg_highways': avg_highways,
                **demo_vars
            })
    
    if state_comparison:
        state_df = pd.DataFrame(state_comparison)
        
        # Create scatter plot: income vs highways
        if 'median_household_income' in state_df.columns or 'median_income' in state_df.columns:
            income_col = 'median_household_income' if 'median_household_income' in state_df.columns else 'median_income'
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(state_df[income_col], state_df['avg_highways'])
            
            # Add state labels
            for i, row in state_df.iterrows():
                ax.annotate(row['state'], (row[income_col], row['avg_highways']), fontsize=8)
            
            ax.set_xlabel('Median Household Income')
            ax.set_ylabel('Average Highways per County')
            ax.set_title('Income vs Memorial Highway Designations by State')
            
            # Calculate correlation
            if len(state_df) > 2:
                corr, p_value = stats.pearsonr(state_df[income_col], state_df['avg_highways'])
                ax.text(0.05, 0.95, f'r = {corr:.3f}, p = {p_value:.3f}', 
                       transform=ax.transAxes, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'state_income_highways_comparison.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Saved: state_income_highways_comparison.png")
    
    return state_df if 'state_df' in locals() else None

def main():
    """Main analysis function."""
    print("=== Comprehensive Memorial Highway Factors Analysis ===")
    print(f"Analyzing {len(states)} states...")
    
    # Load and analyze all states
    all_results = []
    for state in states:
        state_data = load_state_data(state)
        if state_data:
            result = analyze_state_factors(state_data)
            all_results.append(result)
    
    # Cross-state analysis
    consistent_vars, all_correlations = analyze_cross_state_patterns(all_results)
    
    # Highway type analysis
    highway_type_analysis = analyze_highway_types_by_demographics(all_results)
    
    # Create visualizations
    state_df = create_visualizations(all_results, consistent_vars, highway_type_analysis)
    
    # Save results
    output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"
    
    # Save consistent variables
    consistent_vars.to_csv(os.path.join(output_dir, 'consistent_demographic_factors.csv'), index=False)
    
    # Save all correlations
    all_correlations.to_csv(os.path.join(output_dir, 'all_state_correlations.csv'), index=False)
    
    # Save highway type analysis
    if len(highway_type_analysis) > 0:
        highway_type_analysis.to_csv(os.path.join(output_dir, 'highway_type_demographic_correlations.csv'), index=False)
    
    # Save state comparison
    if state_df is not None:
        state_df.to_csv(os.path.join(output_dir, 'state_demographic_highway_comparison.csv'), index=False)
    
    print("\n=== Analysis Complete ===")
    print(f"Results saved to: {output_dir}")
    print(f"Files created:")
    print(f"  - consistent_demographic_factors.csv")
    print(f"  - all_state_correlations.csv")
    print(f"  - highway_type_demographic_correlations.csv")
    print(f"  - state_demographic_highway_comparison.csv")
    print(f"  - cross_state_correlation_comparison.png")
    print(f"  - highway_type_demographic_correlations.png")
    print(f"  - state_income_highways_comparison.png")

if __name__ == "__main__":
    main()