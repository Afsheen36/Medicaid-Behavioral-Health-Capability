# Limitations

This project is an exploratory state-level analysis of Medicaid behavioral
health infrastructure. Several limitations should be considered when
interpreting the findings.

## Ecological Analysis

The primary unit of analysis is the state.

State-level associations cannot be interpreted as relationships at the
individual patient, clinician, or facility level. The results are therefore
descriptive and ecological rather than causal.

## Facility Counts Are Not Treatment Capacity

N-SUMHSS identifies treatment facilities and their reported service
characteristics.

A facility count does not measure:

- number of treatment slots
- number of clinicians
- clinician full-time equivalents
- appointment availability
- waiting times
- hours of operation
- patient volume
- treatment intensity
- service quality

Two facilities may therefore represent very different amounts of actual
treatment capacity.

## Medicaid Acceptance Does Not Equal Access

A facility reporting that it accepts Medicaid does not establish that every
Medicaid beneficiary can obtain timely treatment.

The analysis does not directly observe:

- whether the facility accepts new Medicaid patients
- appointment wait times
- managed-care network participation
- prior authorization requirements
- transportation barriers
- geographic distance
- language accessibility
- telehealth availability
- provider-level Medicaid participation
- patient out-of-pocket costs

For this reason, the project uses the term **behavioral health
infrastructure** rather than treating facility counts as a direct measure
of realized patient access.

## Population-Relative Capacity Measure

The measure:

**Medicaid-accepting mental health facilities per 100,000 Medicaid
enrollees**

provides a population-relative indicator of infrastructure.

It should not be interpreted as the number of facilities available to each
beneficiary or as a measure of service adequacy.

The denominator represents state Medicaid enrollment, while the numerator
counts treatment facilities rather than treatment slots or clinicians.

## Rhode Island CMS Enrollment

The December 2024 updated CMS extract used in this project reports zero
Medicaid enrollment for Rhode Island.

Because this value is not a plausible denominator for the intended
population-relative calculation, it was treated as unusable.

Rhode Island remains in analyses that do not require the CMS Medicaid
enrollment denominator but is excluded from denominator-based capacity
measures.

## Differences in Data Years

The integrated dataset combines measures from multiple sources and
reference periods:

- N-SUMHSS facility characteristics: 2024
- AHRF psychiatrist workforce measures: primarily 2023
- ACS socioeconomic context: 2024 5-year estimates
- CMS Medicaid enrollment: December 2024 updated data

These measures provide approximately aligned state context but should not
be interpreted as perfectly contemporaneous observations.

## Psychiatrist Supply

Psychiatrist supply is measured at the state level using AHRF data.

The measure does not establish:

- whether psychiatrists accept Medicaid
- whether they practice in mental health treatment facilities
- their clinical workload
- their geographic distribution within a state
- their availability to new patients
- whether they primarily serve children or adults

Consequently, psychiatrist supply should be interpreted as a broad
workforce-context measure.

## Socioeconomic Measures

ACS poverty and median household income measures describe state-level
socioeconomic context.

They do not represent the socioeconomic characteristics of individual
Medicaid beneficiaries or patients using the facilities in N-SUMHSS.

## Cross-Sectional Design

The project primarily compares states during a single general time period.

The analysis therefore cannot determine whether changes in workforce,
Medicaid enrollment, or socioeconomic conditions caused subsequent changes
in facility participation or capability.

Longitudinal data would be required to examine temporal relationships more
rigorously.

## Statistical Power and Multiple Testing

The state-level analytic sample contains only 51 jurisdictions.

This limits statistical power for multivariable modeling, particularly
when several correlated state characteristics are included simultaneously.

False discovery rate correction was used for the primary set of Spearman
correlations to reduce the risk of interpreting chance findings from
multiple comparisons.

## Unmeasured State Characteristics

Observed state differences may reflect factors not directly measured in
this project, including:

- Medicaid reimbursement policy
- managed-care penetration
- Medicaid expansion history
- behavioral health carve-outs
- state licensing rules
- rurality
- hospital and community mental health infrastructure
- state behavioral health funding
- provider market structure
- scope-of-practice regulations

The observed associations should therefore not be interpreted as isolated
effects of psychiatrist supply, poverty, income, or Medicaid enrollment.

## General Interpretation

The project is designed to characterize variation, integrate multiple
public health data sources, and generate reproducible state-level measures.

Its findings are most appropriately interpreted as descriptive and
hypothesis-generating.

They are not estimates of causal effects and should not be used alone to
judge the adequacy or quality of a state's Medicaid behavioral health
system.