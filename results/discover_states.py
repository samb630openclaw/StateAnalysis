#!/usr/bin/env python3
"""
Discover states with both demographic and highway data for comprehensive analysis.
"""

import os
import pandas as pd
from pathlib import Path

# Base directory for Capstone data
base_dir = "/media/sam/USB DISK/openclaw-capstone-agent/Capstone/Capstone-states/states/"

# States to check
states = [
    'california', 'florida', 'michigan', 'indiana', 'nebraska', 
    'texas', 'wisconsin', 'minnesota', 'utah', 'connecticut',
    'hawaii', 'montana', 'north_carolina', 'oklahoma'
]

def check_state_data(state):
    """Check if a state has both demographic and highway data."""
    state_dir = os.path.join(base_dir, state)
    demographic_files = []
    highway_files = []
    
    # Check state directory
    if os.path.exists(state_dir):
        files = os.listdir(state_dir)
        for file in files:
            if 'demographic' in file.lower() or 'counties' in file.lower():
                demographic_files.append(file)
            elif 'highway' in file.lower() or 'memorial' in file.lower() or 'commemorative' in file.lower():
                highway_files.append(file)
    
    # Check parent directory for demographic files
    parent_files = os.listdir(base_dir)
    for file in parent_files:
        if file.startswith(f"{state}_") and 'demographic' in file.lower():
            demographic_files.append(file)
    
    return {
        'state': state,
        'demographic_files': demographic_files,
        'highway_files': highway_files,
        'has_both': len(demographic_files) > 0 and len(highway_files) > 0
    }

# Check all states
results = []
for state in states:
    result = check_state_data(state)
    if result:
        results.append(result)

# Print summary
print("=== States with Both Demographic and Highway Data ===")
for r in results:
    if r['has_both']:
        print(f"✓ {r['state'].title()}")
        print(f"  Demographic files: {r['demographic_files']}")
        print(f"  Highway files: {r['highway_files']}")
        print()

print("\n=== States with Only One Type of Data ===")
for r in results:
    if not r['has_both']:
        print(f"✗ {r['state'].title()}")
        if r['demographic_files']:
            print(f"  Demographic files: {r['demographic_files']}")
        if r['highway_files']:
            print(f"  Highway files: {r['highway_files']}")
        print()

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('/media/sam/USB DISK/openclaw-capstone-agent/results/state_data_discovery.csv', index=False)
print(f"Results saved to state_data_discovery.csv")