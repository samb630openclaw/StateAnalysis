#!/usr/bin/env python3
"""
California Analysis: Memorial Highways vs Demographics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import os
import re

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Paths
demographics_path = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_counties_demographics.csv"
highways_path = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_memorial_highways.csv"
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"

print("=== California Analysis: Memorial Highways vs Demographics ===")
print(f"Demographics: {demographics_path}")
print(f"Highways: {highways_path}")
print(f"Output: {output_dir}")
print()

# Load data
print("Loading data...")
try:
    demographics = pd.read_csv(demographics_path)
    print(f"Demographics loaded: {demographics.shape}")
    print(f"Columns: {list(demographics.columns)}")
    print()
except Exception as e:
    print(f"Error loading demographics: {e}")
    exit()

try:
    highways = pd.read_csv(highways_path)
    print(f"Highways loaded: {highways.shape}")
    print(f"Columns: {list(highways.columns)}")
    print()
except Exception as e:
    print(f"Error loading highways: {e}")
    exit()

# Explore demographics data
print("=== Demographics Data Exploration ===")
print(demographics.head())
print()
print("Demographics info:")
print(demographics.info())
print()

# Check for county column
county_cols = [col for col in demographics.columns if 'county' in col.lower()]
print(f"County columns found: {county_cols}")
print()

# Explore highways data
print("=== Highways Data Exploration ===")
print(highways.head())
print()
print("Highways info:")
print(highways.info())
print()

# Check for county information in highways
print("=== Highway Location Analysis ===")
print("Sample locations:")
for i, loc in enumerate(highways['from_location'].head(10)):
    print(f"{i}: {loc}")
print()

# Try to extract counties from highway locations
def extract_counties(location):
    """Extract county names from location string"""
    if pd.isna(location):
        return []
    
    # Common patterns for county mentions
    patterns = [
        r'([A-Z][a-z]+ County)',
        r'([A-Z][a-z]+/[A-Z][a-z]+ County)',
        r'([A-Z][a-z]+-[A-Z][a-z]+ County)',
    ]
    
    counties = []
    for pattern in patterns:
        matches = re.findall(pattern, location)
        counties.extend(matches)
    
    return list(set(counties))

# Apply county extraction to both from_location and to_location
highways['from_counties'] = highways['from_location'].apply(extract_counties)
highways['to_counties'] = highways['to_location'].apply(extract_counties)

# Combine all counties
highways['all_counties'] = highways.apply(
    lambda row: list(set(row['from_counties'] + row['to_counties'])), axis=1
)

print("Sample extracted counties:")
for i, counties in enumerate(highways['all_counties'].head(10)):
    print(f"{i}: {counties}")
print()

# Count highways per county
all_counties = []
for county_list in highways['all_counties']:
    all_counties.extend(county_list)

county_counts = pd.Series(all_counties).value_counts()
print(f"Highways per county (top 20):")
print(county_counts.head(20))
print()

# Create highway count by county
highway_counts = pd.DataFrame({
    'County': county_counts.index,
    'highway_count': county_counts.values
})

print(f"Total counties with highways: {len(highway_counts)}")
print()

# Clean county names in demographics
print("=== Cleaning County Names ===")
# Check county column
if county_cols:
    county_col = county_cols[0]
    print(f"Using county column: {county_col}")
    print(f"Sample county names: {demographics[county_col].head(10).tolist()}")
    
    # Clean county names
    demographics['county_clean'] = demographics[county_col].str.replace(r', California', '', regex=True)
    demographics['county_clean'] = demographics['county_clean'].str.strip()
    print(f"Sample cleaned county names: {demographics['county_clean'].head(10).tolist()}")
else:
    print("No county column found!")
    exit()

# Merge demographics with highway counts
print("=== Merging Data ===")
merged = pd.merge(
    demographics,
    highway_counts,
    left_on='county_clean',
    right_on='County',
    how='left'
)

# Fill missing highway counts with 0
merged['highway_count'] = merged['highway_count'].fillna(0)

print(f"Merged data shape: {merged.shape}")
print(f"Counties with highways: {(merged['highway_count'] > 0).sum()}")
print(f"Counties without highways: {(merged['highway_count'] == 0).sum()}")
print()

# Save merged data
merged.to_csv(os.path.join(output_dir, 'california_merged_data.csv'), index=False)
print(f"Saved merged data to: {os.path.join(output_dir, 'california_merged_data.csv')}")
print()

# Data summary
print("=== Data Summary ===")
print(f"Total counties: {len(merged)}")
print(f"Total highways: {merged['highway_count'].sum()}")
print(f"Average highways per county: {merged['highway_count'].mean():.2f}")
print(f"Median highways per county: {merged['highway_count'].median():.2f}")
print(f"Max highways in a county: {merged['highway_count'].max()}")
print()

# Identify numeric columns for analysis
numeric_cols = merged.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [col for col in numeric_cols if col not in ['highway_count', 'GEOID']]
print(f"Numeric demographic columns: {numeric_cols}")
print()

# Correlation analysis
print("=== Correlation Analysis ===")
correlations = []
for col in numeric_cols:
    try:
        # Pearson correlation
        pearson_r, pearson_p = stats.pearsonr(merged[col].dropna(), merged.loc[merged[col].notna(), 'highway_count'])
        
        # Spearman correlation
        spearman_r, spearman_p = stats.spearmanr(merged[col].dropna(), merged.loc[merged[col].notna(), 'highway_count'])
        
        correlations.append({
            'variable': col,
            'pearson_r': pearson_r,
            'pearson_p': pearson_p,
            'spearman_r': spearman_r,
            'spearman_p': spearman_p,
            'significant': pearson_p < 0.05 or spearman_p < 0.05
        })
    except Exception as e:
        print(f"Error calculating correlation for {col}: {e}")

corr_df = pd.DataFrame(correlations)
print("Correlations with highway count (sorted by absolute Pearson r):")
print(corr_df.sort_values('pearson_r', key=abs, ascending=False).to_string())
print()

# Save correlations
corr_df.to_csv(os.path.join(output_dir, 'california_correlation_matrix.csv'), index=False)
print(f"Saved correlations to: {os.path.join(output_dir, 'california_correlation_matrix.csv')}")
print()

# Create correlation heatmap
print("=== Creating Correlation Heatmap ===")
plt.figure(figsize=(14, 12))
corr_matrix = merged[numeric_cols + ['highway_count']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', 
            cbar_kws={'shrink': 0.8}, square=True)
plt.title('California: Correlation Matrix - Demographics vs Highway Count', fontsize=16, pad=20)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'california_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
print(f"Saved correlation heatmap to: {os.path.join(output_dir, 'california_correlation_heatmap.png')}")
plt.close()
print()

# Group comparisons: High vs Low highway counties
print("=== Group Comparisons: High vs Low Highway Counties ===")
median_highways = merged['highway_count'].median()
merged['highway_group'] = np.where(merged['highway_count'] >= median_highways, 'High', 'Low')

ttest_results = []
for col in numeric_cols:
    try:
        high_group = merged[merged['highway_group'] == 'High'][col].dropna()
        low_group = merged[merged['highway_group'] == 'Low'][col].dropna()
        
        if len(high_group) > 2 and len(low_group) > 2:
            t_stat, p_value = stats.ttest_ind(high_group, low_group, equal_var=False)
            
            ttest_results.append({
                'variable': col,
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'high_mean': high_group.mean(),
                'low_mean': low_group.mean(),
                'difference': high_group.mean() - low_group.mean()
            })
    except Exception as e:
        print(f"Error in t-test for {col}: {e}")

ttest_df = pd.DataFrame(ttest_results)
if not ttest_df.empty:
    print("T-test results (High vs Low highway counties):")
    print(ttest_df.sort_values('p_value').to_string())
    print()

    # Save t-test results
    ttest_df.to_csv(os.path.join(output_dir, 'california_ttest_results.csv'), index=False)
    print(f"Saved t-test results to: {os.path.join(output_dir, 'california_ttest_results.csv')}")
else:
    print("No t-test results to save (no significant comparisons)")
print()

# Regression analysis
print("=== Regression Analysis ===")
# Select significant predictors from correlation
significant_vars = corr_df[corr_df['significant'] & (corr_df['pearson_p'] < 0.05)]['variable'].tolist()
print(f"Significant predictors: {significant_vars}")

if len(significant_vars) > 0:
    # Prepare data for regression
    X = merged[significant_vars].copy()
    y = merged['highway_count'].copy()
    
    # Handle missing values
    X = X.dropna()
    y = y[X.index]
    
    # Add constant for intercept
    X = sm.add_constant(X)
    
    # Fit OLS model
    try:
        model = sm.OLS(y, X).fit()
        print("\nRegression Summary:")
        print(model.summary())
        
        # Save regression summary
        with open(os.path.join(output_dir, 'california_regression_summary.txt'), 'w') as f:
            f.write(str(model.summary()))
        print(f"\nSaved regression summary to: {os.path.join(output_dir, 'california_regression_summary.txt')}")
        
        # Create residual plot
        plt.figure(figsize=(10, 6))
        residuals = model.resid
        fitted = model.fittedvalues
        
        plt.scatter(fitted, residuals, alpha=0.6)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Fitted Values')
        plt.ylabel('Residuals')
        plt.title('California: Regression Residual Plot')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'california_residual_plot.png'), dpi=300, bbox_inches='tight')
        print(f"Saved residual plot to: {os.path.join(output_dir, 'california_residual_plot.png')}")
        plt.close()
        
    except Exception as e:
        print(f"Error in regression: {e}")
else:
    print("No significant predictors found for regression")
print()

# Create visualizations for significant correlations
print("=== Creating Visualizations for Significant Correlations ===")
significant_corrs = corr_df[corr_df['significant']].sort_values('pearson_r', key=abs, ascending=False)

for _, row in significant_corrs.head(10).iterrows():
    var = row['variable']
    r = row['pearson_r']
    p = row['pearson_p']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(merged[var], merged['highway_count'], alpha=0.6)
    
    # Add trend line
    z = np.polyfit(merged[var], merged['highway_count'], 1)
    p_poly = np.poly1d(z)
    plt.plot(merged[var], p_poly(merged[var]), "r--", alpha=0.8)
    
    plt.xlabel(var)
    plt.ylabel('Highway Count')
    plt.title(f'California: {var} vs Highway Count\nr = {r:.3f}, p = {p:.4f}, n = {len(merged)}')
    plt.tight_layout()
    
    # Create safe filename
    safe_var = var.replace(' ', '_').replace('/', '_')
    filename = f'california_{safe_var}_vs_highways.png'
    plt.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches='tight')
    print(f"Saved: {filename}")
    plt.close()

print()
print("=== Analysis Complete ===")
print(f"Results saved to: {output_dir}")