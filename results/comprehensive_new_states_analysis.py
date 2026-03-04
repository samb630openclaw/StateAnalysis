#!/usr/bin/env python3
"""
Comprehensive analysis of new states with both demographic and highway data.
This script analyzes Connecticut, Indiana, Louisiana, Minnesota, Montana, Nebraska, Utah, and Wisconsin
to find additional patterns in memorial highway designations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
states_dir = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/"
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"

# States to analyze
states_to_analyze = {
    'Connecticut': {
        'demo_file': 'connecticut_counties_demographics.csv',
        'highway_file': 'connecticut_memorial_highways.csv'
    },
    'Indiana': {
        'demo_file': 'indiana_counties_demographics.csv',
        'highway_file': 'indiana_memorial_highways.xlsx'
    },
    'Louisiana': {
        'demo_file': 'louisiana_counties_demographics.csv',
        'highway_file': 'louisiana_memorial_highways.csv'
    },
    'Minnesota': {
        'demo_file': 'minnesota_counties_demographics.csv',
        'highway_file': 'minnesota_memorial_highways.csv'
    },
    'Montana': {
        'demo_file': 'montana_counties_demographics.csv',
        'highway_file': 'montana_memorial_highways.csv'
    },
    'Nebraska': {
        'demo_file': 'nebraska_counties_demographics.csv',
        'highway_file': 'nebraska-named-highways(1).csv'
    },
    'Utah': {
        'demo_file': 'utah_counties_demographics.csv',
        'highway_file': 'utah_memorial_highways.csv'
    },
    'Wisconsin': {
        'demo_file': 'wisconsin_counties_demographics.csv',
        'highway_file': 'wisconsin_commemorative_highways_output.csv'
    }
}

def load_demographic_data(state, filename):
    """Load demographic data for a state."""
    try:
        filepath = os.path.join(states_dir, f"{state.lower()}", filename)
        if not os.path.exists(filepath):
            # Try in states directory
            filepath = os.path.join(states_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"  Warning: Demographic file not found for {state}")
            return None
        
        df = pd.read_csv(filepath)
        print(f"  Loaded {state} demographics: {df.shape}")
        return df
    except Exception as e:
        print(f"  Error loading {state} demographics: {e}")
        return None

def load_highway_data(state, filename):
    """Load highway data for a state."""
    try:
        filepath = os.path.join(states_dir, state.lower(), filename)
        
        if not os.path.exists(filepath):
            print(f"  Warning: Highway file not found for {state}")
            return None
        
        if filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
        
        print(f"  Loaded {state} highways: {df.shape}")
        return df
    except Exception as e:
        print(f"  Error loading {state} highways: {e}")
        return None

def clean_column_names(df):
    """Clean column names for analysis."""
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
    return df

def aggregate_highways_by_county(highway_df, state_name):
    """Aggregate highway counts by county."""
    # Try different column names for county
    county_cols = ['county', 'county_name', 'county_fips', 'fips', 'jurisdiction']
    
    for col in county_cols:
        if col in highway_df.columns:
            # Count highways per county
            highway_counts = highway_df.groupby(col).size().reset_index(name='highway_count')
            return highway_counts
    
    # If no county column found, try to extract from other columns
    print(f"  Warning: No county column found in {state_name} highway data")
    return None

def merge_data(demo_df, highway_df, state_name):
    """Merge demographic and highway data."""
    # Clean column names
    demo_df = clean_column_names(demo_df)
    highway_df = clean_column_names(highway_df)
    
    # Aggregate highways by county
    highway_counts = aggregate_highways_by_county(highway_df, state_name)
    
    if highway_counts is None:
        return None
    
    # Try to find common county column
    demo_county_col = None
    highway_county_col = None
    
    for col in ['county', 'county_name', 'name']:
        if col in demo_df.columns:
            demo_county_col = col
            break
    
    for col in ['county', 'county_name', 'jurisdiction']:
        if col in highway_counts.columns:
            highway_county_col = col
            break
    
    if demo_county_col is None or highway_county_col is None:
        print(f"  Warning: Could not find common county column for {state_name}")
        return None
    
    # Merge data
    merged = pd.merge(demo_df, highway_counts, left_on=demo_county_col, right_on=highway_county_col, how='inner')
    
    if merged.empty:
        print(f"  Warning: No matching counties found for {state_name}")
        return None
    
    print(f"  Merged {state_name} data: {merged.shape}")
    return merged

def analyze_correlations(df, state_name):
    """Analyze correlations between demographic variables and highway counts."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if 'highway_count' not in numeric_cols:
        print(f"  Warning: highway_count not found in {state_name} data")
        return None
    
    # Calculate correlations
    correlations = {}
    for col in numeric_cols:
        if col != 'highway_count':
            try:
                corr, p_value = stats.pearsonr(df[col].dropna(), df['highway_count'].dropna())
                if not np.isnan(corr):
                    correlations[col] = {'correlation': corr, 'p_value': p_value}
            except:
                continue
    
    return correlations

def save_correlation_plot(df, state_name, var1, var2, corr, p_value):
    """Save correlation plot."""
    plt.figure(figsize=(10, 6))
    plt.scatter(df[var1], df[var2], alpha=0.6)
    plt.xlabel(var1.replace('_', ' ').title())
    plt.ylabel(var2.replace('_', ' ').title())
    plt.title(f'{state_name}: {var1.replace("_", " ").title()} vs Highway Count\nr={corr:.3f}, p={p_value:.4f}')
    
    # Add trend line
    z = np.polyfit(df[var1], df[var2], 1)
    p = np.poly1d(z)
    plt.plot(df[var1], p(df[var1]), "r--", alpha=0.8)
    
    filename = f"{state_name.lower()}_{var1}_vs_highways.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    plt.close()
    
    return filename

def main():
    print("=== Comprehensive New States Analysis ===")
    print("Analyzing states with both demographic and highway data...")
    
    all_correlations = []
    significant_findings = []
    
    for state, files in states_to_analyze.items():
        print(f"\n--- {state} ---")
        
        # Load data
        demo_df = load_demographic_data(state, files['demo_file'])
        highway_df = load_highway_data(state, files['highway_file'])
        
        if demo_df is None or highway_df is None:
            print(f"  Skipping {state} - missing data")
            continue
        
        # Merge data
        merged_df = merge_data(demo_df, highway_df, state)
        
        if merged_df is None:
            print(f"  Skipping {state} - could not merge data")
            continue
        
        # Analyze correlations
        correlations = analyze_correlations(merged_df, state)
        
        if correlations is None:
            print(f"  Skipping {state} - no correlations found")
            continue
        
        # Find significant correlations (p < 0.05)
        for var, stats in correlations.items():
            if stats['p_value'] < 0.05:
                all_correlations.append({
                    'state': state,
                    'variable': var,
                    'correlation': stats['correlation'],
                    'p_value': stats['p_value']
                })
                
                # Save plot for strong correlations (|r| > 0.3)
                if abs(stats['correlation']) > 0.3:
                    filename = save_correlation_plot(merged_df, state, var, 'highway_count', 
                                                    stats['correlation'], stats['p_value'])
                    significant_findings.append({
                        'state': state,
                        'variable': var,
                        'correlation': stats['correlation'],
                        'p_value': stats['p_value'],
                        'plot_file': filename
                    })
                    print(f"  Strong correlation: {var} (r={stats['correlation']:.3f}, p={stats['p_value']:.4f})")
    
    # Save all correlations
    if all_correlations:
        corr_df = pd.DataFrame(all_correlations)
        corr_df.to_csv(os.path.join(output_dir, 'new_states_correlations.csv'), index=False)
        print(f"\nSaved {len(all_correlations)} significant correlations to new_states_correlations.csv")
    
    # Save significant findings
    if significant_findings:
        findings_df = pd.DataFrame(significant_findings)
        findings_df.to_csv(os.path.join(output_dir, 'new_states_significant_findings.csv'), index=False)
        print(f"Saved {len(significant_findings)} strong findings to new_states_significant_findings.csv")
    
    # Print summary
    print("\n=== Summary of New States Analysis ===")
    print(f"States analyzed: {len(states_to_analyze)}")
    print(f"Significant correlations found: {len(all_correlations)}")
    print(f"Strong correlations (|r| > 0.3): {len(significant_findings)}")
    
    if significant_findings:
        print("\nTop findings:")
        for finding in sorted(significant_findings, key=lambda x: abs(x['correlation']), reverse=True)[:10]:
            print(f"  {finding['state']}: {finding['variable']} (r={finding['correlation']:.3f}, p={finding['p_value']:.4f})")

if __name__ == "__main__":
    main()