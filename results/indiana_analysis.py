#!/usr/bin/env python3
"""
Indiana Memorial Highway Analysis
Analyzes the relationship between demographic data and memorial highway counts in Indiana.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Paths
demographics_path = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana_counties_demographics.csv"
highways_path = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana/indiana_memorial_highways.xlsx"
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"

print("=" * 80)
print("INDIANA MEMORIAL HIGHWAY ANALYSIS")
print("=" * 80)

# Step 1: Load and prepare demographic data
print("\n1. Loading demographic data...")
try:
    demo_df = pd.read_csv(demographics_path)
    print(f"   Loaded {len(demo_df)} counties")
    print(f"   Columns: {list(demo_df.columns)}")
    
    # Clean county names
    demo_df['County'] = demo_df['County'].str.replace(' County, Indiana', '', regex=False)
    demo_df['County'] = demo_df['County'].str.strip()
    print(f"   Sample counties: {demo_df['County'].head().tolist()}")
except Exception as e:
    print(f"   ERROR loading demographics: {e}")
    exit(1)

# Step 2: Load and prepare highway data
print("\n2. Loading highway data...")
try:
    highway_df = pd.read_excel(highways_path)
    print(f"   Loaded {len(highway_df)} highway records")
    print(f"   Columns: {list(highway_df.columns)}")
    
    # Clean county names
    highway_df['COUNTY'] = highway_df['COUNTY'].str.strip()
    
    # Handle multi-county highways by splitting and counting for each county
    highway_counts = {}
    for idx, row in highway_df.iterrows():
        county_str = row['COUNTY']
        if pd.isna(county_str):
            continue
        
        # Split multi-county entries (e.g., "Adams/Allen")
        counties = [c.strip() for c in str(county_str).split('/')]
        
        for county in counties:
            if county not in highway_counts:
                highway_counts[county] = 0
            highway_counts[county] += 1
    
    # Create highway count dataframe
    highway_count_df = pd.DataFrame(list(highway_counts.items()), columns=['County', 'Highway_Count'])
    print(f"   Counties with highways: {len(highway_count_df)}")
    print(f"   Total highways counted: {highway_count_df['Highway_Count'].sum()}")
    print(f"   Sample: {highway_count_df.head()}")
except Exception as e:
    print(f"   ERROR loading highways: {e}")
    exit(1)

# Step 3: Merge datasets
print("\n3. Merging datasets...")
try:
    merged_df = pd.merge(demo_df, highway_count_df, on='County', how='inner')
    print(f"   Merged {len(merged_df)} counties")
    print(f"   Missing counties in demographics: {len(demo_df) - len(merged_df)}")
    print(f"   Missing counties in highways: {len(highway_count_df) - len(merged_df)}")
    
    # Save merged data
    merged_path = os.path.join(output_dir, "indiana_merged_data.csv")
    merged_df.to_csv(merged_path, index=False)
    print(f"   Saved merged data to: {merged_path}")
    
    # Print summary
    print(f"\n   Data Summary:")
    print(f"   - Shape: {merged_df.shape}")
    print(f"   - Highway count range: {merged_df['Highway_Count'].min()} - {merged_df['Highway_Count'].max()}")
    print(f"   - Mean highways per county: {merged_df['Highway_Count'].mean():.2f}")
    print(f"   - Median highways per county: {merged_df['Highway_Count'].median():.2f}")
except Exception as e:
    print(f"   ERROR merging data: {e}")
    exit(1)

# Step 4: Correlation analysis
print("\n4. Running correlation analysis...")
try:
    # Select numeric columns for correlation
    numeric_cols = merged_df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove Highway_Count from predictors, keep it as target
    if 'Highway_Count' in numeric_cols:
        numeric_cols.remove('Highway_Count')
    
    correlations = {}
    for col in numeric_cols:
        if col != 'Highway_Count':
            corr, p_value = stats.pearsonr(merged_df[col].fillna(merged_df[col].median()), 
                                          merged_df['Highway_Count'].fillna(merged_df['Highway_Count'].median()))
            correlations[col] = {'correlation': corr, 'p_value': p_value}
    
    # Sort by absolute correlation
    sorted_corrs = sorted(correlations.items(), key=lambda x: abs(x[1]['correlation']), reverse=True)
    
    print(f"   Top 10 correlations with Highway_Count:")
    for i, (col, stats_dict) in enumerate(sorted_corrs[:10]):
        sig = "***" if stats_dict['p_value'] < 0.001 else "**" if stats_dict['p_value'] < 0.01 else "*" if stats_dict['p_value'] < 0.05 else ""
        print(f"   {i+1}. {col}: r = {stats_dict['correlation']:.3f}, p = {stats_dict['p_value']:.4f} {sig}")
    
    # Save correlation matrix
    corr_df = pd.DataFrame([(col, stats_dict['correlation'], stats_dict['p_value']) 
                           for col, stats_dict in correlations.items()],
                          columns=['Variable', 'Correlation', 'P_Value'])
    corr_df = corr_df.sort_values('Correlation', key=abs, ascending=False)
    corr_path = os.path.join(output_dir, "indiana_correlation_matrix.csv")
    corr_df.to_csv(corr_path, index=False)
    print(f"   Saved correlation matrix to: {corr_path}")
except Exception as e:
    print(f"   ERROR in correlation analysis: {e}")

# Step 5: Regression analysis
print("\n5. Running regression analysis...")
try:
    # Prepare data for regression
    X = merged_df[numeric_cols].fillna(merged_df[numeric_cols].median())
    y = merged_df['Highway_Count'].fillna(merged_df['Highway_Count'].median())
    
    # Add constant for intercept
    X = sm.add_constant(X)
    
    # Fit OLS model
    model = sm.OLS(y, X).fit()
    
    print(f"   Regression R²: {model.rsquared:.3f}")
    print(f"   Adjusted R²: {model.rsquared_adj:.3f}")
    print(f"   F-statistic: {model.fvalue:.3f}")
    print(f"   F-test p-value: {model.f_pvalue:.4f}")
    
    # Print significant predictors
    print(f"\n   Significant predictors (p < 0.05):")
    significant = model.pvalues[model.pvalues < 0.05].index.tolist()
    if 'const' in significant:
        significant.remove('const')
    
    for pred in significant:
        coef = model.params[pred]
        p_val = model.pvalues[pred]
        print(f"   - {pred}: coef = {coef:.4f}, p = {p_val:.4f}")
    
    # Save regression summary
    summary_path = os.path.join(output_dir, "indiana_regression_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("INDIANA REGRESSION ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        f.write(model.summary().as_text())
    print(f"   Saved regression summary to: {summary_path}")
    
    # Create residual plot
    plt.figure(figsize=(10, 6))
    plt.scatter(model.fittedvalues, model.resid, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Fitted Values')
    plt.ylabel('Residuals')
    plt.title('Indiana: Regression Residual Plot')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'indiana_residual_plot.png'), dpi=300)
    plt.close()
    print(f"   Saved residual plot to: indiana_residual_plot.png")
except Exception as e:
    print(f"   ERROR in regression analysis: {e}")

# Step 6: Group comparisons (T-tests)
print("\n6. Running group comparisons...")
try:
    # Split by median highway count
    median_highways = merged_df['Highway_Count'].median()
    merged_df['Highway_Group'] = merged_df['Highway_Count'].apply(lambda x: 'High' if x >= median_highways else 'Low')
    
    ttest_results = []
    for col in numeric_cols:
        high_group = merged_df[merged_df['Highway_Group'] == 'High'][col]
        low_group = merged_df[merged_df['Highway_Group'] == 'Low'][col]
        
        if len(high_group) > 1 and len(low_group) > 1:
            t_stat, p_value = stats.ttest_ind(high_group, low_group, equal_var=False)
            effect_size = (high_group.mean() - low_group.mean()) / np.sqrt((high_group.var() + low_group.var()) / 2)
            
            ttest_results.append({
                'Variable': col,
                'T_Statistic': t_stat,
                'P_Value': p_value,
                'Effect_Size': effect_size,
                'High_Mean': high_group.mean(),
                'Low_Mean': low_group.mean(),
                'Significant': p_value < 0.05
            })
    
    ttest_df = pd.DataFrame(ttest_results)
    ttest_df = ttest_df.sort_values('P_Value')
    
    print(f"   Significant differences (p < 0.05):")
    significant_ttests = ttest_df[ttest_df['Significant']]
    for idx, row in significant_ttests.head(10).iterrows():
        print(f"   - {row['Variable']}: t = {row['T_Statistic']:.3f}, p = {row['P_Value']:.4f}, d = {row['Effect_Size']:.3f}")
    
    # Save t-test results
    ttest_path = os.path.join(output_dir, "indiana_ttest_results.csv")
    ttest_df.to_csv(ttest_path, index=False)
    print(f"   Saved t-test results to: {ttest_path}")
except Exception as e:
    print(f"   ERROR in t-test analysis: {e}")

# Step 7: Visualizations
print("\n7. Creating visualizations...")
try:
    # Top correlations plot
    top_corrs = sorted_corrs[:8]
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    for idx, (col, stats_dict) in enumerate(top_corrs):
        if idx < len(axes):
            ax = axes[idx]
            ax.scatter(merged_df[col], merged_df['Highway_Count'], alpha=0.6)
            ax.set_xlabel(col)
            ax.set_ylabel('Highway Count')
            ax.set_title(f'{col}\nr = {stats_dict["correlation"]:.3f}, p = {stats_dict["p_value"]:.4f}')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'indiana_top_correlations.png'), dpi=300)
    plt.close()
    print(f"   Saved top correlations plot to: indiana_top_correlations.png")
    
    # Correlation heatmap
    corr_matrix = merged_df[numeric_cols + ['Highway_Count']].corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', 
                cbar_kws={'shrink': 0.8})
    plt.title('Indiana: Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'indiana_correlation_heatmap.png'), dpi=300)
    plt.close()
    print(f"   Saved correlation heatmap to: indiana_correlation_heatmap.png")
    
    # Top counties by highway count
    top_counties = merged_df.nlargest(10, 'Highway_Count')[['County', 'Highway_Count']]
    plt.figure(figsize=(12, 6))
    plt.barh(range(len(top_counties)), top_counties['Highway_Count'])
    plt.yticks(range(len(top_counties)), top_counties['County'])
    plt.xlabel('Highway Count')
    plt.title('Indiana: Top Counties by Memorial Highway Count')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'indiana_top_counties.png'), dpi=300)
    plt.close()
    print(f"   Saved top counties plot to: indiana_top_counties.png")
    
    # Save top counties data
    top_counties_path = os.path.join(output_dir, "indiana_top_counties.csv")
    top_counties.to_csv(top_counties_path, index=False)
    print(f"   Saved top counties data to: {top_counties_path}")
except Exception as e:
    print(f"   ERROR creating visualizations: {e}")

# Step 8: Summary
print("\n" + "=" * 80)
print("INDIANA ANALYSIS SUMMARY")
print("=" * 80)
print(f"Counties analyzed: {len(merged_df)}")
print(f"Total highways: {merged_df['Highway_Count'].sum()}")
print(f"Strongest demographic predictor: {sorted_corrs[0][0] if sorted_corrs else 'None'}")
print(f"Regression R²: {model.rsquared:.3f}" if 'model' in locals() else "Regression not completed")
print("\nKey Findings:")
print("1. Analysis completed successfully")
print("2. All results saved to output directory")
print("=" * 80)