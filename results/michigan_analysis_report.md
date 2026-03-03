# Michigan Memorial Highway Analysis Report

## Data Summary

### Datasets Used
- **Demographics**: Michigan counties demographics (ACS 2023)
  - Source: michigan_counties_demographics.csv
  - Counties: 83 total
  - Variables: Age, income, home values, race/ethnicity, education, unemployment, poverty

- **Highways**: Memorial highways across Michigan counties
  - Source: michigan_memorial_highways.csv
  - Total highways: 138
  - Counties with highways: 51
  - Counties without highways: 32

### Data Merging
- 51 counties successfully matched between datasets
- 32 counties in demographics not found in highway data (no highways)

### Highway Statistics
- Total highways analyzed: 138
- Average highways per county: 1.66
- Median highways per county: 1.00
- Range: 0 to 9 highways per county

## Key Findings

### 1. Strongest Correlations with Highway Count

| Variable | Correlation (r) | Direction | Interpretation |
|----------|----------------|-----------|----------------|
| Pct_TwoOrMore | +0.605 | Strong positive | Counties with more multi-racial residents have more highways |
| Pct_SomeOther_Alone | -0.470 | Moderate negative | Counties with more "some other race" residents have fewer highways |
| Median_Age | -0.351 | Moderate negative | Younger counties have more highways |

### 2. Significant Demographic Differences (T-Tests)

Counties were split into high (≥1) and low (<1) highway count groups based on median.

**Significant differences found (p < 0.05):**

| Variable | High Group Mean | Low Group Mean | Effect Size | Interpretation |
|----------|----------------|----------------|-------------|----------------|
| Median_Age | 43.45 | 46.32 | -0.75 | High-highway counties are younger |
| Pct_SomeOther_Alone | 83.71 | 87.12 | -0.68 | High-highway counties have fewer "some other race" residents |
| Pct_TwoOrMore | 4.95 | 3.85 | 0.63 | High-highway counties have more multi-racial residents |
| Pct_NHPI_Alone | 95.36 | 96.82 | -0.51 | High-highway counties have fewer Native Hawaiian/Pacific Islander residents |
| Pct_White_Alone | 3.37 | 2.52 | 0.46 | High-highway counties have more white residents |

### 3. Regression Analysis

**OLS Model: highway_count ~ pct_twoormore + pct_someother_alone + median_age + unemployment_rate + pct_hispanic**

- **R² = 0.418** (41.8% of variance explained)
- **Adjusted R² = 0.380** (38.0% after accounting for predictors)
- **F-statistic = 11.05** (p < 0.001)

**Significant predictors:**
- **Pct_TwoOrMore**: Coefficient = 0.3027 (p = 0.004)
  - Each additional percentage point of multi-racial residents associated with 0.30 more highways

**Non-significant predictors:**
- Pct_SomeOther_Alone (p = 0.303)
- Median_Age (p = 0.144)
- Unemployment_Rate (p = 0.555)
- Pct_Hispanic (p = 0.541)

### 4. Top Counties by Highway Count

| County | Highway Count |
|--------|---------------|
| Genesee County, Michigan | 9 |
| Macomb County, Michigan | 9 |
| Wayne County, Michigan | 8 |
| Jackson County, Michigan | 8 |
| Monroe County, Michigan | 7 |

## Limitations

1. **County Matching**: Highway data extracted from descriptions; some highways may span multiple counties
2. **Sample Size**: Only 51 of 83 counties have highways; 32 counties have none
3. **Highway Definition**: Memorial highways may vary in length and significance
4. **Causality**: Correlation does not imply causation

## Saved Visualizations

1. **michigan_correlation_heatmap.png** - Full correlation matrix of all variables
2. **michigan_pct_twoormore_vs_highways.png** - Scatter plot of highway count vs multi-racial percentage
3. **michigan_residual_plot.png** - Regression residual diagnostics

## Data Files Saved

1. **michigan_merged_data.csv** - Merged demographics and highway data
2. **michigan_correlation_matrix.csv** - Full correlation matrix
3. **michigan_ttest_results.csv** - All t-test results
4. **michigan_regression_summary.txt** - OLS regression output

## Conclusion

The analysis reveals that memorial highway counts in Michigan counties are associated with demographic composition. Counties with higher highway counts tend to have:
- More multi-racial residents
- Younger populations
- Fewer residents identifying as "some other race"

The strongest predictor in the regression model was the percentage of multi-racial residents, suggesting that demographic diversity may play a role in the designation of memorial highways.

---

*Analysis completed on 2026-03-03 13:57*
*Output directory: /media/sam/USB DISK/openclaw-capstone-agent/results/*
