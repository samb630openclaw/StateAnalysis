#!/usr/bin/env python3
"""
Comprehensive State Analysis: Who Gets Memorialized?
Analyzes patterns across multiple states to understand factors contributing to memorialization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import glob

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Output directory
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"
os.makedirs(output_dir, exist_ok=True)

# States with both demographic and highway data
states_to_analyze = {
    'florida': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/florida_counties_demographics_with_voterreg.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/highways.csv',
        'merged_data': '/media/sam/USB DISK/openclaw-capstone-agent/results/florida_merged_data.csv'
    },
    'michigan': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_memorial_highways.csv',
        'merged_data': None  # Michigan merged data not saved
    },
    'california': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_memorial_highways.csv',
        'merged_data': '/media/sam/USB DISK/openclaw-capstone-agent/results/california_merged_data.csv'
    }
}

def load_state_data(state_name, config):
    """Load demographic and highway data for a state."""
    try:
        # Load demographics
        demo_df = pd.read_csv(config['demographics'])
        print(f"Loaded {state_name} demographics: {demo_df.shape}")

        # Try to load highways
        try:
            highway_df = pd.read_csv(config['highways'])
            print(f"Loaded {state_name} highways: {highway_df.shape}")
            return demo_df, highway_df
        except:
            print(f"Could not load highways for {state_name}")
            return demo_df, None
    except Exception as e:
        print(f"Error loading {state_name}: {e}")
        return None, None

def analyze_highway_types(highway_df, state_name):
    """Analyze types of memorial highways."""
    print(f"\nAnalyzing highway types for {state_name}...")
    
    # Look for columns that might indicate highway type/category
    type_columns = []
    for col in highway_df.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['type', 'category', 'honor', 'memorial', 'name', 'purpose']):
            type_columns.append(col)
    
    print(f"Found type columns: {type_columns}")
    
    # Analyze each type column
    type_analysis = {}
    for col in type_columns:
        if highway_df[col].nunique() > 1:  # Only analyze if there are multiple values
            value_counts = highway_df[col].value_counts()
            type_analysis[col] = value_counts
            print(f"\n{col} distribution:")
            print(value_counts.head(10))
    
    return type_analysis

def analyze_highway_attributes(highway_df, state_name):
    """Analyze attributes of memorialized individuals."""
    print(f"\nAnalyzing highway attributes for {state_name}...")
    
    # Look for columns that might indicate attributes
    attribute_columns = []
    for col in highway_df.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['age', 'gender', 'military', 'police', 'fire', 'teacher', 
                                               'veteran', 'service', 'occupation', 'cause', 'death']):
            attribute_columns.append(col)
    
    print(f"Found attribute columns: {attribute_columns}")
    
    # Analyze each attribute column
    attribute_analysis = {}
    for col in attribute_columns:
        if highway_df[col].nunique() > 1:  # Only analyze if there are multiple values
            value_counts = highway_df[col].value_counts()
            attribute_analysis[col] = value_counts
            print(f"\n{col} distribution:")
            print(value_counts.head(10))
    
    return attribute_analysis

def create_highway_type_visualizations(type_analysis, state_name):
    """Create visualizations for highway types."""
    if not type_analysis:
        return
    
    n_plots = len(type_analysis)
    fig, axes = plt.subplots(1, n_plots, figsize=(6*n_plots, 6))
    if n_plots == 1:
        axes = [axes]
    
    for idx, (col, value_counts) in enumerate(type_analysis.items()):
        ax = axes[idx]
        top_10 = value_counts.head(10)
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_10)))
        ax.bar(range(len(top_10)), top_10.values, color=colors)
        ax.set_xticks(range(len(top_10)))
        ax.set_xticklabels(top_10.index, rotation=45, ha='right')
        ax.set_title(f'{state_name} - {col} Distribution')
        ax.set_ylabel('Count')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{state_name}_highway_types.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {state_name}_highway_types.png")

def create_highway_attribute_visualizations(attribute_analysis, state_name):
    """Create visualizations for highway attributes."""
    if not attribute_analysis:
        return
    
    n_plots = len(attribute_analysis)
    fig, axes = plt.subplots(1, n_plots, figsize=(6*n_plots, 6))
    if n_plots == 1:
        axes = [axes]
    
    for idx, (col, value_counts) in enumerate(attribute_analysis.items()):
        ax = axes[idx]
        top_10 = value_counts.head(10)
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_10)))
        ax.bar(range(len(top_10)), top_10.values, color=colors)
        ax.set_xticks(range(len(top_10)))
        ax.set_xticklabels(top_10.index, rotation=45, ha='right')
        ax.set_title(f'{state_name} - {col} Distribution')
        ax.set_ylabel('Count')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{state_name}_highway_attributes.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {state_name}_highway_attributes.png")

def analyze_cross_state_patterns():
    """Analyze patterns across multiple states."""
    all_states_data = []
    
    for state_name, config in states_to_analyze.items():
        demo_df, highway_df = load_state_data(state_name, config)
        
        if demo_df is None or highway_df is None:
            continue
        
        # Analyze highway types and attributes
        type_analysis = analyze_highway_types(highway_df, state_name)
        attribute_analysis = analyze_highway_attributes(highway_df, state_name)
        
        # Create visualizations
        if type_analysis:
            create_highway_type_visualizations(type_analysis, state_name)
        if attribute_analysis:
            create_highway_attribute_visualizations(attribute_analysis, state_name)
        
        # Standardize column names
        demo_cols = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_')
                    for col in demo_df.columns]
        demo_df.columns = demo_cols
        
        # Calculate summary statistics
        state_summary = {
            'state': state_name,
            'n_counties': len(demo_df),
            'n_highways': len(highway_df),
            'median_income': None,
            'poverty_rate': None,
            'college_educated': None,
            'median_age': None,
            'pct_white': None,
            'pct_black': None,
            'pct_hispanic': None,
            'pct_asian': None,
            'republican_pct': None,
            'democrat_pct': None
        }
        
        # Extract values if columns exist
        for col in demo_cols:
            if 'median_income' in col or 'median_household_income' in col:
                state_summary['median_income'] = demo_df[col].median()
            elif 'poverty' in col and 'pct' in col:
                state_summary['poverty_rate'] = demo_df[col].median()
            elif 'college' in col or 'bachelor' in col:
                state_summary['college_educated'] = demo_df[col].median()
            elif 'median_age' in col:
                state_summary['median_age'] = demo_df[col].median()
            elif 'white' in col and 'alone' in col:
                state_summary['pct_white'] = demo_df[col].median()
            elif 'black' in col and 'alone' in col:
                state_summary['pct_black'] = demo_df[col].median()
            elif 'hispanic' in col and 'alone' in col:
                state_summary['pct_hispanic'] = demo_df[col].median()
            elif 'asian' in col and 'alone' in col:
                state_summary['pct_asian'] = demo_df[col].median()
            elif 'republican' in col:
                state_summary['republican_pct'] = demo_df[col].median()
            elif 'democrat' in col:
                state_summary['democrat_pct'] = demo_df[col].median()
        
        all_states_data.append(state_summary)
    
    # Create cross-state comparison
    cross_state_df = pd.DataFrame(all_states_data)
    
    # Save cross-state summary
    cross_state_df.to_csv(os.path.join(output_dir, 'cross_state_demographic_summary.csv'), index=False)
    print("\nSaved cross-state demographic summary")
    
    return cross_state_df

def create_comprehensive_visualizations(cross_state_df):
    """Create comprehensive visualizations comparing states."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Cross-State Demographic Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: Median Income by State
    axes[0,0].bar(cross_state_df['state'], cross_state_df['median_income'])
    axes[0,0].set_title('Median Household Income by State')
    axes[0,0].set_ylabel('Income ($)')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Plot 2: Poverty Rate by State
    axes[0,1].bar(cross_state_df['state'], cross_state_df['poverty_rate'])
    axes[0,1].set_title('Poverty Rate by State')
    axes[0,1].set_ylabel('Poverty Rate (%)')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Plot 3: College Educated by State
    axes[0,2].bar(cross_state_df['state'], cross_state_df['college_educated'])
    axes[0,2].set_title('College Educated by State')
    axes[0,2].set_ylabel('College Educated (%)')
    axes[0,2].tick_params(axis='x', rotation=45)
    
    # Plot 4: Racial Composition
    racial_data = cross_state_df[['state', 'pct_white', 'pct_black', 'pct_hispanic', 'pct_asian']].set_index('state')
    racial_data.plot(kind='bar', stacked=True, ax=axes[1,0])
    axes[1,0].set_title('Racial Composition by State')
    axes[1,0].set_ylabel('Percentage')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # Plot 5: Political Composition
    political_data = cross_state_df[['state', 'republican_pct', 'democrat_pct']].set_index('state')
    political_data.plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('Political Composition by State')
    axes[1,1].set_ylabel('Percentage')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    # Plot 6: Highway Count by State
    axes[1,2].bar(cross_state_df['state'], cross_state_df['n_highways'])
    axes[1,2].set_title('Highway Count by State')
    axes[1,2].set_ylabel('Number of Highways')
    axes[1,2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comprehensive_state_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved comprehensive state comparison plot")

def main():
    """Main analysis function."""
    print("=" * 80)
    print("COMPREHENSIVE STATE ANALYSIS: WHO GETS MEMORIALIZED?")
    print("=" * 80)
    
    # Step 1: Analyze cross-state demographics
    print("\nStep 1: Analyzing cross-state demographics...")
    cross_state_df = analyze_cross_state_patterns()
    
    # Step 2: Create visualizations
    print("\nStep 2: Creating comprehensive visualizations...")
    create_comprehensive_visualizations(cross_state_df)
    
    # Step 3: Print summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE STATE ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"States analyzed: {len(cross_state_df)}")
    print("\nDemographic patterns:")
    for _, row in cross_state_df.iterrows():
        print(f"  {row['state']}: {row['n_counties']} counties, {row['n_highways']} highways")
        if row['median_income']:
            print(f"    Median income=${row['median_income']:,.0f}")
        if row['poverty_rate']:
            print(f"    Poverty rate={row['poverty_rate']:.1f}%")
        if row['college_educated']:
            print(f"    College educated={row['college_educated']:.1f}%")
    
    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    print("1. Highway counts vary significantly by state")
    print("2. Demographic patterns differ across states")
    print("3. Highway types and attributes can reveal patterns in who gets memorialized")
    print("\nNext steps:")
    print("- Analyze specific highway types (military, police, fire, etc.)")
    print("- Compare demographic patterns with highway attributes")
    print("- Identify factors that predict memorialization")
    
    print("\nAnalysis complete! Check results directory for visualizations.")

if __name__ == "__main__":
    main()