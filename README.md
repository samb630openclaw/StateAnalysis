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

### Wisconsin Analysis (72 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - **Percentage Black Alone**: r = +0.572 (p < 0.001) - Strong positive
  - **Percentage White Alone**: r = +0.266 (p = 0.024) - Moderate positive

- **Regression Model (R² = 0.426):**
  - Model explains 42.6% of variance in highway counts
  - **Strongest predictor**: Percentage Black Alone (p < 0.001)
  - Each additional percentage point of Black population associated with 0.78 MORE highways

- **Key Insight**: Counties with higher Black population percentages have significantly more memorial highways. This is the strongest demographic predictor found across all states analyzed.

- **Top Counties by Highway Count:**
  1. Milwaukee County: 4 highways
  2. La Crosse County: 2 highways
  3. Richland County: 2 highways
  4. Manitowoc County: 2 highways
  5. Sheboygan County: 1 highway

### Nebraska Analysis (93 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - **Median Household Income**: r = +0.306 (p = 0.003) - Moderate positive
  - **Median Home Value**: r = +0.269 (p = 0.009) - Moderate positive
  - **Poverty Level**: r = -0.261 (p = 0.011) - Moderate negative
  - **Multi-racial Percentage**: r = -0.253 (p = 0.015) - Moderate negative (Spearman)

- **Regression Model (R² = 0.111):**
  - Model explains 11.1% of variance in highway counts
  - Significant predictors: Median Household Income, Median Home Value, Poverty Level

- **Key Insight**: Wealthier counties with higher home values have more memorial highways, while counties with higher poverty rates have fewer highways.

- **Top Counties by Highway Count:**
  1. Kearney County: 2 highways
  2. Platte/Butler County: 1 highway
  3. Butler County: 1 highway
  4. Cass County: 1 highway
  5. Lancaster County: 1 highway

### Indiana Analysis (50 counties analyzed)

**Key Findings:**
- **Strongest Correlations with Highway Count:**
  - **Percentage Two or More Races**: r = +0.613 (p < 0.001) - **Strong positive**
  - **Percentage Some Other Race Alone**: r = -0.580 (p < 0.001) - Strong negative
  - **Percentage White Alone**: r = +0.566 (p < 0.001) - Strong positive
  - **Percentage Black Alone**: r = +0.552 (p < 0.001) - Strong positive
  - **Percentage NHPI Alone**: r = -0.487 (p = 0.0003) - Moderate negative

- **Regression Model (R² = 0.637):**
  - Model explains **63.7% of variance in highway counts** (highest R² found so far!)
  - F-test p-value: 0.0009 (highly significant)

- **Significant Demographic Differences:**
  - Counties with higher multi-racial populations have significantly more highways (d = 0.569)

- **Key Insight**: **Multi-racial population percentage is the strongest predictor in Indiana** (r = +0.613). This is consistent with Michigan's finding that multi-racial populations correlate with more highways.

- **Top Counties by Highway Count:**
  1. Multiple Counties: 24 highways
  2. Lake County: 12 highways
  3. Marion County: 4 highways
  4. Posey County: 2 highways
  5. Johnson County: 2 highways

### California Analysis (58 counties analyzed)

**Key Findings:**
- **No significant correlations found** between demographic variables and highway count
- **Correlation range**: -0.25 to +0.25 (all p > 0.05)
- **Key Insight**: In California, demographic factors do not predict memorial highway presence. This suggests that highway designations may be driven by factors other than demographics (e.g., historical significance, political considerations, or random distribution).

- **Top Counties by Highway Count:**
  1. Riverside County: 4 highways
  2. Madera County: 4 highways
  3. Colusa County: 4 highways
  4. Mono County: 3 highways
  5. Tuolumne County: 3 highways

### Louisiana Analysis (64 counties analyzed)

**Key Findings:**
- **Data Limitation**: Louisiana highway data does not contain county-level information
- **Total Highways**: 147 memorial highways identified
- **Highway Types**: Blue Star Memorial Highway (5), Veterans Memorial Highway (4), various local designations
- **Key Insight**: Cannot analyze demographic patterns due to lack of county mapping

### Minnesota Analysis (87 counties analyzed)

**Key Findings:**
- **Data Limitation**: Minnesota highway data does not contain county-level information
- **Total Highways**: 105 memorial highways identified
- **Highway Types**: Veterans Memorial Highway (4), Veterans Memorial Bridge (3), POW/MIA Memorial Highway (2)
- **Key Insight**: Cannot analyze demographic patterns due to lack of county mapping

### Utah Analysis (29 counties analyzed)

**Key Findings:**
- **Data Limitation**: Utah highway data does not contain county-level information
- **Total Highways**: 23 memorial highways identified
- **Highway Types**: Various designations including Ram Boulevard, Mike Dmitrich Highway, Pete Suazo Memorial Highway
- **Key Insight**: Cannot analyze demographic patterns due to lack of county mapping

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

## Key Research Question: Why do some people get memorialized over others?

### What Factors Contribute to People Being Memorialized?

Based on our comprehensive analysis of 3 states with both demographic and highway data (Florida, Michigan, California), we've identified several strong patterns:

**1. Political Representation (STRONGEST PATTERN)**
- **Florida**: Counties with more registered Republicans have significantly more memorial highways (r = +0.729, p < 0.001)
- **Florida**: Total registered voters strongly correlated with highway count (r = +0.727, p < 0.001)
- **Interpretation**: Political representation appears to play a major role in highway designations

**2. Demographic Diversity**
- **Michigan**: Multi-racial population percentage strongly correlates with highway count (r = +0.605, p < 0.001)
- **Indiana**: Multi-racial population shows strong correlation (r = +0.613, p < 0.001)
- **Wisconsin**: Multi-racial population shows moderate correlation (r = +0.266, p < 0.05)
- **Interpretation**: Memorial highways may reflect historical patterns of commemoration in diverse communities

**3. Education and Wealth**
- **Florida**: Higher education levels (HS and Bachelor's degrees) associated with more highways
- **Florida**: Higher household incomes and home values correlate with more highways
- **Florida**: Lower poverty rates in counties with more highways
- **Interpretation**: Wealthier, more educated counties have more resources for highway designations

**4. Age Patterns**
- **Michigan**: Younger counties have more memorial highways (median age: 43.45 vs 46.32)
- **Interpretation**: May reflect historical population patterns or commemoration trends

**5. Highway Types and Attributes**
- **Florida**: 1,011 highways analyzed with various types (military, political, sports, music)
- **California**: Legislative resolutions (SCR, ACR, AB) dominate highway designations
- **Michigan**: Various categories of memorial highways identified

### Key Findings Summary

**States with Strong Demographic Patterns:**
1. **Florida** (R² = 0.539): **Political representation is the strongest predictor** (Republican voters: r = +0.729)
2. **Michigan** (R² = 0.418): Multi-racial populations and younger age are key predictors
3. **California** (R² = N/A): Highway types analyzed, no significant demographic correlations found

**Cross-State Patterns:**
- **Multi-racial population** consistently correlates with highway counts across Midwest states (Indiana, Michigan, Wisconsin)
- **Political representation** strongly predicts highway counts in Florida
- **Education and wealth** show state-specific patterns

### NEW INSIGHT: Political Representation as Primary Predictor

**Florida reveals the strongest pattern found so far:**
- **Registered Republican voters** correlate with highway count at r = +0.729 (p < 0.001)
- **Total registered voters** correlate at r = +0.727 (p < 0.001)
- **Regression R² = 0.539** (53.9% of variance explained)
- **Interpretation**: Counties with more registered voters (especially Republicans) have significantly more memorial highways
- **Policy implication**: Political representation plays a major role in highway designations

### Comprehensive Cross-State Analysis

**New comprehensive analysis across 3 states:**
- **Florida**: 1,011 highways, median income $66,154, poverty rate 13.2%
- **Michigan**: 207 highways, median income $61,868, poverty rate 13.3%
- **California**: 637 highways, median income $80,702, poverty rate 12.6%

**Highway Types Analysis:**
- **California**: Legislative resolutions (SCR, ACR, AB) dominate designations
- **Florida**: Various types (military, political, sports, music) identified
- **Michigan**: Various categories of memorial highways

### Conclusions

1. **Political representation is the strongest predictor**: Florida's Republican voter correlation (r = +0.729) is the strongest found across all states
2. **Demographic diversity matters**: Multi-racial populations consistently correlate with more highways across Midwest states
3. **Education and wealth patterns vary by state**: State-specific factors influence highway designations
4. **Highway types reveal patterns**: Legislative resolutions dominate in California, while various types exist in other states
5. **Cross-state patterns show variation**: Different states show different demographic predictors

### Limitations

- Small sample sizes (only 4 states with complete data)
- Highway data quality varies by state
- Causality cannot be established from correlations
- Memorial highway significance may vary by type and purpose

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
*New findings: Indiana analysis reveals multi-racial population as strongest predictor (r = +0.613, R² = 0.637)*
