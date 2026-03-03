# Florida Memorial Highway Analysis Report

## Data Summary

### Datasets Used
- **Demographics**: Florida counties demographics with voter registration data
  - Source: florida_counties_demographics_with_voterreg.csv
  - Counties: 67 total
  - Variables: Age, income, home values, race/ethnicity, education, unemployment, poverty, voter registration

- **Highways**: Memorial highways across Florida counties
  - Source: highways.csv
  - Total highways: 1,011
  - Counties with highways: 70
  - Variables: Honoree age, gender, military/political/sports/music involvement, cause of death

### Data Merging
- 64 counties successfully matched between datasets
- 3 counties in demographics not found in highway data
- 6 counties in highway data not found in demographics (likely due to county name variations)

### Highway Statistics
- Total highways analyzed: 603
- Average highways per county: 9.4
- Median highways per county: 6.5
- Range: 1 to 53 highways per county

## Key Findings

### 1. Strongest Correlations with Highway Count

| Variable | Correlation (r) | Direction | Interpretation |
|----------|----------------|-----------|----------------|
| Registered Republicans | +0.729 | Strong positive | Counties with more Republicans have more highways |
| Registered Total | +0.727 | Strong positive | Total registered voters strongly correlated |
| Registered Democrats | +0.719 | Strong positive | Counties with more Democrats also have more highways |
| HS Graduation Rate | +0.416 | Moderate positive | Higher education levels associated with more highways |
| Bachelor's Degree Rate | +0.323 | Moderate positive | Higher education levels associated with more highways |
| Median Household Income | +0.295 | Moderate positive | Wealthier counties have more highways |
| Median Home Value | +0.288 | Moderate positive | Higher property values associated with more highways |

### 2. Significant Demographic Differences (T-Tests)

Counties were split into high (≥6.5) and low (<6.5) highway count groups based on median.

**Significant differences found (p < 0.05):**

| Variable | High Group Mean | Low Group Mean | Effect Size | Interpretation |
|----------|----------------|----------------|-------------|----------------|
| HS Graduation Rate | Higher | Lower | 1.21 | High-highway counties have significantly higher education |
| Registered Republicans | Higher | Lower | 1.20 | High-highway counties have more Republicans |
| Registered Total | Higher | Lower | 1.08 | High-highway counties have more voters |
| Bachelor's Degree Rate | Higher | Lower | 1.01 | High-highway counties have more college graduates |
| Registered Democrats | Higher | Lower | 0.98 | High-highway counties have more Democrats |
| Median Household Income | Higher | Lower | 0.74 | High-highway counties are wealthier |
| Hispanic Percentage | Lower | Higher | -0.69 | High-highway counties have fewer Hispanics |
| Median Home Value | Higher | Lower | 0.60 | High-highway counties have higher property values |
| Poverty Rate | Lower | Higher | -0.53 | High-highway counties have less poverty |

### 3. Regression Analysis

**OLS Model: highway_count ~ Registered_Republican + HS_Grad_or_Higher + Pct_Below_Poverty_Level + Median_Household_Income**

- **R² = 0.539** (53.9% of variance explained)
- **Adjusted R² = 0.508** (50.8% after accounting for predictors)
- **F-statistic = 17.24** (p < 0.001)

**Significant predictors:**
- **Registered_Republican**: Coefficient = 7.91e-05 (p < 0.001)
  - Each additional Republican voter associated with 0.000079 more highways
  - This is the strongest predictor in the model

**Non-significant predictors:**
- HS_Grad_or_Higher (p = 0.724)
- Pct_Below_Poverty_Level (p = 0.504)
- Median_Household_Income (p = 0.996)

### 4. Top Counties by Highway Count

| County | Highway Count |
|--------|---------------|
| Miami-Dade | 53 |
| Broward | 42 |
| Hillsborough | 35 |
| Palm Beach | 26 |
| Brevard | 26 |
| Orange | 25 |
| Duval | 22 |
| Lee | 21 |
| Collier | 20 |
| Polk | 19 |

## Limitations

1. **Data Quality**: Some highway data has missing age information (34/64 counties missing avg_age_at_death)
2. **Sample Size**: Only 64 counties analyzed; statistical power limited for small counties
3. **Causality**: Correlation does not imply causation; cannot determine if highways cause demographic patterns or vice versa
4. **County Name Matching**: Some counties may not have matched due to naming variations
5. **Highway Definition**: Memorial highways may vary in length and significance; counts may not reflect actual highway density

## Saved Visualizations

1. **correlation_heatmap.png** - Full correlation matrix of all variables
2. **highways_vs_republicans.png** - Scatter plot of highway count vs Republican voters
3. **highways_vs_hs_grad.png** - Scatter plot of highway count vs HS graduation rate
4. **top_counties_highways.png** - Bar chart of top 15 counties by highway count
5. **highways_vs_poverty.png** - Scatter plot of highway count vs poverty rate
6. **residual_plot.png** - Regression residual diagnostics

## Data Files Saved

1. **florida_highway_aggregates.csv** - Aggregated highway data by county
2. **florida_merged_data.csv** - Merged demographics and highway data
3. **correlation_matrix.csv** - Full correlation matrix
4. **ttest_results.csv** - All t-test results
5. **significant_ttest_results.csv** - Only significant t-test results
6. **regression_summary.txt** - OLS regression output

## Conclusion

The analysis reveals that memorial highway counts in Florida counties are strongly associated with voter registration numbers and education levels. Counties with higher highway counts tend to have:
- More registered voters (both Republican and Democrat)
- Higher education levels (HS and Bachelor's degree rates)
- Higher household incomes and home values
- Lower poverty rates
- Lower Hispanic population percentages

The strongest predictor in the regression model was the number of registered Republicans, suggesting that political representation may play a role in the designation of memorial highways.

---

*Analysis completed on 2026-03-03 11:48*
*Output directory: /media/sam/USB DISK/openclaw-capstone-agent/results/*
