# StateAnalysis

A data analysis project exploring patterns between demographic data and memorial highway counts across US states.

## Project Overview

This project analyzes the relationship between county-level demographic characteristics and the number of memorial highways in Florida and Texas. The analysis uses statistical methods to identify significant patterns and correlations.

## Analysis Results

### Michigan Analysis (83 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - Pct_TwoOrMore (multi-racial): r = +0.605 (strong positive)
  - Pct_SomeOther_Alone: r = -0.470 (moderate negative)
  - Median_Age: r = -0.351 (moderate negative)

- **Significant Demographic Differences:**
  - High-highway counties are younger
  - High-highway counties have more multi-racial residents
  - High-highway counties have fewer residents identifying as "some other race"

- **Regression Model (R² = 0.418):**
  - Strongest predictor: Percentage of multi-racial residents
  - Model explains 41.8% of variance in highway counts

- **Top Counties by Highway Count:**
  1. Genesee County: 9 highways
  2. Macomb County: 9 highways
  3. Wayne County: 8 highways
  4. Jackson County: 8 highways
  5. Monroe County: 7 highways

### Florida Analysis (64 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - **Percentage of Registered Republicans**: r = -0.413 (moderate negative)
    - Counties with higher Republican percentages have FEWER highways
  - **Percentage of Registered NPA (No Party Affiliation)**: r = +0.419 (moderate positive)
    - Counties with more independent voters have MORE highways
  - **HS Graduation Rate**: r = +0.416 (moderate positive)
  - **Percentage Asian**: r = +0.382 (moderate positive)

- **Significant Demographic Differences:**
  - High-highway counties have significantly higher education levels
  - High-highway counties have more Asian residents
  - High-highway counties are wealthier with lower poverty rates

- **Multiple Regression Model (R² = 0.229):**
  - **Percentage Republican**: Coefficient = -0.296 (p = 0.004)
    - Each additional percentage point of Republicans associated with 0.30 FEWER highways
  - **Percentage with Bachelor's degree**: Coefficient = 0.478 (p = 0.046)
    - Each additional percentage point with Bachelor's degree associated with 0.48 MORE highways

- **Key Insight**: The relationship between politics and highways depends on whether you look at **absolute counts** or **percentages**:
  - Absolute counts: More Republicans = More highways (positive correlation)
  - Percentages: Higher Republican percentage = Fewer highways (negative correlation)
  - This suggests **political diversity** (not just Republican dominance) is associated with more highways

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

## Highway Attributes Analysis (Florida)

### Key Findings: Highway Attributes vs Demographics

**Strongest Correlations:**
- **Military highways** vs HS Graduation Rate: r = +0.416 (p = 0.0007)
- **Military highways** vs Bachelor's Degree Rate: r = +0.367 (p = 0.0020)
- **Politics highways** vs HS Graduation Rate: r = +0.365 (p = 0.0023)
- **Sports highways** vs HS Graduation Rate: r = +0.356 (p = 0.0029)
- **Music highways** vs Asian Percentage: r = +0.330 (p = 0.0065)

**Key Insights:**
1. **Education is the key driver**: All attribute types show positive correlations with education levels
2. **Asian population pattern**: Consistent positive correlation across all attribute types
3. **Military highways show strongest demographic links**: Most correlated with education, income, and wealth
4. **Sports highways and younger populations**: Negative correlation with median age

## Limitations

- Sample size: Only 3 states analyzed (Florida, Texas, Michigan)
- Data quality: Some missing values in demographic data
- Causality: Correlation does not imply causation
- Highway definition: Memorial highways may vary in significance
- Michigan highway data extracted from descriptions; some highways may span multiple counties
- Highway attributes extracted from descriptions; some misclassifications may exist

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
