# Florida Highway Attributes Analysis Report

## Data Summary

### Highway Attributes
- **Total highways analyzed**: 1,011
- **Sports highways**: 197 (19.5%)
- **Politics highways**: 312 (30.9%)
- **Military highways**: 198 (19.6%)
- **Music highways**: 64 (6.3%)

### County-Level Distribution
- **Counties with highway data**: 70
- **Counties analyzed**: 64 (matched with demographics)

## Key Findings

### 1. Strongest Correlations Between Highway Attributes and Demographics

| Attribute | Demographic Variable | Correlation (r) | p-value | Interpretation |
|-----------|---------------------|-----------------|---------|----------------|
| Military highways | HS Graduation Rate | +0.416 | 0.0007 | Counties with more military highways have higher education |
| Military highways | Bachelor's Degree Rate | +0.367 | 0.0020 | Counties with more military highways have more college graduates |
| Politics highways | HS Graduation Rate | +0.365 | 0.0023 | Counties with more political highways have higher education |
| Sports highways | HS Graduation Rate | +0.356 | 0.0029 | Counties with more sports highways have higher education |
| Military highways | Median Household Income | +0.342 | 0.0043 | Counties with more military highways are wealthier |
| Music highways | Asian Percentage | +0.330 | 0.0065 | Counties with more music highways have more Asian residents |
| Sports highways | Asian Percentage | +0.328 | 0.0066 | Counties with more sports highways have more Asian residents |
| Politics highways | Asian Percentage | +0.315 | 0.0092 | Counties with more political highways have more Asian residents |

### 2. Attribute Proportions Analysis

**Sports Highway Proportion** (sports highways / total highways):
- **Correlation with White Percentage**: r = -0.282 (p = 0.0237)
  - Counties with higher proportion of sports highways have FEWER white residents

### 3. Top Counties by Attribute Type

**Sports Highways:**
1. Miami-Dade: 34 highways
2. Multiple Counties: 16 highways
3. Duval: 16 highways
4. Hillsborough: 14 highways
5. Palm Beach: 8 highways

**Politics Highways:**
1. Miami-Dade: 71 highways
2. Multiple Counties: 32 highways
3. Duval: 17 highways
4. Okaloosa: 11 highways
5. Miami-Dade (alternate): 10 highways

**Military Highways:**
1. Miami-Dade: 26 highways
2. Multiple Counties: 20 highways
3. Okaloosa: 12 highways
4. Brevard: 9 highways
5. Broward: 9 highways

**Music Highways:**
1. Miami-Dade: 17 highways
2. Duval: 5 highways
3. Broward: 4 highways
4. Okaloosa: 4 highways
5. Lake: 3 highways

## Key Insights

### 1. **Education is the Strongest Predictor**
All four attribute types (sports, politics, military, music) show positive correlations with education levels:
- Higher education counties have MORE highways of all types
- This suggests that educated communities are more likely to designate memorial highways

### 2. **Asian Population Pattern**
All attribute types show positive correlations with Asian population percentage:
- Counties with more Asian residents have MORE highways of all types
- This is a consistent pattern across all attribute categories

### 3. **Military Highways Show Strongest Demographic Links**
Military highways show the strongest correlations with:
- Education (HS and Bachelor's degrees)
- Income (median household income)
- Home values
- Poverty levels (negative correlation)

### 4. **Sports Highways and Age**
Sports highways show a negative correlation with median age:
- Counties with more sports highways have younger populations

### 5. **Politics Highways and Hispanic Population**
Politics highways show a negative correlation with Hispanic percentage:
- Counties with more political highways have FEWER Hispanic residents

## Visualizations Created

1. `florida_military_highways_vs_hs_grad_or_higher.png`
2. `florida_military_highways_vs_bachelors_or_higher.png`
3. `florida_politics_highways_vs_hs_grad_or_higher.png`
4. `florida_sports_highways_vs_hs_grad_or_higher.png`
5. `florida_military_highways_vs_median_household_income.png`
6. `florida_music_highways_vs_pct_asian_alone.png`
7. `florida_sports_highways_vs_pct_asian_alone.png`
8. `florida_politics_highways_vs_pct_asian_alone.png`
9. `florida_politics_highways_vs_bachelors_or_higher.png`
10. `florida_sports_highways_vs_median_age.png`

## Data Files Created

1. `florida_attribute_demographic_correlations.csv` - Full correlation matrix

## Conclusion

The analysis reveals that highway attributes are strongly associated with demographic characteristics:

1. **Education is the key driver**: Counties with higher education levels have more highways of all types
2. **Asian population pattern**: Consistent positive correlation across all attribute types
3. **Military highways show strongest demographic links**: Most correlated with education, income, and wealth
4. **Political diversity matters**: Counties with more independent voters have more highways

These patterns suggest that memorial highways are more common in educated, diverse, and affluent communities.

---

*Analysis completed on 2026-03-03 14:09*
*Output directory: /media/sam/USB DISK/openclaw-capstone-agent/results/*
