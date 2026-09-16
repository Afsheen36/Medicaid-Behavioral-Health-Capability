from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024_acs.csv"
)

CMS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cms_medicaid_enrollment_dec2024.csv"
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

state_df = pd.read_csv(
    STATE_PATH
)

cms = pd.read_csv(
    CMS_PATH
)

print("CMS + BEHAVIORAL HEALTH INTEGRATION")
print("-" * 60)

print(
    f"Existing state records: {len(state_df)}"
)

print(
    f"CMS records: {len(cms)}"
)


# --------------------------------------------------
# 3. Prepare CMS data
# --------------------------------------------------

cms_merge = cms[
    [
        "state",
        "medicaid_enrollment",
        "chip_enrollment",
        "medicaid_chip_enrollment",
        "enrollment_qc_flag",
    ]
].copy()

# Rename CMS state key to match the existing dataset.
cms_merge = cms_merge.rename(
    columns={
        "state": "LOCATIONSTATE"
    }
)

# Standardize state abbreviations.
state_df["LOCATIONSTATE"] = (
    state_df["LOCATIONSTATE"]
    .astype(str)
    .str.strip()
    .str.upper()
)

cms_merge["LOCATIONSTATE"] = (
    cms_merge["LOCATIONSTATE"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# --------------------------------------------------
# 4. Merge CMS enrollment
# --------------------------------------------------

integrated = state_df.merge(
    cms_merge,
    on="LOCATIONSTATE",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# 5. Merge quality control
# --------------------------------------------------

print("\nMERGE QUALITY CONTROL")
print("-" * 60)

print(
    f"Integrated rows: {len(integrated)}"
)

print(
    f"Missing CMS matches: "
    f"{integrated['medicaid_enrollment'].isna().sum()}"
)

print(
    f"Missing/invalid Medicaid enrollment: "
    f"{integrated['medicaid_enrollment'].isna().sum()}"
)

if integrated["medicaid_enrollment"].isna().any():

    print(
        "\nStates without usable "
        "Medicaid denominator:"
    )

    print(
        integrated.loc[
            integrated["medicaid_enrollment"].isna(),
            "LOCATIONSTATE"
        ].tolist()
    )


# --------------------------------------------------
# 6. Calculate Medicaid behavioral-health capacity
# --------------------------------------------------

integrated[
    "mh_facilities_per_100k_medicaid"
] = (
    integrated["total_mh_facilities"]
    / integrated["medicaid_enrollment"]
    * 100000
)

integrated[
    "medicaid_accepting_mh_facilities_per_100k_medicaid"
] = (
    integrated["medicaid_facilities"]
    / integrated["medicaid_enrollment"]
    * 100000
)


# --------------------------------------------------
# 7. Protect against invalid calculations
# --------------------------------------------------

invalid_enrollment = (
    integrated["medicaid_enrollment"].isna()
    | (integrated["medicaid_enrollment"] <= 0)
)

integrated.loc[
    invalid_enrollment,
    [
        "mh_facilities_per_100k_medicaid",
        "medicaid_accepting_mh_facilities_per_100k_medicaid",
    ]
] = pd.NA


# --------------------------------------------------
# 8. Round derived measures
# --------------------------------------------------

integrated[
    "mh_facilities_per_100k_medicaid"
] = integrated[
    "mh_facilities_per_100k_medicaid"
].round(2)

integrated[
    "medicaid_accepting_mh_facilities_per_100k_medicaid"
] = integrated[
    "medicaid_accepting_mh_facilities_per_100k_medicaid"
].round(2)


# --------------------------------------------------
# 9. Create presentation table
# --------------------------------------------------

capacity_columns = [
    "LOCATIONSTATE",
    "medicaid_enrollment",
    "total_mh_facilities",
    "medicaid_facilities",
    "medicaid_acceptance_pct",
    "mh_facilities_per_100k_medicaid",
    "medicaid_accepting_mh_facilities_per_100k_medicaid",
]

capacity_table = integrated[
    capacity_columns
].sort_values(
    "medicaid_accepting_mh_facilities_per_100k_medicaid",
    ascending=False,
    na_position="last"
)


# --------------------------------------------------
# 10. Display results
# --------------------------------------------------

print("\nMEDICAID BEHAVIORAL HEALTH CAPACITY")
print("-" * 90)

print(
    capacity_table.to_string(index=False)
)


# --------------------------------------------------
# 11. Arizona benchmark
# --------------------------------------------------

print("\nARIZONA MEDICAID CAPACITY")
print("-" * 60)

print(
    capacity_table.loc[
        capacity_table["LOCATIONSTATE"] == "AZ"
    ].to_string(index=False)
)


# --------------------------------------------------
# 12. Save final integrated dataset
# --------------------------------------------------

OUTPUT_PATH = (
    OUTPUT_DIR
    / "integrated_state_2024_full.csv"
)

integrated.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# 13. Save presentation table
# --------------------------------------------------

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "tables"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CAPACITY_PATH = (
    RESULTS_DIR
    / "medicaid_behavioral_health_capacity_2024.csv"
)

capacity_table.to_csv(
    CAPACITY_PATH,
    index=False
)


# --------------------------------------------------
# 14. Final confirmation
# --------------------------------------------------

print("\nFINAL DATASETS SAVED")
print("-" * 60)

print(OUTPUT_PATH)
print(CAPACITY_PATH)