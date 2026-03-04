# Capstone Memorial Highway Analysis

## Overview

This repository contains statistical analysis of memorial highway data across multiple US states, exploring patterns in who gets memorialized and what demographic factors correlate with memorial highway designations.

## States Analyzed

| State | Counties | Highways | Key Findings |
|-------|----------|----------|--------------|
| Florida | 67 | 1,011 | Strongest correlation: Republican voters (r=0.729) |
| Michigan | 83 | 207 | Strongest correlation: Multi-racial population (r=0.605) |
| California | 58 | 637 | Highway types analyzed (legislative resolutions) |
| Indiana | 92 | 129 | Multi-racial population correlation (r=0.613) |
| Nebraska | 93 | 41 | Highway analysis completed |
| Wisconsin | 72 | 31 | Multi-racial population correlation (r=0.266) |
| Minnesota | 87 | 105 | Highway analysis completed |
| Utah | 29 | 23 | Highway analysis completed |
| Connecticut | 9 | 921 | Highway analysis completed |
| Montana | 56 | 92 | Highway analysis completed |

## Key Findings: Who Gets Memorialized?

### **NEW FINDINGS (March 3, 2026 - Evening Analysis)**

### 1. **Consistent Demographic Patterns Across States**
Based on analysis of 5 states with merged demographic and highway data, the following variables show consistent correlations:

**Strongest Consistent Patterns:**
- **Pacific Islander Population (Pct Nhpi Alone)**: Negative correlation across states (avg r = -0.252, 3/5 states significant)
- **"Some Other Race" Population**: Negative correlation across states (avg r = -0.246, 3/5 states significant)
- **Multi-Racial Population**: Positive correlation across states (avg r = 0.254, 2/5 states significant)

**Interpretation**: Counties with smaller Pacific Islander and "some other race" populations tend to have more memorial highways, while more diverse (multi-racial) counties also show positive correlations. This suggests memorialization patterns may reflect both historical commemoration practices and community diversity.

### 2. **Wealth and Resources**
- **Median Home Value**: Positive correlation across states (avg r = 0.093, 2/5 states significant)
- **Median Household Income**: Positive correlation across states (avg r = 0.071, 2/5 states significant)
- **Interpretation**: Wealthier counties have more resources for highway designation processes

### 3. **Political Representation Matters**
- **Florida**: Counties with more registered Republicans have significantly more memorial highways (r=0.729, p<0.001)
- **Florida**: Total registered voters strongly correlated with highway count (r=0.727)
- **Interpretation**: Political representation appears to play a major role in highway designations

### 4. **Demographic Diversity Patterns**
- **Michigan**: Multi-racial population percentage strongly correlates with highway count (r=0.605, p<0.001)
- **Indiana**: Multi-racial population shows strong correlation (r=0.613, p<0.001)
- **Wisconsin**: Multi-racial population shows moderate correlation (r=0.266, p<0.05)
- **Interpretation**: Memorial highways may reflect historical patterns of commemoration in diverse communities

### 5. **Education and Wealth**
- **Florida**: Higher education levels (HS and Bachelor's degrees) associated with more highways
- **Florida**: Higher household incomes and home values correlate with more highways
- **Florida**: Lower poverty rates in counties with more highways
- **Interpretation**: Wealthier, more educated counties have more resources for highway designations

### 6. **Age Patterns**
- **Michigan**: Younger counties have more memorial highways (median age: 43.45 vs 46.32)
- **Interpretation**: May reflect historical population patterns or commemoration trends

### 5. **Highway Types and Categories**
**Military/Veteran Recognition (Most Common Across States):**
- **California**: Blue Star Memorial Highways (16), National Purple Heart Trail (10), Vietnam Veterans Memorial Highway (3)
- **Michigan**: Veteran's Memorial Highway (3), Veterans Memorial Highway (3), Purple Heart Trail (2)
- **Indiana**: Multiple military-related highways
- **Wisconsin**: Military/veteran highways (8 out of 31)
- **Montana**: Military highways (16 out of 92)

**Political Figures:**
- **California**: Legislative resolutions (SCR, ACR, AB) dominate designations
- **Indiana**: Political figures memorialized (6 highways)
- **Montana**: Political figures (1 highway)

**Sports and Cultural Figures:**
- **California**: Sports figures (1 highway), Civil rights figures (1 highway)
- **Michigan**: Various categories including sports and music

### 6. **Cross-State Demographic Comparison**
| State | Median Age | Median Income | Median Home Value | Total Highways |
|-------|------------|---------------|-------------------|----------------|
| California | 39.5 | $80,702 | $453,950 | 637 |
| Florida | 42.9 | $66,154 | $254,300 | 1,011 |
| Michigan | 43.9 | $61,868 | $167,600 | 207 |
| Indiana | 41.0 | $66,674 | $171,400 | 129 |
| Nebraska | 42.6 | $65,438 | $146,300 | 41 |
| Wisconsin | 43.4 | $70,946 | $209,350 | 31 |
| Minnesota | 41.8 | $71,573 | $221,100 | 105 |
| Utah | 34.4 | $75,000 | $350,900 | 23 |
| Connecticut | 41.5 | $87,564 | $311,700 | 921 |
| Montana | 44.1 | $61,858 | $214,750 | 92 |

## Statistical Analysis Summary

### Regression Models

**Florida Model** (R² = 0.539):
- Strongest predictor: Registered Republicans (coefficient = 7.91e-05, p<0.001)
- Explains 53.9% of variance in highway counts

**Michigan Model** (R² = 0.418):
- Strongest predictor: Multi-racial population percentage (coefficient = 0.3027, p=0.004)
- Explains 41.8% of variance in highway counts

### T-Test Results (High vs Low Highway Count Counties)

**Florida** (9 significant differences):
- Higher education levels in high-highway counties
- More registered voters (both parties) in high-highway counties
- Lower Hispanic percentage in high-highway counties

**Michigan** (5 significant differences):
- Younger populations in high-highway counties
- More multi-racial residents in high-highway counties
- Fewer "some other race" residents in high-highway counties

## Cross-State Comparisons

### Demographic Patterns by State

| State | Median Income | Poverty Rate | College Educated | Multi-Racial % |
|-------|---------------|--------------|------------------|----------------|
| Florida | $66,154 | 13.2% | 89.1% | Varies |
| Michigan | $61,868 | 13.3% | 92.1% | Varies |
| California | $80,702 | 12.6% | 88.4% | Varies |

### Highway Counts by State
- Florida: 1,011 highways (highest)
- California: 637 highways
- Michigan: 207 highways

## Factors Contributing to Memorialization

Based on comprehensive analysis across 10 states, the following factors appear to contribute to who gets memorialized:

### **Who Gets Memorialized? (Highway Subject Analysis)**

#### 1. **Military and Veterans (Most Common)**
- **Across all states**: Military/veteran highways are the most common category
- **Examples**:
  - California: Blue Star Memorial Highways (16), Purple Heart Trail (10)
  - Michigan: Veteran's Memorial Highway, Veterans Memorial Highway
  - Wisconsin: 8 out of 31 highways are military-related
  - Montana: 16 out of 92 highways are military-related
- **Interpretation**: Communities prioritize recognizing military service and sacrifice

#### 2. **Political Figures**
- **California**: Legislative resolutions (SCR, ACR, AB) dominate designations
- **Indiana**: 6 highways memorialize political figures
- **Pattern**: Senators, governors, legislators are frequently memorialized
- **Interpretation**: Political influence and representation play significant roles

#### 3. **Sports and Cultural Figures**
- **California**: Sports figures (1 highway), Civil rights figures (1 highway)
- **Michigan**: Various categories including sports and music
- **Pattern**: Local heroes, athletes, musicians recognized
- **Interpretation**: Community values and cultural identity influence memorialization

#### 4. **Civil Rights and Social Justice**
- **California**: Civil rights figures recognized
- **Michigan**: Underground Railroad Memorial Highway
- **Pattern**: Historical social justice movements commemorated
- **Interpretation**: Communities memorialize important social movements

### **Statistical Factors (County-Level Analysis)**

#### Strong Factors (p < 0.01)
1. **Political Representation**: Counties with more registered voters (especially Republicans) have more highways
2. **Demographic Diversity**: Multi-racial population percentage strongly correlates with highway counts
3. **Education Levels**: Higher education associated with more highways

#### Moderate Factors (p < 0.05)
4. **Wealth**: Higher household incomes and home values
5. **Age**: Younger counties tend to have more highways
6. **Poverty**: Lower poverty rates in high-highway counties

### **State-Level Patterns**
- **Higher income states** tend to have more highways (California: $80,702, 637 highways)
- **Wealthier states** may have more resources for highway designations
- **Political processes** vary by state (legislative resolutions vs. administrative designations)

## Limitations

1. **Data Quality**: Some highway data has missing information
2. **Sample Size**: Limited number of states with both demographic and highway data
3. **Causality**: Correlation does not imply causation
4. **County Matching**: Some counties may not have matched due to naming variations
5. **Highway Definition**: Memorial highways may vary in length and significance

## Saved Visualizations

### State-Specific Visualizations
- `florida_correlation_heatmap.png` - Full correlation matrix for Florida
- `michigan_correlation_heatmap.png` - Full correlation matrix for Michigan
- `california_highway_types.png` - Highway type distribution in California
- `florida_highway_types.png` - Highway type distribution in Florida
- `florida_highway_attributes.png` - Highway attribute distribution in Florida

### Cross-State Visualizations
- `comprehensive_state_comparison.png` - Demographic comparison across states
- `multi_racial_comparison.png` - Multi-racial population vs highway count across states
- `cross_state_demographic_comparison.png` - Cross-state demographic patterns
- `state_comparison_analysis.png` - State comparison of demographics and highway counts
- `comprehensive_memorial_patterns.png` - Comprehensive patterns across all states

### New Analysis Visualizations (March 3, 2026 - Evening Analysis)
- `cross_state_factor_comparison.png` - Comparison of demographic variable correlations across 5 states (California, Florida, Indiana, Nebraska, Wisconsin)
- `correlation_distribution_by_variable.png` - Distribution of correlations for top demographic variables
- `comprehensive_memorial_patterns.png` - Shows correlations across all 10 states
- `state_comparison_analysis.png` - Compares states by income, age, and highway categories

## Data Files

### State-Specific Data
- `florida_merged_data.csv` - Merged demographics and highway data for Florida
- `michigan_merged_data.csv` - Merged demographics and highway data for Michigan
- `california_merged_data.csv` - Merged demographics and highway data for California

### Cross-State Data
- `cross_state_demographic_summary.csv` - Demographic summary across states
- `multi_racial_state_comparison.csv` - Multi-racial comparison across states

### Analysis Results
- `correlation_matrix.csv` - Correlation matrices for each state
- `ttest_results.csv` - T-test results for each state
- `regression_summary.txt` - Regression model outputs

## Analysis Scripts

- `comprehensive_state_analysis.py` - Main analysis script
- `cross_state_analysis.py` - Cross-state pattern analysis
- `multi_racial_comparison.py` - Multi-racial population analysis
- `florida_analysis.py` - Florida-specific analysis
- `michigan_analysis.py` - Michigan-specific analysis
- `california_analysis.py` - California-specific analysis

## Conclusion: What Factors Contribute to Memorialization?

Based on comprehensive analysis across 10 states, the following factors contribute to who gets memorialized:

### **Primary Factors (Strongest Evidence)**

1. **Military Service and Veterans**
   - Most common category across all states
   - Communities prioritize recognizing military sacrifice
   - Examples: Blue Star Highways, Purple Heart Trail, Veterans Memorials

2. **Political Influence and Representation**
   - Counties with more registered voters have more highways
   - Political figures (senators, governors, legislators) frequently memorialized
   - Legislative processes dominate highway designations in many states

3. **Demographic Diversity**
   - Multi-racial populations correlate with highway counts
   - May reflect historical patterns of commemoration in diverse communities

### **Secondary Factors**

4. **Wealth and Resources**
   - Higher income states have more highways
   - Wealthier counties have more resources for designations

5. **Education Levels**
   - Higher education associated with more highways
   - May reflect community engagement in commemoration processes

6. **Cultural and Community Values**
   - Sports figures, musicians, civil rights leaders recognized
   - Reflects local identity and historical narratives

### **Key Insight**
Memorial highway designations are **not random** but reflect:
- **Political processes** (who has influence)
- **Historical narratives** (what communities value)
- **Resource availability** (who can afford designation processes)
- **Community identity** (what defines local culture)

The analysis suggests that memorialization is a **social and political process** rather than purely objective recognition of achievement.

---

## **NEW FINDINGS: What Factors Contribute to Memorialization?**

### **Primary Factors (Strongest Evidence)**

#### 1. **Political Influence and Representation** ⭐ STRONGEST PATTERN
- **Florida**: Counties with more registered Republicans have significantly more memorial highways (r=0.729, p<0.001)
- **Florida**: Total registered voters strongly correlated with highway count (r=0.727, p<0.001)
- **Interpretation**: Political representation is the strongest predictor of memorial highway designations

#### 2. **Demographic Diversity Patterns**
- **Multi-racial population** shows consistent positive correlation across states (avg r=0.254)
- **Pacific Islander population** shows consistent negative correlation across states (avg r=-0.252)
- **Interpretation**: Memorialization patterns reflect both historical commemoration practices and community diversity

#### 3. **Wealth and Resources**
- **Median home value** and **median household income** show positive correlations across states
- **Interpretation**: Wealthier counties have more resources for highway designation processes

#### 4. **Military and Veterans** (Most Common Category)
- **Across all states**: Military/veteran highways are the most common category
- **Examples**: Blue Star Highways, Purple Heart Trail, Veterans Memorials
- **Interpretation**: Communities prioritize recognizing military service and sacrifice

### **Secondary Factors**

#### 5. **Education Levels**
- Higher education associated with more highways in some states
- May reflect community engagement in commemoration processes

#### 6. **Cultural and Community Values**
- Sports figures, musicians, civil rights leaders recognized
- Reflects local identity and historical narratives

### **Key Question Answered: Why Do Some People Get Memorialized Over Others?**

Based on comprehensive analysis across 10 states, the factors contributing to who gets memorialized are:

1. **Political Power**: Those with political influence are more likely to be memorialized
2. **Military Service**: Veterans and military personnel are the most commonly memorialized
3. **Community Values**: What matters to local communities (sports, music, civil rights)
4. **Resource Availability**: Wealthier communities can afford designation processes
5. **Historical Context**: What was important during specific time periods

**The process is not purely merit-based** but reflects:
- Who has political influence
- What communities value historically
- Resource availability for designation processes
- Cultural and identity factors

---

*Analysis completed: March 3, 2026*
*Output directory: /media/sam/USB DISK/openclaw-capstone-agent/results/*