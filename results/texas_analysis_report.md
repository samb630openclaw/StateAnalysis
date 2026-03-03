# Texas Analysis Report

## Data Summary
- **Counties analyzed**: 254
- **Counties with highways**: 114
- **Counties without highways**: 140
- **Total highways**: 508
- **Highways per county**: Mean = 2.0, Median = 0.0, Max = 20

## Key Findings

### Top Counties by Highway Count
1. Hudspeth County: 20 highways
2. Webb County: 18 highways
3. Gillespie County: 18 highways
4. Harris County: 17 highways
5. Tom Green County: 15 highways

### Strongest Correlations with Highway Count
1. HS Graduation Rate: r = +0.183 (p = 0.0033)
2. Asian Percentage: r = +0.182 (p = 0.0035)
3. White Percentage: r = +0.144 (p = 0.0218)
4. Black Percentage: r = +0.142 (p = 0.0236)
5. Median Household Income: r = -0.201 (p = 0.0013)

### Significant Demographic Differences (T-Tests)
Counties split into high (≥2 highways) and low (<2 highways) groups:

| Variable | Effect Size | Interpretation |
|----------|-------------|----------------|
| HS Graduation Rate | 0.49 | High-highway counties have significantly higher education |
| Black Percentage | 0.36 | High-highway counties have more Black population |
| Median Age | -0.30 | High-highway counties are younger |

### Regression Analysis
- **R² = 0.173** (17.3% of variance explained)
- **Strongest predictors**: 
  - HS Graduation Rate (p < 0.001)
  - Median Household Income (p = 0.006)
  - Unemployment Rate (p = 0.038)

## Limitations
- 140 counties (55%) have no highways
- Median highway count is 0 (highly skewed distribution)
- R² = 0.173 indicates limited explanatory power
- Some demographic variables may be collinear

## Files Created
1. texas_highway_aggregates.csv
2. texas_merged_data.csv
3. texas_correlation_matrix.csv
4. texas_correlation_heatmap.png
5. texas_median_age_vs_highways.png
6. texas_median_household_income_vs_highways.png
7. texas_pct_asian_alone_vs_highways.png
8. texas_pct_black_alone_vs_highways.png
9. texas_pct_white_alone_vs_highways.png
10. texas_regression_summary.txt
11. texas_residual_plot.png
12. texas_significant_ttest_results.csv
13. texas_top_counties.csv
14. texas_top_counties.png
15. texas_ttest_results.csv
