from pathlib import Path
import pandas as pd

# Locate the project and raw N-SUMHSS dataset
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "NSUMHSS_2024_PUF_CSV.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH, low_memory=False)

print("N-SUMHSS 2024 DATA INSPECTION")
print("-" * 40)

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]:,}")

print("\nFirst 10 column names:")
print(df.columns[:10].tolist())


# Search for variables relevant to our research question
search_terms = [
    "MENTAL",
    "REVCHK5",
    "SETTING",
    "SUICIDE",
    "PRIMARY",
    "SMISED",
    "TELE"
]

print("\nRELEVANT VARIABLE SEARCH")
print("-" * 40)

for term in search_terms:
    matches = [col for col in df.columns if term in col.upper()]

    print(f"\n{term}:")

    for variable in matches:
        print(f"  {variable}")


# Inspect coding of key research variables
key_variables = [
    "MENTALHTHSERV",
    "REVCHK5_MH",
    "SETTINGIP",
    "SETTINGRC",
    "SETTINGDTPH",
    "SETTINGOP",
    "MHSUICIDE",
    "PRIMARYCARE",
    "SMISEDSUD_MH"
]

print("\nKEY VARIABLE VALUES")
print("-" * 40)

for variable in key_variables:
    print(f"\n{variable}")
    print(df[variable].value_counts(dropna=False).sort_index())
# Create initial mental-health facility cohort
mh_df = df[df["MENTALHTHSERV"] == "1"].copy()

print("\nMENTAL HEALTH ANALYTIC COHORT")
print("-" * 40)
print(f"All N-SUMHSS facilities: {len(df):,}")
print(f"Mental-health facilities: {len(mh_df):,}")

print("\nMedicaid acceptance within mental-health facilities:")
print(mh_df["REVCHK5_MH"].value_counts(dropna=False).sort_index())

# Compare selected service capabilities by Medicaid acceptance
capability_variables = [
    "SETTINGIP",
    "SETTINGRC",
    "SETTINGDTPH",
    "SETTINGOP",
    "MHSUICIDE",
    "PRIMARYCARE",
    "SMISEDSUD_MH"
]

print("\nSERVICE CAPABILITY BY MEDICAID ACCEPTANCE")
print("-" * 50)

for variable in capability_variables:
    comparison = pd.crosstab(
        mh_df["REVCHK5_MH"],
        mh_df[variable],
        normalize="index"
    ) * 100

    print(f"\n{variable}")
    print(comparison.round(1))

# Create analysis-ready subset for Project 1
analysis_variables = [
    "MPRID",
    "LOCATIONSTATE",
    "REVCHK5_MH",
    "SETTINGOP",
    "SETTINGDTPH",
    "SETTINGRC",
    "SETTINGIP",
    "SMISEDSUD_MH",
    "MHSUICIDE",
    "PRIMARYCARE"
]

analysis_df = mh_df[analysis_variables].copy()

print("\nANALYSIS DATASET")
print("-" * 40)
print(f"Rows: {analysis_df.shape[0]:,}")
print(f"Columns: {analysis_df.shape[1]}")
print("\nVariables:")
for column in analysis_df.columns:
    print(f"  {column}")

# Save analysis-ready N-SUMHSS subset
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = PROCESSED_DIR / "nsumhss_mh_2024.csv"

analysis_df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved analysis dataset to:")
print(OUTPUT_PATH)

# --------------------------------------------------
# Search for geographic variables
# --------------------------------------------------

geo_terms = [
    "COUNTY",
    "FIPS",
    "ZIP",
    "CITY",
    "STATE",
    "REGION",
    "METRO",
    "RURAL",
    "URBAN"
]

print("\nGEOGRAPHIC VARIABLE SEARCH")
print("-" * 50)

for term in geo_terms:
    matches = [
        column
        for column in df.columns
        if term in column.upper()
    ]

    print(f"\n{term}: {len(matches)} matches")

    for column in matches:
        print(f"  {column}")