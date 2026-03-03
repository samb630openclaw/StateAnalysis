#!/usr/bin/env python3
"""
Utah Analysis: Memorial Highways vs Demographics
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
demographics_path = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/utah_counties_demographics.csv"
highways_path = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/utah/utah_memorial_highways.csv"
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"

print("=== Utah Analysis: Memorial Highways vs Demographics ===")
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
print("Sample highway names:")
for i, name in enumerate(highways['Name'].head(10)):
    print(f"{i}: {name}")
print()

# Check if there are other columns that might have county info
print("All highway columns:", list(highways.columns))
print()

# For now, let's analyze the highways themselves
print("=== Highway Analysis ===")
print(f"Total highways: {len(highways)}")
print(f"Highway types: {highways['Name'].value_counts().head(10)}")
print()

# Clean county names in demographics
print("=== Cleaning County Names ===")
if county_cols:
    county_col = county_cols[0]
    print(f"Using county column: {county_col}")
    print(f"Sample county names: {demographics[county_col].head(10).tolist()}")
    
    # Clean county names
    demographics['county_clean'] = demographics[county_col].str.replace(r', Utah', '', regex=True)
    demographics['county_clean'] = demographics['county_clean'].str.strip()
    print(f"Sample cleaned county names: {demographics['county_clean'].head(10).tolist()}")
else:
    print("No county column found!")
    exit()

# Since we can't map highways to counties, let's analyze the highways themselves
print("=== Highway Analysis ===")
print(f"Total highways: {len(highways)}")
print(f"Highway types: {highways['Name'].value_counts().head(10)}")
print()

# For now, let's save the demographics data and note the limitation
demographics.to_csv(os.path.join(output_dir, 'utah_demographics_cleaned.csv'), index=False)
print(f"Saved cleaned demographics to: {os.path.join(output_dir, 'utah_demographics_cleaned.csv')}")
print()

print("=== Analysis Complete ===")
print("Note: Utah analysis limited due to lack of county-level highway data.")
print(f"Results saved to: {output_dir}")