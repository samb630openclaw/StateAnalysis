#!/usr/bin/env python3
"""
Comprehensive analysis of memorial highway patterns across all states.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Output directory
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"

# States to analyze
states = {
    "Florida": {
        "demographics": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/florida_counties_demographics_with_voterreg.csv",
        "highways": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/highways.csv",
        "county_col": "County",
        "highway_count_col": "highway_count"
    },
    "Michigan": {
        "demographics": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_counties_demographics.csv",
        "highways": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_memorial_highways.csv",
        "county_col": "County",
        "highway_count_col": "highway_count"
    },
    "Nebraska": {
        "demographics": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska_counties_demographics.csv",
        "highways": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska/nebraska-named-highways(1).csv",
        "county_col": "County",
        "highway_count_col": "highway_count"
    },
    "Wisconsin": {
        "demographics": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin_counties_demographics.csv",
        "highways": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin/wisconsin_commemorative_highways_output.csv",
        "county_col": "County",
        "highway_count_col": "highway_count"
    },
    "California": {
        "demographics": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_counties_demographics.csv",
        "highways": "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_memorial_highways.csv",
        "county_col": "County",
        "highway_count_col": "highway_count"
    }
}

def load_and_merge_data(state_name, config):
    """Load and merge demographics and highway data for a state."""
    try:
        # Load demographics
        demo_df = pd.read_csv(config["demographics"])
        print(f"Loaded {state_name} demographics: {len(demo_df)} counties")

        # Load highways
        highway_df = pd.read_csv(config["highways"])
        print(f"Loaded {state_name} highways: {len(highway_df)} records")

        # Count highways per county
        if "County" in highway_df.columns:
            highway_count = highway_df.groupby("County").size().reset_index(name="highway_count")
        elif "Description" in highway_df.columns:
            # Extract county information from Description column
            import re
            county_counts = {}
            for desc in highway_df["Description"].dropna():
                # Look for county names in the description
                matches = re.findall(r'([A-Za-z\s]+) County', str(desc))
                for match in matches:
                    county = match.strip()
                    if county and len(county) > 2:
                        county_counts[county] = county_counts.get(county, 0) + 1
            
            if county_counts:
                highway_count = pd.DataFrame(list(county_counts.items()), columns=["County", "highway_count"])
            else:
                print(f"Warning: No county information found in {state_name} highway data")
                return None
        else:
            # Try to find county information in other columns
            print(f"Warning: No 'County' or 'Description' column in {state_name} highway data")
            return None

        # Merge data
        merged = demo_df.merge(highway_count, on=config["county_col"], how="inner")
        print(f"Merged data: {len(merged)} counties with highway data")

        return merged

    except Exception as e:
        print(f"Error loading {state_name} data: {e}")
        return None

def analyze_state(state_name, df):
    """Analyze a single state's data."""
    if df is None or len(df) < 3:
        print(f"Skipping {state_name}: insufficient data")
        return None

    print(f"\n=== Analyzing {state_name} ===")
    print(f"Counties: {len(df)}")
    print(f"Highway count range: {df['highway_count'].min()} - {df['highway_count'].max()}")
    print(f"Mean highways per county: {df['highway_count'].mean():.2f}")

    # Select numeric columns for correlation analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if "highway_count" in numeric_cols:
        numeric_cols.remove("highway_count")

    results = {
        "state": state_name,
        "n_counties": len(df),
        "highway_stats": {
            "mean": df["highway_count"].mean(),
            "median": df["highway_count"].median(),
            "std": df["highway_count"].std(),
            "min": df["highway_count"].min(),
            "max": df["highway_count"].max()
        },
        "correlations": {},
        "significant_correlations": []
    }

    # Calculate correlations with highway count
    for col in numeric_cols:
        if col in df.columns and df[col].notna().sum() > 10:
            try:
                corr, p_value = stats.pearsonr(df["highway_count"], df[col])
                results["correlations"][col] = {"r": corr, "p": p_value}

                if p_value < 0.05:
                    results["significant_correlations"].append({
                        "variable": col,
                        "r": corr,
                        "p": p_value,
                        "direction": "positive" if corr > 0 else "negative"
                    })
            except:
                continue

    # Sort significant correlations by absolute value
    results["significant_correlations"].sort(key=lambda x: abs(x["r"]), reverse=True)

    return results

def create_comprehensive_visualization(all_results):
    """Create a comprehensive visualization of patterns across states."""
    # Prepare data for visualization
    state_names = []
    multi_racial_corrs = []
    black_pop_corrs = []
    education_corrs = []
    income_corrs = []

    for state, results in all_results.items():
        if results is None:
            continue

        state_names.append(state)

        # Find correlations for key variables
        multi_racial_corr = None
        black_pop_corr = None
        education_corr = None
        income_corr = None

        for corr_data in results["correlations"].items():
            var_name, corr_info = corr_data
            if "TwoOrMore" in var_name or "multi" in var_name.lower():
                multi_racial_corr = corr_info["r"]
            elif "Black" in var_name or "black" in var_name.lower():
                black_pop_corr = corr_info["r"]
            elif "Bachelor" in var_name or "HS_Grad" in var_name:
                education_corr = corr_info["r"]
            elif "Income" in var_name or "income" in var_name.lower():
                income_corr = corr_info["r"]

        multi_racial_corrs.append(multi_racial_corr if multi_racial_corr is not None else np.nan)
        black_pop_corrs.append(black_pop_corr if black_pop_corr is not None else np.nan)
        education_corrs.append(education_corr if education_corr is not None else np.nan)
        income_corrs.append(income_corr if income_corr is not None else np.nan)

    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Multi-racial population correlation
    axes[0, 0].bar(state_names, multi_racial_corrs, color='skyblue')
    axes[0, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[0, 0].set_title('Multi-Racial Population Correlation with Highway Count')
    axes[0, 0].set_ylabel('Correlation (r)')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Black population correlation
    axes[0, 1].bar(state_names, black_pop_corrs, color='lightcoral')
    axes[0, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[0, 1].set_title('Black Population Correlation with Highway Count')
    axes[0, 1].set_ylabel('Correlation (r)')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Education correlation
    axes[1, 0].bar(state_names, education_corrs, color='lightgreen')
    axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1, 0].set_title('Education Level Correlation with Highway Count')
    axes[1, 0].set_ylabel('Correlation (r)')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Income correlation
    axes[1, 1].bar(state_names, income_corrs, color='gold')
    axes[1, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1, 1].set_title('Income Correlation with Highway Count')
    axes[1, 1].set_ylabel('Correlation (r)')
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "comprehensive_correlation_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved comprehensive correlation comparison to {output_dir}")

def main():
    """Main analysis function."""
    all_results = {}

    # Analyze each state
    for state_name, config in states.items():
        df = load_and_merge_data(state_name, config)
        results = analyze_state(state_name, df)
        all_results[state_name] = results

    # Create comprehensive visualization
    create_comprehensive_visualization(all_results)

    # Print summary
    print("\n" + "="*80)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("="*80)

    for state_name, results in all_results.items():
        if results is None:
            continue

        print(f"\n{state_name}:")
        print(f"  Counties analyzed: {results['n_counties']}")
        print(f"  Mean highways per county: {results['highway_stats']['mean']:.2f}")
        print(f"  Significant correlations found: {len(results['significant_correlations'])}")

        if results['significant_correlations']:
            print(f"  Top 3 correlations:")
            for i, corr in enumerate(results['significant_correlations'][:3]):
                print(f"    {i+1}. {corr['variable']}: r={corr['r']:.3f}, p={corr['p']:.4f}")

    # Save results to CSV
    summary_data = []
    for state_name, results in all_results.items():
        if results is None:
            continue

        for corr in results['significant_correlations']:
            summary_data.append({
                'State': state_name,
                'Variable': corr['variable'],
                'Correlation': corr['r'],
                'P_Value': corr['p'],
                'Direction': corr['direction']
            })

    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(os.path.join(output_dir, "comprehensive_correlation_summary.csv"), index=False)
        print(f"\nSaved comprehensive correlation summary to {output_dir}")

if __name__ == "__main__":
    main()
