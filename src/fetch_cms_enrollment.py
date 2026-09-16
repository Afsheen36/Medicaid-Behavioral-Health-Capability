from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 2. Official CMS dataset
# --------------------------------------------------

CMS_URL = (
    "https://download.medicaid.gov/data/"
    "pi-dataset-august-2026-release.csv"
)


print("CMS MEDICAID ENROLLMENT INSPECTION")
print("-" * 60)

print("Downloading official CMS Performance Indicator dataset...")


# --------------------------------------------------
# 3. Load CMS data
# --------------------------------------------------

cms = pd.read_csv(
    CMS_URL,
    low_memory=False
)

print(f"\nRows: {len(cms):,}")
print(f"Columns: {cms.shape[1]}")


# --------------------------------------------------
# 4. Inspect columns
# --------------------------------------------------

print("\nCOLUMN NAMES")
print("-" * 60)

for column in cms.columns:
    print(column)


# --------------------------------------------------
# 5. Inspect reporting periods
# --------------------------------------------------

print("\nREPORTING PERIOD RANGE")
print("-" * 60)

print(
    cms["Reporting Period"]
    .dropna()
    .sort_values()
    .unique()[-24:]
)


# --------------------------------------------------
# 6. Inspect December 2024 updated records
# --------------------------------------------------

dec_2024 = cms[
    (cms["Reporting Period"] == 202412)
    & (cms["Preliminary or Updated"] == "U")
].copy()


print("\nDECEMBER 2024 UPDATED DATA")
print("-" * 60)

print(f"Records: {len(dec_2024)}")


columns_to_show = [
    "State Abbreviation",
    "State Name",
    "Reporting Period",
    "Preliminary or Updated",
    "Total Medicaid and CHIP Enrollment",
    "Total Medicaid Enrollment",
    "Total CHIP Enrollment",
]


available_columns = [
    column
    for column in columns_to_show
    if column in dec_2024.columns
]


print(
    dec_2024[
        available_columns
    ].to_string(index=False)
)

# --------------------------------------------------
# 7. Create clean December 2024 Medicaid table
# --------------------------------------------------

cms_state = dec_2024[
    [
        "State Abbreviation",
        "State Name",
        "Total Medicaid Enrollment",
        "Total CHIP Enrollment",
        "Total Medicaid and CHIP Enrollment",
    ]
].copy()

cms_state = cms_state.rename(
    columns={
        "State Abbreviation": "state",
        "State Name": "state_name",
        "Total Medicaid Enrollment": "medicaid_enrollment",
        "Total CHIP Enrollment": "chip_enrollment",
        "Total Medicaid and CHIP Enrollment": "medicaid_chip_enrollment",
    }
)


# --------------------------------------------------
# 8. Convert enrollment fields to numeric
# --------------------------------------------------

enrollment_columns = [
    "medicaid_enrollment",
    "chip_enrollment",
    "medicaid_chip_enrollment",
]

for column in enrollment_columns:
    cms_state[column] = pd.to_numeric(
        cms_state[column],
        errors="coerce"
    )


# --------------------------------------------------
# 9. Flag nonpositive enrollment values
# --------------------------------------------------

cms_state["enrollment_qc_flag"] = (
    cms_state["medicaid_enrollment"] <= 0
)

print("\nCMS ENROLLMENT QUALITY CONTROL")
print("-" * 60)

print(
    f"State records: {len(cms_state)}"
)

print(
    f"Missing Medicaid enrollment: "
    f"{cms_state['medicaid_enrollment'].isna().sum()}"
)

print(
    f"Nonpositive Medicaid enrollment: "
    f"{cms_state['enrollment_qc_flag'].sum()}"
)

if cms_state["enrollment_qc_flag"].any():

    print("\nRecords requiring review:")

    print(
        cms_state.loc[
            cms_state["enrollment_qc_flag"],
            [
                "state",
                "state_name",
                "medicaid_enrollment",
                "chip_enrollment",
                "medicaid_chip_enrollment",
            ]
        ].to_string(index=False)
    )


# --------------------------------------------------
# 10. Replace invalid denominator values with missing
# --------------------------------------------------

cms_state.loc[
    cms_state["medicaid_enrollment"] <= 0,
    "medicaid_enrollment"
] = pd.NA


# --------------------------------------------------
# 11. Save processed CMS enrollment table
# --------------------------------------------------

OUTPUT_PATH = (
    PROCESSED_DIR
    / "cms_medicaid_enrollment_dec2024.csv"
)

cms_state.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nProcessed CMS enrollment table saved to:")
print(OUTPUT_PATH)