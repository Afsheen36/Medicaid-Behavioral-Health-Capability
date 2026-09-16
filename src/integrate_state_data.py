from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

NSUMHSS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nsumhss_mh_2024.csv"
)

AHRF_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ahrf_state_psychiatrist_2023.csv"
)


# --------------------------------------------------
# 2. Load processed datasets
# --------------------------------------------------

nsumhss = pd.read_csv(
    NSUMHSS_PATH,
    low_memory=False
)

ahrf = pd.read_csv(
    AHRF_PATH
)

print("STATE DATA INTEGRATION")
print("-" * 50)

print(f"N-SUMHSS facility records: {len(nsumhss):,}")
print(f"AHRF state records: {len(ahrf):,}")


# --------------------------------------------------
# 3. Restrict N-SUMHSS to primary geography
# --------------------------------------------------

nsumhss = nsumhss[
    ~nsumhss["LOCATIONSTATE"].isin(["PR", "ZZ"])
].copy()

print(
    f"N-SUMHSS jurisdictions: "
    f"{nsumhss['LOCATIONSTATE'].nunique()}"
)


# --------------------------------------------------
# 4. Create state-level N-SUMHSS summary
# --------------------------------------------------

state_nsumhss = (
    nsumhss
    .groupby("LOCATIONSTATE")
    .agg(
        total_mh_facilities=("MPRID", "count"),
        medicaid_facilities=(
            "REVCHK5_MH",
            lambda x: (x == 1).sum()
        )
    )
    .reset_index()
)

state_nsumhss["medicaid_acceptance_pct"] = (
    state_nsumhss["medicaid_facilities"]
    / state_nsumhss["total_mh_facilities"]
    * 100
).round(1)


# --------------------------------------------------
# 5. Merge N-SUMHSS and AHRF
# --------------------------------------------------

integrated = state_nsumhss.merge(
    ahrf,
    left_on="LOCATIONSTATE",
    right_on="state",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# 6. Merge quality control
# --------------------------------------------------

print("\nMERGE QUALITY CONTROL")
print("-" * 50)

print(f"Integrated rows: {len(integrated)}")

print(
    "States missing AHRF match:",
    integrated["psychiatrists_per_100k"].isna().sum()
)

if integrated["psychiatrists_per_100k"].isna().any():
    print("\nUnmatched states:")
    print(
        integrated.loc[
            integrated["psychiatrists_per_100k"].isna(),
            "LOCATIONSTATE"
        ].tolist()
    )


# --------------------------------------------------
# 7. Inspect integrated state dataset
# --------------------------------------------------

print("\nINTEGRATED STATE DATA")
print("-" * 50)

print(
    integrated[
        [
            "LOCATIONSTATE",
            "total_mh_facilities",
            "medicaid_facilities",
            "medicaid_acceptance_pct",
            "psychiatrists",
            "population_2023",
            "psychiatrists_per_100k"
        ]
    ].to_string(index=False)
)


# --------------------------------------------------
# 8. Save integrated dataset
# --------------------------------------------------

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024.csv"
)

integrated.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nIntegrated dataset saved to:")
print(OUTPUT_PATH)