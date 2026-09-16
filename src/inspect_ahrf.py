from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

AHRF_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "NCHWA-2024-2025+AHRF+COUNTY+CSV"
)


# --------------------------------------------------
# 2. Find available AHRF files
# --------------------------------------------------

csv_files = list(AHRF_DIR.glob("*.csv"))

print("AHRF FILE INSPECTION")
print("-" * 40)

print(f"CSV files found: {len(csv_files)}")

for file in csv_files:
    print(f"  {file.name}")


# --------------------------------------------------
# 3. Load Health Professions file
# --------------------------------------------------

HP_PATH = AHRF_DIR / "AHRF2025hp.csv"

hp_df = pd.read_csv(
    HP_PATH,
    low_memory=False
)

print("\nAHRF HEALTH PROFESSIONS FILE")
print("-" * 40)

print(f"Rows: {hp_df.shape[0]:,}")
print(f"Columns: {hp_df.shape[1]:,}")


# --------------------------------------------------
# 4. Search AHRF variable names using abbreviations
# --------------------------------------------------

search_terms = [
    "psy",
    "psych",
    "soc",
    "sw",
    "mh",
    "mental",
    "behav",
    "sub"
]

print("\nAHRF VARIABLE SEARCH")
print("-" * 50)

for term in search_terms:

    matches = [
        column
        for column in hp_df.columns
        if term in column.lower()
    ]

    print(f"\n{term}: {len(matches)} matches")

    for column in matches[:40]:
        print(f"  {column}")

# Show all psychiatrist-related variables
psy_vars = [
    column
    for column in hp_df.columns
    if "psych" in column.lower()
]

print("\nPSYCHIATRIST VARIABLES")
print("-" * 50)

for column in psy_vars:
    print(column)

# --------------------------------------------------
# 5. Search likely behavioral-health workforce fields
# --------------------------------------------------

profession_terms = [
    "psych",
    "social",
    "work"
]

print("\nPOTENTIAL BEHAVIORAL-HEALTH WORKFORCE VARIABLES")
print("-" * 60)

for term in profession_terms:
    matches = [
        column
        for column in hp_df.columns
        if term in column.lower()
    ]

    print(f"\n{term}: {len(matches)} matches")

    for column in matches[:50]:
        print(f"  {column}")

# --------------------------------------------------
# 6. Inspect selected psychiatrist workforce variable
# --------------------------------------------------

selected_vars = [
    "fips_st_cnty",
    "cnty_name_st_abbrev",
    "md_nf_psych_23",
    "do_nf_psych_23",
    "tot_md_do_psych_23"
]

print("\nSELECTED PSYCHIATRIST VARIABLES")
print("-" * 60)

print(
    hp_df[selected_vars]
    .head(15)
    .to_string(index=False)
)

print("\nMissing values:")
print(hp_df[selected_vars].isna().sum())

# --------------------------------------------------
# 7. Inspect AHRF population file
# --------------------------------------------------

POP_PATH = (
    AHRF_DIR / "AHRF2025pop.csv"
)

pop_df = pd.read_csv(
    POP_PATH,
    low_memory=False
)

print("\nAHRF POPULATION FILE")
print("-" * 50)

print(f"Rows: {pop_df.shape[0]:,}")
print(f"Columns: {pop_df.shape[1]:,}")

print("\nPopulation-related variables:")

population_matches = [
    column
    for column in pop_df.columns
    if "pop" in column.lower()
]

for column in population_matches[:80]:
    print(f"  {column}")