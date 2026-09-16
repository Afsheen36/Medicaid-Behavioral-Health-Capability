# Methodology

## Study Objective

This project examines state-level variation in Medicaid behavioral health
infrastructure across the United States.

The analysis distinguishes between two related but different concepts:

1. **Medicaid participation** — the percentage of mental health treatment
   facilities that accept Medicaid.

2. **Population-relative Medicaid behavioral health capacity** — the number
   of Medicaid-accepting mental health treatment facilities relative to the
   size of the Medicaid-enrolled population.

The project also explores whether state psychiatrist workforce supply and
socioeconomic context are associated with selected service capabilities
among Medicaid-accepting mental health facilities.


## Geographic Scope

The primary analytic geography consists of the 50 U.S. states and the
District of Columbia.

Puerto Rico and unidentified/other geographic records were excluded from
the primary N-SUMHSS state analysis.

Rhode Island remains part of the overall state dataset but is excluded from
analyses requiring a Medicaid enrollment denominator because the December
2024 CMS extract used in this project reports zero Medicaid enrollment for
Rhode Island. This value was treated as unusable rather than interpreted as
true zero enrollment.


## Data Sources

### 1. N-SUMHSS 2024

The National Substance Use and Mental Health Services Survey (N-SUMHSS)
2024 public-use data were used to identify mental health treatment
facilities and characterize Medicaid participation and selected service
capabilities.

The mental-health analytic cohort contained 14,331 facilities before
restriction to the primary U.S. analytic geography.

Key measures included:

- Medicaid acceptance
- Outpatient treatment
- Day treatment / partial hospitalization
- Residential treatment
- Inpatient treatment
- Suicide-related services
- Services for serious mental illness / co-occurring substance use
- Primary care integration


### 2. Area Health Resources Files (AHRF)

AHRF workforce data were used to estimate state psychiatrist supply.

County-level psychiatrist counts were aggregated to the state level and
standardized using population estimates to calculate psychiatrists per
100,000 population.

The workforce measure primarily reflects 2023 psychiatrist supply.


### 3. American Community Survey (ACS)

The 2024 ACS 5-year estimates were obtained programmatically through the
U.S. Census Bureau Data API.

State-level socioeconomic measures included:

- Total population
- Poverty rate
- Median household income

API credentials were stored locally using environment variables and were
not included in the public repository.


### 4. CMS Medicaid Enrollment

CMS Medicaid and CHIP Performance Indicator data were used to obtain
December 2024 updated state enrollment counts.

The primary denominator for this project is total Medicaid enrollment
rather than combined Medicaid and CHIP enrollment.


## Primary Measures

### Medicaid Acceptance Percentage

For each state:

Medicaid acceptance percentage =

(number of mental health facilities accepting Medicaid /
total number of mental health facilities) × 100


### Medicaid-Accepting Facilities per 100,000 Medicaid Enrollees

For each state with a usable CMS enrollment denominator:

Medicaid-accepting facilities per 100,000 Medicaid enrollees =

(number of Medicaid-accepting mental health facilities /
total Medicaid enrollment) × 100,000


### Psychiatrist Supply

Psychiatrist supply was expressed as:

psychiatrists per 100,000 state residents.


## Statistical Analysis

State-level associations between psychiatrist supply and facility service
capabilities were examined using Pearson and Spearman correlations.

Because multiple service capabilities were evaluated, false discovery rate
(FDR) correction was applied to the Spearman tests.

Sensitivity analyses were conducted excluding the District of Columbia
because DC had substantially higher psychiatrist supply than other
jurisdictions.

An exploratory multivariable ordinary least squares model examined
state suicide-service capability as a function of:

- psychiatrists per 100,000 population
- poverty rate
- median household income

HC3 heteroskedasticity-robust standard errors were used.

A second model excluded the District of Columbia as a sensitivity analysis.


## Interpretation

All analyses are observational and ecological.

Associations identified at the state level should not be interpreted as
individual-level relationships or causal effects.

Facility counts measure the presence of treatment organizations rather than
treatment slots, staffing intensity, appointment availability, geographic
accessibility, service quality, or realized utilization.


## Reproducibility

The project uses Python scripts for:

- source-data inspection
- analytic cohort construction
- state aggregation
- API-based data acquisition
- cross-source integration
- statistical analysis
- sensitivity analysis
- visualization

Raw and processed datasets are excluded from version control where
appropriate. Reproducible code, research tables, and selected figures are
maintained in the public repository.