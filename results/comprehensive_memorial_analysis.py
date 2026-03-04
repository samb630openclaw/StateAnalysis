#!/usr/bin/env python3
"""
Comprehensive Memorial Highway Analysis
Analyzes patterns across multiple states to understand factors contributing to memorialization.
Goal: Understand why some people get memorialized over others.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import glob
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Output directory
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"
os.makedirs(output_dir, exist_ok=True)

# States with both demographic and highway data
states_to_analyze = {
    'california': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_memorial_highways.csv',
    },
    'florida': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/florida_counties_demographics_with_voterreg.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/highways.csv',
    },
    'michigan': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_memorial_highways.csv',
    },
    'indiana': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana/indiana_memorial_highways.xlsx',
    },
    'nebraska': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska/nebraska-named-highways(1).csv',
    },
    'wisconsin': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin/wisconsin_commemorative_highways.csv',
    },
    'minnesota': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/minnesota_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/minnesota/minnesota_memorial_highways.csv',
    },
    'utah': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/utah_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/utah/utah_memorial_highways.csv',
    },
    'connecticut': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/connecticut_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/connecticut/connecticut_memorial_highways.csv',
    },
    'montana': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/montana_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/montana/montana_memorial_highways.csv',
    },
}

def load_state_data(state_name, config):
    """Load demographic and highway data for a state."""
    try:
        # Load demographics
        demo_df = pd.read_csv(config['demographics'])
        print(f"✓ {state_name}: Loaded demographics ({demo_df.shape[0]} counties)")

        # Try to load highways
        try:
            if config['highways'].endswith('.xlsx'):
                highway_df = pd.read_excel(config['highways'])
            else:
                highway_df = pd.read_csv(config['highways'])
            print(f"✓ {state_name}: Loaded highways ({highway_df.shape[0]} highways)")
            return demo_df, highway_df
        except Exception as e:
            print(f"✗ {state_name}: Could not load highways - {e}")
            return demo_df, None
    except Exception as e:
        print(f"✗ {state_name}: Could not load demographics - {e}")
        return None, None

def clean_column_names(df):
    """Clean column names for consistency."""
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '', regex=True)
    return df

def analyze_highway_types(highway_df, state_name):
    """Analyze highway types and categories."""
    if highway_df is None:
        return None
    
    # Look for columns that might indicate highway type or category
    type_columns = []
    for col in highway_df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['type', 'category', 'kind', 'class', 'purpose', 'memorial', 'honor']):
            type_columns.append(col)
    
    if type_columns:
        print(f"  Highway type columns found: {type_columns}")
        # Analyze the first type column
        type_col = type_columns[0]
        if type_col in highway_df.columns:
            type_counts = highway_df[type_col].value_counts()
            print(f"  Highway type distribution:")
            for idx, count in type_counts.head(10).items():
                print(f"    {idx}: {count}")
    
    return type_columns

def analyze_state_patterns(state_name, demo_df, highway_df):
    """Analyze patterns for a single state."""
    if demo_df is None or highway_df is None:
        return None
    
    print(f"\n=== Analyzing {state_name.title()} ===")
    
    # Clean column names
    demo_df = clean_column_names(demo_df)
    highway_df = clean_column_names(highway_df)
    
    # Count highways by county
    # Look for county column in highway data
    county_col = None
    for col in highway_df.columns:
        if 'county' in col.lower():
            county_col = col
            break
    
    if county_col:
        highway_counts = highway_df.groupby(county_col).size().reset_index(name='highway_count')
        print(f"  Highway counts by county: {highway_counts.shape[0]} counties")
        
        # Merge with demographics
        # Look for county column in demographics
        demo_county_col = None
        for col in demo_df.columns:
            if 'county' in col.lower():
                demo_county_col = col
                break
        
        if demo_county_col:
            # Standardize county names
            highway_counts[county_col] = highway_counts[county_col].str.title().str.strip()
            demo_df[demo_county_col] = demo_df[demo_county_col].str.title().str.strip()
            
            # Merge
            merged = pd.merge(demo_df, highway_counts, left_on=demo_county_col, right_on=county_col, how='inner')
            print(f"  Merged data: {merged.shape[0]} counties with both demographics and highways")
            
            if merged.shape[0] > 0:
                # Analyze correlations
                numeric_cols = merged.select_dtypes(include=[np.number]).columns
                highway_col = 'highway_count'
                
                if highway_col in numeric_cols:
                    correlations = {}
                    for col in numeric_cols:
                        if col != highway_col:
                            try:
                                corr, p_value = stats.pearsonr(merged[col].dropna(), merged[highway_col].dropna())
                                if p_value < 0.05:  # Only significant correlations
                                    correlations[col] = {'correlation': corr, 'p_value': p_value}
                            except:
                                pass
                    
                    # Sort by absolute correlation
                    sorted_corrs = sorted(correlations.items(), key=lambda x: abs(x[1]['correlation']), reverse=True)
                    
                    print(f"  Significant correlations with highway count:")
                    for col, stats_dict in sorted_corrs[:10]:  # Top 10
                        print(f"    {col}: r={stats_dict['correlation']:.3f}, p={stats_dict['p_value']:.4f}")
                    
                    return {
                        'state': state_name,
                        'counties': merged.shape[0],
                        'highways': highway_df.shape[0],
                        'correlations': sorted_corrs[:10],
                        'merged_data': merged
                    }
    
    return None

def create_comprehensive_visualization(all_results):
    """Create comprehensive visualization of patterns across states."""
    if not all_results:
        return
    
    # Collect all significant correlations
    all_correlations = []
    for result in all_results:
        state = result['state']
        for col, stats_dict in result['correlations']:
            all_correlations.append({
                'state': state,
                'variable': col,
                'correlation': stats_dict['correlation'],
                'p_value': stats_dict['p_value']
            })
    
    if not all_correlations:
        print("No significant correlations found across states")
        return
    
    corr_df = pd.DataFrame(all_correlations)
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Top correlations by state
    ax1 = axes[0, 0]
    top_corrs = corr_df.groupby('state').apply(lambda x: x.nlargest(3, 'correlation')).reset_index(drop=True)
    for state in corr_df['state'].unique():
        state_corrs = top_corrs[top_corrs['state'] == state]
        if not state_corrs.empty:
            ax1.barh(range(len(state_corrs)), state_corrs['correlation'], label=state)
    ax1.set_yticks(range(len(top_corrs)))
    ax1.set_yticklabels([f"{row['state']}: {row['variable']}" for _, row in top_corrs.iterrows()])
    ax1.set_xlabel('Correlation Coefficient')
    ax1.set_title('Top Correlations by State')
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    # 2. Correlation distribution
    ax2 = axes[0, 1]
    ax2.hist(corr_df['correlation'], bins=20, edgecolor='black')
    ax2.set_xlabel('Correlation Coefficient')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Significant Correlations')
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    
    # 3. Variables that appear across multiple states
    ax3 = axes[1, 0]
    variable_counts = corr_df['variable'].value_counts()
    if len(variable_counts) > 0:
        top_vars = variable_counts.head(10)
        ax3.barh(range(len(top_vars)), top_vars.values)
        ax3.set_yticks(range(len(top_vars)))
        ax3.set_yticklabels(top_vars.index)
        ax3.set_xlabel('Number of States')
        ax3.set_title('Variables Correlated with Highway Count Across States')
    
    # 4. Average correlation by variable type
    ax4 = axes[1, 1]
    # Group variables by type
    demographic_vars = ['pop', 'race', 'age', 'income', 'education', 'poverty', 'voter', 'republican', 'democrat']
    corr_df['var_type'] = 'other'
    for var_type in demographic_vars:
        corr_df.loc[corr_df['variable'].str.contains(var_type, case=False), 'var_type'] = var_type
    
    avg_corrs = corr_df.groupby('var_type')['correlation'].mean().sort_values()
    ax4.barh(range(len(avg_corrs)), avg_corrs.values)
    ax4.set_yticks(range(len(avg_corrs)))
    ax4.set_yticklabels(avg_corrs.index)
    ax4.set_xlabel('Average Correlation')
    ax4.set_title('Average Correlation by Variable Type')
    ax4.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comprehensive_memorial_patterns.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Comprehensive visualization saved: comprehensive_memorial_patterns.png")

def main():
    """Main analysis function."""
    print("=== Comprehensive Memorial Highway Analysis ===")
    print("Goal: Understand why some people get memorialized over others")
    print()
    
    all_results = []
    
    for state_name, config in states_to_analyze.items():
        demo_df, highway_df = load_state_data(state_name, config)
        
        if demo_df is not None and highway_df is not None:
            # Analyze highway types
            analyze_highway_types(highway_df, state_name)
            
            # Analyze patterns
            result = analyze_state_patterns(state_name, demo_df, highway_df)
            if result:
                all_results.append(result)
    
    # Create comprehensive visualization
    if all_results:
        create_comprehensive_visualization(all_results)
        
        # Save summary
        summary_df = pd.DataFrame([
            {
                'state': r['state'],
                'counties_analyzed': r['counties'],
                'highways_total': r['highways'],
                'top_correlation': r['correlations'][0][0] if r['correlations'] else None,
                'top_correlation_value': r['correlations'][0][1]['correlation'] if r['correlations'] else None,
                'top_correlation_p': r['correlations'][0][1]['p_value'] if r['correlations'] else None,
            }
            for r in all_results
        ])
        summary_df.to_csv(os.path.join(output_dir, 'memorial_analysis_summary.csv'), index=False)
        print(f"\n✓ Analysis summary saved: memorial_analysis_summary.csv")
        
        # Print key findings
        print("\n=== KEY FINDINGS: Who Gets Memorialized? ===")
        print()
        
        # Find variables that appear across multiple states
        all_vars = []
        for r in all_results:
            for col, stats_dict in r['correlations']:
                all_vars.append(col)
        
        from collections import Counter
        var_counts = Counter(all_vars)
        
        print("Variables correlated with highway count across multiple states:")
        for var, count in var_counts.most_common(10):
            if count >= 2:  # Only show variables that appear in 2+ states
                print(f"  {var}: appears in {count} states")
        
        print("\n=== CONCLUSION ===")
        print("Based on analysis across multiple states, the following factors appear to contribute to memorialization:")
        print()
        
        # Group by variable type
        demographic_vars = ['pop', 'race', 'age', 'income', 'education', 'poverty', 'voter', 'republican', 'democrat']
        findings = {}
        
        for r in all_results:
            for col, stats_dict in r['correlations']:
                for var_type in demographic_vars:
                    if var_type in col.lower():
                        if var_type not in findings:
                            findings[var_type] = []
                        findings[var_type].append((r['state'], stats_dict['correlation']))
        
        for var_type, correlations in findings.items():
            if len(correlations) >= 2:
                avg_corr = np.mean([c[1] for c in correlations])
                states = ', '.join([c[0] for c in correlations])
                print(f"  {var_type.title()}: Average correlation {avg_corr:.3f} (states: {states})")
    
    else:
        print("\nNo states could be analyzed successfully.")

if __name__ == "__main__":
    main()