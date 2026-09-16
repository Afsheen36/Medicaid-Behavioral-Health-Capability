import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Project paths and data loading
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nsumhss_mh_2024.csv"
)

df = pd.read_csv(DATA_PATH, low_memory=False)


# --------------------------------------------------
# 2. Basic dataset inspection
# --------------------------------------------------

print("N-SUMHSS MENTAL HEALTH ANALYSIS")
print("-" * 40)

print(f"Facilities: {len(df):,}")
print(f"Variables: {df.shape[1]}")

print("\nStates/locations represented:")
print(df["LOCATIONSTATE"].nunique())


# --------------------------------------------------
# 3. Medicaid acceptance by state/location
# --------------------------------------------------

state_summary = (
    df.groupby("LOCATIONSTATE")
    .agg(
        total_mh_facilities=("MPRID", "count"),
        medicaid_facilities=(
            "REVCHK5_MH",
            lambda x: (x == 1).sum()
        )
    )
)

state_summary["medicaid_acceptance_pct"] = (
    state_summary["medicaid_facilities"]
    / state_summary["total_mh_facilities"]
    * 100
)

state_summary = state_summary.sort_values(
    "medicaid_acceptance_pct",
    ascending=False
)

print("\nMEDICAID ACCEPTANCE BY STATE/LOCATION")
print("-" * 50)

print(state_summary.round(1))


# --------------------------------------------------
# 4. Geographic quality control
# --------------------------------------------------

print("\nGEOGRAPHIC QUALITY CONTROL")
print("-" * 40)

location_counts = (
    df["LOCATIONSTATE"]
    .value_counts()
    .sort_index()
)

print(location_counts)


# --------------------------------------------------
# 5. Primary U.S. analytic geography
# --------------------------------------------------

excluded_locations = ["PR", "ZZ"]

us_df = df[
    ~df["LOCATIONSTATE"].isin(excluded_locations)
].copy()

print("\nPRIMARY U.S. ANALYTIC GEOGRAPHY")
print("-" * 40)

print(f"Facilities retained: {len(us_df):,}")
print(
    f"Jurisdictions retained: "
    f"{us_df['LOCATIONSTATE'].nunique()}"
)
print(f"Excluded locations: {excluded_locations}")


# --------------------------------------------------
# 6. Figure 1: Medicaid acceptance by state
# --------------------------------------------------

state_plot = (
    us_df.groupby("LOCATIONSTATE")
    .agg(
        total_facilities=("MPRID", "count"),
        medicaid_facilities=(
            "REVCHK5_MH",
            lambda x: (x == 1).sum()
        )
    )
)

state_plot["medicaid_pct"] = (
    state_plot["medicaid_facilities"]
    / state_plot["total_facilities"]
    * 100
)

state_plot = state_plot.sort_values("medicaid_pct")


# Create results directory
RESULTS_DIR = PROJECT_ROOT / "results" / "figures"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Create Figure 1
fig, ax = plt.subplots(figsize=(12, 14))

ax.barh(
    state_plot.index,
    state_plot["medicaid_pct"]
)

ax.set_xlabel(
    "Mental health facilities accepting Medicaid (%)"
)

ax.set_ylabel("State")

ax.set_title(
    "Share of Mental Health Treatment Facilities "
    "Accepting Medicaid, 2024"
)

ax.set_xlim(0, 100)

ax.grid(
    axis="x",
    alpha=0.25
)

plt.tight_layout()

OUTPUT_FIGURE = (
    RESULTS_DIR
    / "medicaid_acceptance_by_state.png"
)

plt.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"\nFigure saved to: {OUTPUT_FIGURE}"
)


# --------------------------------------------------
# 7. Medicaid-accepting facility cohort
# --------------------------------------------------

medicaid_df = us_df[
    us_df["REVCHK5_MH"] == 1
].copy()

print("\nMEDICAID-ACCEPTING FACILITIES")
print("-" * 40)

print(f"Facilities: {len(medicaid_df):,}")


# --------------------------------------------------
# 8. Capability variables
# --------------------------------------------------

capability_vars = [
    "SETTINGOP",
    "SETTINGDTPH",
    "SETTINGRC",
    "SETTINGIP",
    "MHSUICIDE",
    "SMISEDSUD_MH",
    "PRIMARYCARE"
]


# Convert capability variables to numeric
# 0 = No, 1 = Yes
# Other values become missing
for variable in capability_vars:
    medicaid_df[variable] = pd.to_numeric(
        medicaid_df[variable],
        errors="coerce"
    )


# --------------------------------------------------
# 9. State-level capability with 95% CI
# --------------------------------------------------

def wilson_interval(successes, total, z=1.96):
    """Calculate a 95% Wilson confidence interval."""
    if total == 0:
        return float("nan"), float("nan")

    p = successes / total

    denominator = 1 + (z ** 2 / total)

    center = (
        p + (z ** 2 / (2 * total))
    ) / denominator

    margin = (
        z
        * (
            (p * (1 - p) / total)
            + (z ** 2 / (4 * total ** 2))
        ) ** 0.5
        / denominator
    )

    return center - margin, center + margin


capability_results = []

for state, group in medicaid_df.groupby("LOCATIONSTATE"):

    for variable in capability_vars:

        valid = group[variable].dropna()

        n_total = len(valid)
        n_yes = (valid == 1).sum()

        percentage = (
            n_yes / n_total * 100
            if n_total > 0
            else float("nan")
        )

        ci_low, ci_high = wilson_interval(
            n_yes,
            n_total
        )

        capability_results.append({
            "state": state,
            "capability": variable,
            "n_yes": n_yes,
            "n_total": n_total,
            "percentage": percentage,
            "ci_low": ci_low * 100,
            "ci_high": ci_high * 100
        })


state_capability_detail = pd.DataFrame(
    capability_results
)

state_capability_detail[
    ["percentage", "ci_low", "ci_high"]
] = state_capability_detail[
    ["percentage", "ci_low", "ci_high"]
].round(1)


print(
    "\nSTATE CAPABILITY WITH 95% CONFIDENCE INTERVALS"
)

print("-" * 70)

print(
    state_capability_detail.to_string(index=False)
)


# --------------------------------------------------
# 10. Arizona capability profile
# --------------------------------------------------

arizona_capability = state_capability_detail[
    state_capability_detail["state"] == "AZ"
].copy()

print("\nARIZONA CAPABILITY PROFILE")
print("-" * 50)

print(
    arizona_capability.to_string(index=False)
)

# --------------------------------------------------
# 11. Save research tables
# --------------------------------------------------

TABLES_DIR = PROJECT_ROOT / "results" / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)

state_table_path = TABLES_DIR / "state_capability_2024.csv"
arizona_table_path = TABLES_DIR / "arizona_capability_2024.csv"

state_capability_detail.to_csv(
    state_table_path,
    index=False
)

arizona_capability.to_csv(
    arizona_table_path,
    index=False
)

print("\nRESEARCH TABLES SAVED")
print("-" * 40)
print(state_table_path)
print(arizona_table_path)