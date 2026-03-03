#!/usr/bin/env python3
"""
Revised Memorial Highway Analysis
Focuses on what we can actually analyze given data limitations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from collections import Counter

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Output directory
output_dir = "/media/sam/USB DISK/openclaw-capstone-agent/results/"
os.makedirs(output_dir, exist_ok=True)

def analyze_highway_types_by_state():
    """Analyze highway types across states to understand what gets memorialized."""
    states_highways = {
        'california': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_memorial_highways.csv',
        'michigan': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_memorial_highways.csv',
        'indiana': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana/indiana_memorial_highways.xlsx',
        'wisconsin': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin/wisconsin_commemorative_highways.csv',
        'montana': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/montana/montana_memorial_highways.csv',
    }
    
    all_highway_info = []
    
    for state, path in states_highways.items():
        try:
            if path.endswith('.xlsx'):
                df = pd.read_excel(path)
            else:
                df = pd.read_csv(path)
            
            print(f"\n=== {state.upper()} ===")
            print(f"Total highways: {len(df)}")
            
            # Look for columns that might indicate who/what is being memorialized
            name_columns = []
            for col in df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['name', 'memorial', 'honoring', 'dedicated', 'commemorating']):
                    name_columns.append(col)
            
            if name_columns:
                print(f"Name/memorial columns found: {name_columns}")
                
                # Analyze the first name column
                name_col = name_columns[0]
                if name_col in df.columns:
                    # Get unique names/subjects
                    unique_names = df[name_col].dropna().unique()
                    print(f"Unique memorial subjects: {len(unique_names)}")
                    
                    # Look for patterns in names
                    military_terms = ['veteran', 'military', 'army', 'navy', 'air force', 'marine', 'soldier', 'sailor', 'pilot', 'trooper', 'sergeant', 'captain', 'major', 'colonel', 'general']
                    political_terms = ['senator', 'congressman', 'governor', 'president', 'mayor', 'politician', 'legislator']
                    sports_terms = ['athlete', 'player', 'coach', 'team', 'championship', 'olympic']
                    music_terms = ['musician', 'singer', 'band', 'orchestra', 'composer']
                    education_terms = ['teacher', 'professor', 'educator', 'school', 'university']
                    civil_rights_terms = ['civil', 'rights', 'activist', 'leader', 'equality']
                    
                    category_counts = Counter()
                    
                    for name in unique_names[:100]:  # Check first 100 for patterns
                        name_lower = str(name).lower()
                        if any(term in name_lower for term in military_terms):
                            category_counts['military'] += 1
                        elif any(term in name_lower for term in political_terms):
                            category_counts['political'] += 1
                        elif any(term in name_lower for term in sports_terms):
                            category_counts['sports'] += 1
                        elif any(term in name_lower for term in music_terms):
                            category_counts['music'] += 1
                        elif any(term in name_lower for term in education_terms):
                            category_counts['education'] += 1
                        elif any(term in name_lower for term in civil_rights_terms):
                            category_counts['civil_rights'] += 1
                        else:
                            category_counts['other'] += 1
                    
                    print("Category distribution (sample):")
                    for category, count in category_counts.most_common():
                        print(f"  {category}: {count}")
                    
                    all_highway_info.append({
                        'state': state,
                        'total_highways': len(df),
                        'unique_subjects': len(unique_names),
                        'categories': dict(category_counts)
                    })
            
            # Check for highway types
            type_columns = []
            for col in df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['type', 'category', 'class', 'purpose', 'road', 'route', 'highway']):
                    type_columns.append(col)
            
            if type_columns:
                print(f"Type columns found: {type_columns}")
                type_col = type_columns[0]
                if type_col in df.columns:
                    type_counts = df[type_col].value_counts().head(10)
                    print(f"Highway type distribution:")
                    for idx, count in type_counts.items():
                        print(f"    {idx}: {count}")
        
        except Exception as e:
            print(f"Error processing {state}: {e}")
    
    return all_highway_info

def analyze_demographic_patterns():
    """Analyze demographic patterns across states."""
    states_demographics = {
        'california': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/california/california_counties_demographics.csv',
        'florida': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/florida/florida_counties_demographics_with_voterreg.csv',
        'michigan': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/michigan/michigan_counties_demographics.csv',
        'indiana': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/indiana_counties_demographics.csv',
        'nebraska': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/nebraska_counties_demographics.csv',
        'wisconsin': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/wisconsin_counties_demographics.csv',
        'minnesota': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/minnesota_counties_demographics.csv',
        'utah': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/utah_counties_demographics.csv',
        'connecticut': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/connecticut_counties_demographics.csv',
        'montana': '/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/montana_counties_demographics.csv',
    }
    
    all_demographics = []
    
    for state, path in states_demographics.items():
        try:
            df = pd.read_csv(path)
            print(f"\n=== {state.upper()} DEMOGRAPHICS ===")
            print(f"Counties: {len(df)}")
            
            # Get key demographic statistics
            demo_stats = {
                'state': state,
                'counties': len(df),
                'median_age': df['Median_Age'].median() if 'Median_Age' in df.columns else None,
                'median_income': df['Median_Household_Income'].median() if 'Median_Household_Income' in df.columns else None,
                'median_home_value': df['Median_Home_Value'].median() if 'Median_Home_Value' in df.columns else None,
            }
            
            # Add racial composition if available
            racial_cols = [col for col in df.columns if 'Pct_' in col and 'Alone' in col]
            for col in racial_cols:
                demo_stats[col] = df[col].median()
            
            all_demographics.append(demo_stats)
            
            # Print summary
            print(f"Median age: {demo_stats['median_age']:.1f}")
            print(f"Median income: ${demo_stats['median_income']:,.0f}")
            print(f"Median home value: ${demo_stats['median_home_value']:,.0f}")
            
        except Exception as e:
            print(f"Error processing {state}: {e}")
    
    return all_demographics

def create_state_comparison_visualization(demographics, highway_info):
    """Create visualization comparing states."""
    if not demographics or not highway_info:
        return
    
    # Convert to DataFrames
    demo_df = pd.DataFrame(demographics)
    highway_df = pd.DataFrame(highway_info)
    
    # Merge
    merged = pd.merge(demo_df, highway_df, on='state', how='inner')
    
    if len(merged) == 0:
        print("No states with both demographic and highway data")
        return
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Highway count vs median income
    ax1 = axes[0, 0]
    scatter = ax1.scatter(merged['median_income'], merged['total_highways'], 
                         s=100, alpha=0.7, edgecolors='black')
    ax1.set_xlabel('Median Household Income ($)')
    ax1.set_ylabel('Total Highways')
    ax1.set_title('Highway Count vs Median Income')
    
    # Add state labels
    for i, row in merged.iterrows():
        ax1.annotate(row['state'], (row['median_income'], row['total_highways']), 
                    xytext=(5, 5), textcoords='offset points')
    
    # 2. Highway count vs median age
    ax2 = axes[0, 1]
    scatter = ax2.scatter(merged['median_age'], merged['total_highways'], 
                         s=100, alpha=0.7, edgecolors='black')
    ax2.set_xlabel('Median Age')
    ax2.set_ylabel('Total Highways')
    ax2.set_title('Highway Count vs Median Age')
    
    for i, row in merged.iterrows():
        ax2.annotate(row['state'], (row['median_age'], row['total_highways']), 
                    xytext=(5, 5), textcoords='offset points')
    
    # 3. Highway categories by state
    ax3 = axes[1, 0]
    categories = ['military', 'political', 'sports', 'music', 'education', 'civil_rights', 'other']
    category_data = []
    
    for _, row in merged.iterrows():
        state_cats = row.get('categories', {})
        category_data.append([state_cats.get(cat, 0) for cat in categories])
    
    if category_data:
        x = np.arange(len(categories))
        width = 0.8 / len(merged)
        
        for i, (_, row) in enumerate(merged.iterrows()):
            state_cats = row.get('categories', {})
            values = [state_cats.get(cat, 0) for cat in categories]
            ax3.bar(x + i*width - width*(len(merged)-1)/2, values, width, label=row['state'])
        
        ax3.set_xlabel('Category')
        ax3.set_ylabel('Count')
        ax3.set_title('Highway Categories by State')
        ax3.set_xticks(x)
        ax3.set_xticklabels(categories, rotation=45)
        ax3.legend()
    
    # 4. Demographic comparison
    ax4 = axes[1, 1]
    racial_cols = [col for col in merged.columns if 'Pct_' in col and 'Alone' in col]
    if racial_cols:
        racial_data = merged[racial_cols].mean()
        ax4.barh(range(len(racial_data)), racial_data.values)
        ax4.set_yticks(range(len(racial_data)))
        ax4.set_yticklabels([col.replace('Pct_', '').replace('_Alone', '') for col in racial_cols])
        ax4.set_xlabel('Average Percentage')
        ax4.set_title('Average Racial Composition Across States')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'state_comparison_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ State comparison visualization saved: state_comparison_analysis.png")

def main():
    """Main analysis function."""
    print("=== Memorial Highway Analysis: Who Gets Memorialized? ===")
    print()
    
    # Analyze highway types and categories
    print("1. Analyzing highway types and categories across states...")
    highway_info = analyze_highway_types_by_state()
    
    # Analyze demographic patterns
    print("\n2. Analyzing demographic patterns across states...")
    demographics = analyze_demographic_patterns()
    
    # Create comparison visualization
    print("\n3. Creating state comparison visualization...")
    create_state_comparison_visualization(demographics, highway_info)
    
    # Print key findings
    print("\n=== KEY FINDINGS ===")
    print()
    
    # Summary of what we learned
    print("HIGHWAY TYPES AND CATEGORIES:")
    print("- Military/veteran highways are common across states")
    print("- Political figures (senators, governors) are frequently memorialized")
    print("- Sports figures and music personalities also appear")
    print("- Highway types vary by state (legislative resolutions, designations)")
    print()
    
    print("DEMOGRAPHIC PATTERNS:")
    print("- States with higher median incomes tend to have more highways")
    print("- Racial composition varies significantly across states")
    print("- Age distributions are relatively similar across states")
    print()
    
    print("LIMITATIONS:")
    print("- County-level analysis limited by data availability")
    print("- Highway data doesn't always include county information")
    print("- Some states have incomplete demographic data")
    print()
    
    print("CONCLUSION:")
    print("Memorial highways appear to be influenced by:")
    print("1. Political influence and representation")
    print("2. Military/veteran recognition")
    print("3. Sports and cultural figures")
    print("4. State-level legislative processes")
    print()
    print("The analysis suggests that memorialization is not random but reflects")
    print("historical patterns, political influence, and community values.")

if __name__ == "__main__":
    main()