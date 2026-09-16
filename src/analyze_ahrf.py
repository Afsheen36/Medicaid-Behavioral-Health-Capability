from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

AHRF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "NCHWA-2024-2025+AHRF+COUNTY+CSV"
    / "AHRF2025hp.csv"
)


# --------------------------------------------------
# 2. Load AHRF health-professions data
# --------------------------------------------------

df = pd.read_csv(
    AHRF_PATH,
    low_memory=False
)


print("AHRF PSYCHIATRIST SUPPLY ANALYSIS")
print("-" * 50)

print(f"County records: {len(df):,}")


# --------------------------------------------------
# 3. Select psychiatrist workforce variable
# --------------------------------------------------

psychiatrist = df[
    [
        "fips_st_cnty",
        "cnty_name_st_abbrev",
        "tot_md_do_psych_23"
    ]
].copy()


# --------------------------------------------------
# 4. Create state FIPS
# --------------------------------------------------

# Preserve the five-digit county FIPS code
psychiatrist["county_fips"] = (
    pd.to_numeric(
        psychiatrist["fips_st_cnty"],
        errors="coerce"
    )
    .astype("Int64")
    .astype(str)
    .str.zfill(5)
)

# First two digits identify the state
psychiatrist["state_fips"] = (
    psychiatrist["county_fips"].str[:2]
)


# --------------------------------------------------
# 5. Aggregate county psychiatrist counts
# --------------------------------------------------

state_psych = (
    psychiatrist
    .groupby("state_fips", as_index=False)
    .agg(
        county_records=("fips_st_cnty", "count"),
        psychiatrists=("tot_md_do_psych_23", "sum")
    )
)


state_psych["psychiatrists"] = (
    pd.to_numeric(
        state_psych["psychiatrists"],
        errors="coerce"
    )
)


# --------------------------------------------------
# 6. Inspect result
# --------------------------------------------------

print("\nSTATE-LEVEL PSYCHIATRIST SUPPLY")
print("-" * 50)

print(
    state_psych
    .sort_values("state_fips")
    .to_string(index=False)
)


print("\nMissing psychiatrist totals:")
print(
    state_psych["psychiatrists"].isna().sum()
)

# --------------------------------------------------
# 7. Load 2023 county population
# --------------------------------------------------

POP_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "NCHWA-2024-2025+AHRF+COUNTY+CSV"
    / "AHRF2025pop.csv"
)

pop_df = pd.read_csv(
    POP_PATH,
    low_memory=False
)

population = pop_df[
    [
        "fips_st_cnty",
        "popn_est_23"
    ]
].copy()


# Preserve five-digit county FIPS
population["county_fips"] = (
    pd.to_numeric(
        population["fips_st_cnty"],
        errors="coerce"
    )
    .astype("Int64")
    .astype(str)
    .str.zfill(5)
)

population["state_fips"] = (
    population["county_fips"].str[:2]
)


# --------------------------------------------------
# 8. Aggregate population to state
# --------------------------------------------------

state_population = (
    population
    .groupby("state_fips", as_index=False)
    .agg(
        population_2023=("popn_est_23", "sum")
    )
)


# --------------------------------------------------
# 9. Merge psychiatrist supply and population
# --------------------------------------------------

state_workforce = state_psych.merge(
    state_population,
    on="state_fips",
    how="left"
)

state_workforce["psychiatrists_per_100k"] = (
    state_workforce["psychiatrists"]
    / state_workforce["population_2023"]
    * 100000
).round(2)


print("\nSTATE PSYCHIATRIST SUPPLY PER 100,000")
print("-" * 60)

print(
    state_workforce[
        [
            "state_fips",
            "psychiatrists",
            "population_2023",
            "psychiatrists_per_100k"
        ]
    ].to_string(index=False)
)
# --------------------------------------------------
# 10. Create state FIPS to abbreviation mapping
# --------------------------------------------------

fips_mapping = (
    psychiatrist[
        ["state_fips", "cnty_name_st_abbrev"]
    ]
    .drop_duplicates()
)

fips_mapping["state"] = (
    fips_mapping["cnty_name_st_abbrev"]
    .str.extract(r",\s*([A-Z]{2})$")
)

fips_mapping = (
    fips_mapping[
        ["state_fips", "state"]
    ]
    .dropna()
    .drop_duplicates()
    .sort_values("state_fips")
)

print("\nSTATE FIPS MAPPING")
print("-" * 40)

print(
    fips_mapping.to_string(index=False)
)

# --------------------------------------------------
# 11. Create final U.S. state workforce table
# --------------------------------------------------

us_state_fips = set(
    fips_mapping.loc[
        fips_mapping["state"].notna(),
        "state_fips"
    ]
) - {"66", "72", "78"}

us_state_fips.add("11")  # District of Columbia

state_workforce_clean = (
    state_workforce[
        state_workforce["state_fips"].isin(us_state_fips)
    ]
    .merge(
        fips_mapping,
        on="state_fips",
        how="left"
    )
)

state_workforce_clean = state_workforce_clean[
    [
        "state",
        "state_fips",
        "psychiatrists",
        "population_2023",
        "psychiatrists_per_100k"
    ]
].sort_values("state")

print("\nFINAL U.S. STATE WORKFORCE TABLE")
print("-" * 60)

print(
    state_workforce_clean.to_string(index=False)
)

print(
    f"\nStates/jurisdictions: "
    f"{state_workforce_clean['state'].nunique()}"
)

# --------------------------------------------------
# 12. Save processed state workforce table
# --------------------------------------------------

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = (
    PROCESSED_DIR
    / "ahrf_state_psychiatrist_2023.csv"
)

state_workforce_clean.to_csv(
    OUTPUT_PATH,
    index=False
)

print(f"\nSaved AHRF state workforce table to:")
print(OUTPUT_PATH)