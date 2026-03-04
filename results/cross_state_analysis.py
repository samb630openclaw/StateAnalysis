#!/usr/bin/env python3
"""
Cross-State Analysis: Who Gets Memorialized?
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
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/highways.csv'
    },
    'michigan': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_memorial_highways.csv'
    },
    'texas': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/texas/texas_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/texas/texas_data_with_counties.csv'
    },
    'wisconsin': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin/wisconsin_commemorative_highways_output.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin/wisconsin_commemorative_highways.csv'
    },
    'indiana': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana/indiana_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana/indiana_counties_demographics.csv'  # Using merged data
    },
    'nebraska': {
        'demographics': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska/nebraska_counties_demographics.csv',
        'highways': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska/nebraska_merged_data.csv'
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
            # If highways file doesn't exist, check if it's already merged
            if 'highway' in config['highways'].lower() or 'merged' in config['highways'].lower():
                # This might be merged data already
                merged_df = pd.read_csv(config['highways'])
                print(f"Loaded {state_name} merged data: {merged_df.shape}")
                return merged_df, None
            else:
                print(f"Could not load highways for {state_name}")
                return demo_df, None
    except Exception as e:
        print(f"Error loading {state_name}: {e}")
        return None, None

def analyze_cross_state_patterns():
    """Analyze patterns across multiple states."""
    all_states_data = []

    for state_name, config in states_to_analyze.items():
        demo_df, highway_df = load_state_data(state_name, config)

        if demo_df is None:
            continue

        # Standardize column names
        demo_cols = [col.lower().replace(' ', '_').replace('%', 'pct').replace('-', '_')
                    for col in demo_df.columns]
        demo_df.columns = demo_cols

        # Look for common demographic variables
        common_vars = []
        for col in demo_cols:
            if any(term in col for term in ['median_income', 'poverty', 'education', 'age',
                                           'white', 'black', 'hispanic', 'asian', 'republican',
                                           'democrat', 'voter', 'population']):
                common_vars.append(col)

        # Calculate summary statistics
        state_summary = {
            'state': state_name,
            'n_counties': len(demo_df),
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
    print("Saved cross-state demographic summary")

    return cross_state_df

def create_cross_state_visualizations(cross_state_df):
    """Create visualizations comparing states."""
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

    # Plot 6: Median Age by State
    axes[1,2].bar(cross_state_df['state'], cross_state_df['median_age'])
    axes[1,2].set_title('Median Age by State')
    axes[1,2].set_ylabel('Age (years)')
    axes[1,2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cross_state_demographic_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved cross-state demographic comparison plot")

def analyze_highway_patterns():
    """Analyze highway patterns across states."""
    highway_patterns = []

    # Florida highway analysis
    try:
        florida_highways = pd.read_csv('/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/highways.csv')
        # Count highways by type
        if 'type' in florida_highways.columns:
            type_counts = florida_highways['type'].value_counts()
            highway_patterns.append({
                'state': 'florida',
                'total_highways': len(florida_highways),
                'most_common_type': type_counts.index[0] if len(type_counts) > 0 else 'Unknown',
                'type_distribution': type_counts.to_dict()
            })
    except Exception as e:
        print(f"Error analyzing Florida highways: {e}")

    # Michigan highway analysis
    try:
        michigan_highways = pd.read_csv('/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_memorial_highways.csv')
        # Count highways by category
        if 'category' in michigan_highways.columns:
            category_counts = michigan_highways['category'].value_counts()
            highway_patterns.append({
                'state': 'michigan',
                'total_highways': len(michigan_highways),
                'most_common_category': category_counts.index[0] if len(category_counts) > 0 else 'Unknown',
                'category_distribution': category_counts.to_dict()
            })
    except Exception as e:
        print(f"Error analyzing Michigan highways: {e}")

    # Texas highway analysis
    try:
        texas_highways = pd.read_csv('/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/texas/texas_data_with_counties.csv')
        # Count highways by type
        if 'type' in texas_highways.columns:
            type_counts = texas_highways['type'].value_counts()
            highway_patterns.append({
                'state': 'texas',
                'total_highways': len(texas_highways),
                'most_common_type': type_counts.index[0] if len(type_counts) > 0 else 'Unknown',
                'type_distribution': type_counts.to_dict()
            })
    except Exception as e:
        print(f"Error analyzing Texas highways: {e}")

    # Save highway patterns
    if highway_patterns:
        highway_df = pd.DataFrame(highway_patterns)
        highway_df.to_csv(os.path.join(output_dir, 'highway_patterns_by_state.csv'), index=False)
        print("Saved highway patterns by state")

    return highway_patterns

def main():
    """Main analysis function."""
    print("=" * 60)
    print("CROSS-STATE ANALYSIS: WHO GETS MEMORIALIZED?")
    print("=" * 60)

    # Step 1: Analyze cross-state demographics
    print("\nStep 1: Analyzing cross-state demographics...")
    cross_state_df = analyze_cross_state_patterns()

    # Step 2: Create visualizations
    print("\nStep 2: Creating cross-state visualizations...")
    create_cross_state_visualizations(cross_state_df)

    # Step 3: Analyze highway patterns
    print("\nStep 3: Analyzing highway patterns across states...")
    highway_patterns = analyze_highway_patterns()

    # Step 4: Print summary
    print("\n" + "=" * 60)
    print("CROSS-STATE ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"States analyzed: {len(cross_state_df)}")
    print("\nDemographic patterns:")
    for _, row in cross_state_df.iterrows():
        print(f"  {row['state']}: Median income=${row['median_income']:,.0f}, "
              f"Poverty={row['poverty_rate']:.1f}%, "
              f"College educated={row['college_educated']:.1f}%")

    print("\nHighway patterns:")
    for pattern in highway_patterns:
        print(f"  {pattern['state']}: {pattern['total_highways']} highways, "
              f"Most common: {pattern.get('most_common_type', pattern.get('most_common_category', 'Unknown'))}")

    print("\nAnalysis complete! Check results directory for visualizations.")

if __name__ == "__main__":
    main()