from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INTEGRATED_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024.csv"
)

ACS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "acs_state_context_2024.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 2. Load datasets
# --------------------------------------------------

integrated = pd.read_csv(
    INTEGRATED_PATH
)

acs = pd.read_csv(
    ACS_PATH
)

print("ACS INTEGRATION")
print("-" * 50)

print(
    f"Existing integrated states: "
    f"{len(integrated)}"
)

print(
    f"ACS state records: "
    f"{len(acs)}"
)


# --------------------------------------------------
# 3. Restrict ACS to primary U.S. geography
# --------------------------------------------------

acs_us = acs[
    ~acs["state_fips"].isin([72])
].copy()

print(
    f"ACS records retained: "
    f"{len(acs_us)}"
)


# --------------------------------------------------
# 4. Merge on state FIPS
# --------------------------------------------------

analysis_df = integrated.merge(
    acs_us,
    on="state_fips",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# 5. Merge quality control
# --------------------------------------------------

print("\nMERGE QUALITY CONTROL")
print("-" * 50)

print(
    f"Integrated rows: "
    f"{len(analysis_df)}"
)

print(
    f"Missing ACS population: "
    f"{analysis_df['total_population'].isna().sum()}"
)

print(
    f"Missing poverty rate: "
    f"{analysis_df['poverty_rate'].isna().sum()}"
)

print(
    f"Missing median income: "
    f"{analysis_df['median_household_income'].isna().sum()}"
)

print(
    f"Duplicate state FIPS: "
    f"{analysis_df['state_fips'].duplicated().sum()}"
)


# --------------------------------------------------
# 6. Inspect final integrated dataset
# --------------------------------------------------

print("\nFINAL MULTI-SOURCE STATE DATASET")
print("-" * 70)

print(
    analysis_df[
        [
            "LOCATIONSTATE",
            "medicaid_acceptance_pct",
            "psychiatrists_per_100k",
            "poverty_rate",
            "median_household_income"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 7. Save
# --------------------------------------------------

OUTPUT_PATH = (
    OUTPUT_DIR
    / "integrated_state_2024_acs.csv"
)

analysis_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nIntegrated ACS dataset saved to:")
print(OUTPUT_PATH)
