# StateAnalysis

A data analysis project exploring patterns between demographic data and memorial highway counts across US states.

## Project Overview

This project analyzes the relationship between county-level demographic characteristics and the number of memorial highways in Florida and Texas. The analysis uses statistical methods to identify significant patterns and correlations.

## Analysis Results

### Florida Analysis (64 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - Registered Republicans: r = +0.729 (strong positive)
  - Registered Total: r = +0.727 (strong positive)
  - Registered Democrats: r = +0.719 (strong positive)
  - HS Graduation Rate: r = +0.416 (moderate positive)

- **Significant Demographic Differences:**
  - High-highway counties have significantly higher education levels
  - High-highway counties have more registered voters (both parties)
  - High-highway counties are wealthier with lower poverty rates
  - High-highway counties have fewer Hispanic residents

- **Regression Model (R² = 0.539):**
  - Strongest predictor: Number of registered Republicans
  - Model explains 53.9% of variance in highway counts

- **Top Counties by Highway Count:**
  1. Miami-Dade: 53 highways
  2. Broward: 42 highways
  3. Hillsborough: 35 highways
  4. Palm Beach: 26 highways
  5. Brevard: 26 highways

### Texas Analysis (254 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - Median Household Income: r = -0.201 (negative)
  - HS Graduation Rate: r = +0.183 (positive)
  - Asian Percentage: r = +0.182 (positive)

- **Significant Demographic Differences:**
  - High-highway counties have higher HS graduation rates
  - High-highway counties have more Black population
  - High-highway counties are younger

- **Regression Model (R² = 0.173):**
  - Strongest predictors: HS Graduation Rate, Median Household Income
  - Model explains 17.3% of variance in highway counts

- **Top Counties by Highway Count:**
  1. Hudspeth County: 20 highways
  2. Webb County: 18 highways
  3. Gillespie County: 18 highways
  4. Harris County: 17 highways
  5. Tom Green County: 15 highways

## Data Sources

- **Florida:** County demographics with voter registration data, memorial highway designations
- **Texas:** County demographics, memorial highway designations

## Analysis Methods

- Correlation analysis (Pearson and Spearman)
- T-tests for group comparisons
- OLS regression modeling
- Distribution analysis

## Results

All analysis results, visualizations, and reports are saved in the `results/` directory.

## Limitations

- Sample size: Only 2 states analyzed
- Data quality: Some missing values in demographic data
- Causality: Correlation does not imply causation
- Highway definition: Memorial highways may vary in significance

## Project Structure

```
StateAnalysis/
├── Capstone/                    # Submodule with raw data
│   └── Capstone-states/
├── results/                     # Analysis results and visualizations
└── README.md                    # This file
```

---

*Analysis completed: 2026-03-03*
*Output directory: /media/sam/USB DISK/openclaw-capstone-agent/results/*
