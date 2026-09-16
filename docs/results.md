# Results

## Overview

The analysis identified substantial state variation in both Medicaid
participation among mental health treatment facilities and the amount of
Medicaid-accepting facility infrastructure relative to state Medicaid
enrollment.

The results also show that Medicaid participation and population-relative
capacity capture different aspects of the behavioral health system.


## Medicaid Participation Across States

Among the 50 states and the District of Columbia, the percentage of mental
health treatment facilities accepting Medicaid varied substantially.

Examples include:

- Wyoming: 100.0%
- District of Columbia: 100.0%
- Maine: 98.8%
- New York: 95.8%
- Arizona: 88.3%
- Texas: 73.0%
- Florida: 65.1%
- Utah: 65.6%
- California: 51.5%

These estimates describe the proportion of surveyed mental health treatment
facilities participating in Medicaid. They do not measure the number of
facilities available relative to the Medicaid-enrolled population.


## Arizona Behavioral Health Capability

Arizona contained 528 mental health treatment facilities in the analytic
dataset, of which 466 accepted Medicaid.

This corresponds to a Medicaid participation rate of:

**88.3%**

Among Medicaid-accepting Arizona facilities, selected service capabilities
included:

| Capability | Arizona (%) |
|---|---:|
| Outpatient treatment | 78.8 |
| Day treatment / partial hospitalization | 13.1 |
| Residential treatment | 22.7 |
| Inpatient treatment | 7.5 |
| Suicide-related services | 70.8 |
| Serious mental illness / co-occurring substance use services | 87.6 |
| Primary care integration | 39.9 |


## Arizona Compared With the National Facility Profile

Compared with the national profile of Medicaid-accepting mental health
facilities, Arizona showed:

| Capability | Arizona (%) | National (%) | Difference (percentage points) |
|---|---:|---:|---:|
| Outpatient treatment | 78.8 | 84.3 | -5.5 |
| Day treatment / partial hospitalization | 13.1 | 12.6 | +0.5 |
| Residential treatment | 22.7 | 13.9 | +8.8 |
| Inpatient treatment | 7.5 | 9.5 | -2.0 |
| Suicide-related services | 70.8 | 70.5 | +0.3 |
| Serious mental illness / co-occurring substance use services | 87.6 | 82.1 | +5.5 |
| Primary care integration | 39.9 | 27.3 | +12.6 |

These are descriptive comparisons and should not be interpreted as causal
effects or measures of service quality.


## Psychiatrist Supply and Facility Capability

State psychiatrist supply was linked with the N-SUMHSS facility capability
measures.

In the initial 51-jurisdiction Spearman analysis:

| Capability | Spearman rho | p-value | FDR q-value |
|---|---:|---:|---:|
| Outpatient treatment | -0.350 | 0.012 | 0.042 |
| Day treatment / partial hospitalization | 0.089 | 0.533 | 0.622 |
| Residential treatment | 0.070 | 0.627 | 0.627 |
| Inpatient treatment | -0.250 | 0.077 | 0.135 |
| Suicide-related services | -0.369 | 0.008 | 0.042 |
| SMI / co-occurring substance use services | -0.317 | 0.023 | 0.054 |
| Primary care integration | 0.098 | 0.492 | 0.622 |

After false discovery rate correction, the associations involving outpatient
treatment and suicide-related services remained statistically significant
at q < 0.05.


## Sensitivity Analysis Excluding the District of Columbia

Because the District of Columbia had substantially higher psychiatrist
supply than other jurisdictions, the correlation analysis was repeated
without DC.

The Spearman results included:

| Capability | Spearman rho | p-value | FDR q-value |
|---|---:|---:|---:|
| Outpatient treatment | -0.432 | 0.002 | 0.014 |
| Suicide-related services | -0.335 | 0.017 | 0.040 |
| SMI / co-occurring substance use services | -0.390 | 0.005 | 0.018 |

These three associations remained statistically significant after FDR
correction in the sensitivity analysis.

The negative direction of these ecological associations should not be
interpreted as evidence that psychiatrist supply reduces facility
capability. They may reflect differences in state health-system structure,
facility organization, service specialization, population characteristics,
or other unmeasured factors.


## Multivariable Suicide-Service Model

An exploratory state-level regression examined suicide-related service
capability while simultaneously including:

- psychiatrists per 100,000 population
- state poverty rate
- median household income

HC3 heteroskedasticity-robust standard errors were used.


### All 51 Jurisdictions

The psychiatrist-supply coefficient was:

**-0.292 percentage points**

with:

- robust SE = 0.335
- p = 0.383
- 95% CI = -0.948 to 0.364

Model R-squared was:

**0.195**


### Excluding the District of Columbia

The psychiatrist-supply coefficient was:

**-0.297 percentage points**

with:

- robust SE = 0.373
- p = 0.426
- 95% CI = -1.028 to 0.434

Model R-squared was:

**0.165**

The adjusted psychiatrist-supply association was therefore imprecisely
estimated in both specifications.

The similarity of the estimates with and without DC suggests that the
adjusted result was not driven solely by the District of Columbia.


## Medicaid Population-Relative Capacity

CMS December 2024 updated enrollment data were used to calculate the number
of Medicaid-accepting mental health treatment facilities per 100,000
Medicaid enrollees.

Across states with usable enrollment denominators, the median values were:

- **90.0%** of mental health facilities accepting Medicaid
- **20.65 Medicaid-accepting facilities per 100,000 Medicaid enrollees**

These measures describe different dimensions of the behavioral health
system.


## Arizona Medicaid Population-Relative Capacity

Arizona had:

- 1,778,734 Medicaid enrollees
- 528 mental health treatment facilities
- 466 Medicaid-accepting mental health facilities
- 88.3% Medicaid participation
- 29.68 total mental health facilities per 100,000 Medicaid enrollees
- 26.20 Medicaid-accepting mental health facilities per 100,000 Medicaid
  enrollees

Arizona therefore had a Medicaid participation percentage slightly below
the state median while its population-relative number of Medicaid-accepting
facilities was above the state median.

This illustrates why Medicaid participation percentage alone does not fully
describe behavioral health infrastructure.


## Participation Versus Capacity

Some states with high Medicaid participation percentages had relatively
different numbers of facilities available per Medicaid-enrolled population.

For example:

- Wyoming had 100.0% facility Medicaid participation and approximately
  87.81 Medicaid-accepting facilities per 100,000 Medicaid enrollees.

- California had 51.5% facility Medicaid participation and approximately
  5.15 Medicaid-accepting facilities per 100,000 Medicaid enrollees.

These values should not be interpreted as direct rankings of patient access.

Facility counts do not capture:

- facility size
- treatment slots
- staffing levels
- appointment availability
- geographic travel distance
- telehealth availability
- service quality
- patient utilization
- differences in clinical need


## Main Interpretation

The project demonstrates that Medicaid behavioral health infrastructure is
multidimensional.

A state may have a high percentage of mental health facilities accepting
Medicaid while still having relatively few Medicaid-accepting facilities
compared with the size of its Medicaid-enrolled population.

Conversely, Medicaid participation percentages alone cannot determine
whether patients have adequate real-world access to behavioral health care.

The findings support using both facility participation and
population-relative infrastructure measures when describing state Medicaid
behavioral health systems.