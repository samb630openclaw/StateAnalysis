#!/usr/bin/env python3
"""
Script to push analysis results to GitHub.
"""

import os
import subprocess

# Change to the openclaw-capstone-agent directory
os.chdir("/media/sam/USB DISK/openclaw-capstone-agent")

print("=== Pushing Analysis Results to GitHub ===")

# Add all new files
print("\n1. Adding new files to git...")
result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
if result.returncode == 0:
    print("   ✓ Files added successfully")
else:
    print(f"   ✗ Error adding files: {result.stderr}")

# Commit changes
print("\n2. Committing changes...")
commit_message = "Add new county-level analysis for Indiana and Florida, update README with key findings about who gets memorialized"
result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
if result.returncode == 0:
    print("   ✓ Changes committed successfully")
else:
    print(f"   ✗ Error committing changes: {result.stderr}")

# Push to GitHub
print("\n3. Pushing to GitHub...")
result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if result.returncode == 0:
    print("   ✓ Pushed to GitHub successfully")
else:
    print(f"   ✗ Error pushing to GitHub: {result.stderr}")

print("\n=== Summary ===")
print("Analysis results have been updated with:")
print("- County-level analysis for Indiana and Florida")
print("- New visualizations showing strong correlations")
print("- Updated README answering 'Why do some people get memorialized?'")
print("- Key finding: Memorialization is primarily a political process, not merit-based")