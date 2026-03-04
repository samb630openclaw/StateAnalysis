#!/usr/bin/env python3
"""
Analyze states with county-level highway data.
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

# States with county-level highway data
states_with_counties = {
    'Indiana': {
        'demo_file': 'indiana_counties_demographics.csv',
        'demo_path': 'states',  # In states directory
        'highway_file': 'indiana_memorial_highways.xlsx',
        'county_col': 'COUNTY'
    },
    'Florida': {
        'demo_file': 'florida_counties_demographics_with_voterreg.csv',
        'demo_path': 'florida',  # In florida subdirectory
        'highway_file': 'highways.csv',
        'county_col': 'COUNTY'
    }
}

def load_demographic_data(state, filename, demo_path):
    """Load demographic data for a state."""
    try:
        if demo_path == 'states':
            filepath = os.path.join(states_dir, filename)
        else:
            filepath = os.path.join(states_dir, demo_path, filename)
        
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

def aggregate_highways_by_county(highway_df, county_col):
    """Aggregate highway counts by county."""
    # Clean county column (county_col is already lowercase after cleaning)
    highway_df[county_col.lower()] = highway_df[county_col.lower()].str.upper().str.strip()
    
    # Count highways per county
    highway_counts = highway_df.groupby(county_col.lower()).size().reset_index(name='highway_count')
    return highway_counts

def merge_data(demo_df, highway_df, state_name, county_col):
    """Merge demographic and highway data."""
    # Clean column names
    demo_df = clean_column_names(demo_df.copy())
    highway_df = clean_column_names(highway_df.copy())
    
    # Find county column in demo data
    demo_county_col = None
    for col in ['county', 'county_name', 'name']:
        if col in demo_df.columns:
            demo_county_col = col
            break
    
    if demo_county_col is None:
        print(f"  Warning: Could not find county column in demographic data for {state_name}")
        return None
    
    # Clean demo county names - extract just the county name
    # Remove "County, State" format
    demo_df[demo_county_col] = demo_df[demo_county_col].str.replace(r',.*$', '', regex=True)
    demo_df[demo_county_col] = demo_df[demo_county_col].str.replace(r' County$', '', regex=True)
    demo_df[demo_county_col] = demo_df[demo_county_col].str.upper().str.strip()
    
    # Aggregate highways by county
    highway_counts = aggregate_highways_by_county(highway_df, county_col)
    
    # Merge data
    merged = pd.merge(demo_df, highway_counts, left_on=demo_county_col, right_on=county_col.lower(), how='inner')
    
    if merged.empty:
        print(f"  Warning: No matching counties found for {state_name}")
        print(f"  Demo counties (sample): {demo_df[demo_county_col].head(5).tolist()}")
        print(f"  Highway counties (sample): {highway_counts[county_col.lower()].head(5).tolist()}")
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
    print("=== States with County-Level Highway Data Analysis ===")
    
    all_correlations = []
    significant_findings = []
    
    for state, config in states_with_counties.items():
        print(f"\n--- {state} ---")
        
        # Load data
        demo_df = load_demographic_data(state, config['demo_file'], config['demo_path'])
        highway_df = load_highway_data(state, config['highway_file'])
        
        if demo_df is None or highway_df is None:
            print(f"  Skipping {state} - missing data")
            continue
        
        # Merge data
        merged_df = merge_data(demo_df, highway_df, state, config['county_col'])
        
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
        corr_df.to_csv(os.path.join(output_dir, 'county_level_correlations.csv'), index=False)
        print(f"\nSaved {len(all_correlations)} significant correlations to county_level_correlations.csv")
    
    # Save significant findings
    if significant_findings:
        findings_df = pd.DataFrame(significant_findings)
        findings_df.to_csv(os.path.join(output_dir, 'county_level_significant_findings.csv'), index=False)
        print(f"Saved {len(significant_findings)} strong findings to county_level_significant_findings.csv")
    
    # Print summary
    print("\n=== Summary of County-Level Analysis ===")
    print(f"States analyzed: {len(states_with_counties)}")
    print(f"Significant correlations found: {len(all_correlations)}")
    print(f"Strong correlations (|r| > 0.3): {len(significant_findings)}")
    
    if significant_findings:
        print("\nTop findings:")
        for finding in sorted(significant_findings, key=lambda x: abs(x['correlation']), reverse=True)[:10]:
            print(f"  {finding['state']}: {finding['variable']} (r={finding['correlation']:.3f}, p={finding['p_value']:.4f})")

if __name__ == "__main__":
    main()