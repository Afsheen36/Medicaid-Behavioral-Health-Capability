# Reproducibility

## Project Workflow

The analysis is organized as a reproducible Python workflow.

The major stages are:

1. Inspect source datasets.
2. Construct the N-SUMHSS mental health analytic cohort.
3. Estimate state Medicaid participation and facility capabilities.
4. Construct state psychiatrist workforce measures from AHRF.
5. Integrate N-SUMHSS and AHRF state data.
6. Retrieve ACS socioeconomic measures through the Census Data API.
7. Integrate ACS socioeconomic context.
8. Retrieve and clean CMS Medicaid enrollment data.
9. Construct population-relative Medicaid behavioral health capacity
   measures.
10. Conduct correlation, sensitivity, multiple-testing, and exploratory
    multivariable analyses.
11. Generate research tables and figures.


## Main Scripts

### Data Inspection

- `src/inspect_nsumhss.py`
- `src/inspect_ahrf.py`
- `src/inspect_directory.py`

### N-SUMHSS Analysis

- `src/analyze_nsumhss.py`

### AHRF Workforce Analysis

- `src/analyze_ahrf.py`

### State Integration

- `src/integrate_state_data.py`

### ACS Acquisition and Integration

- `src/fetch_acs.py`
- `src/integrate_acs.py`

### CMS Medicaid Enrollment

- `src/fetch_cms_enrollment.py`
- `src/integrate_cms.py`

### Statistical Analysis

- `src/analyze_integrated.py`
- `src/model_state_capability.py`

### Visualization

- `src/visualize_integrated.py`
- `src/visualize_medicaid_capacity.py`


## Environment Variables

The Census Data API requires an API key.

The key is stored locally in:

`.env`

using:

`CENSUS_API_KEY=...`

The `.env` file is excluded from version control and should never be
committed to the public repository.


## Generated Outputs

Research outputs are stored in:

- `results/figures/`
- `results/tables/`

Examples include:

- state Medicaid acceptance estimates
- Arizona capability comparisons
- psychiatrist-supply correlation results
- sensitivity analyses
- multivariable model results
- Medicaid population-relative capacity estimates
- presentation-quality figures


## Data Management

Large or source datasets are not intended to be committed directly to the
repository when licensing, size, or reproducibility considerations make
that inappropriate.

The repository emphasizes reproducible scripts, documentation, selected
derived tables, and figures.


## Software

The workflow is implemented primarily in Python using packages including:

- pandas
- matplotlib
- scipy
- statsmodels
- requests
- python-dotenv
- openpyxl

Exact package versions should be captured in a project requirements file
before final release.


## Reproducing the Analysis

A final reproducibility workflow should:

1. Obtain the required source datasets.
2. Place source files in the documented raw-data locations.
3. Configure the Census API key in `.env`.
4. Install Python dependencies.
5. Run inspection and processing scripts.
6. Run state integration scripts.
7. Run statistical analyses.
8. Generate figures and tables.

The repository README provides the high-level project description, while
the methodology, results, limitations, and reproducibility documents
provide detailed research documentation.Re