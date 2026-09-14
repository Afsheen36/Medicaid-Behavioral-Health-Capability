from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "nsumhss_mh_2024.csv"

# Load analysis-ready mental-health facility dataset
df = pd.read_csv(DATA_PATH, low_memory=False)

print("N-SUMHSS MENTAL HEALTH ANALYSIS")
print("-" * 40)
print(f"Facilities: {len(df):,}")
print(f"Variables: {df.shape[1]}")
print("\nStates/locations represented:")
print(df["LOCATIONSTATE"].nunique())

# Calculate Medicaid acceptance by state/location
state_summary = (
    df.groupby("LOCATIONSTATE")
    .agg(
        total_mh_facilities=("MPRID", "count"),
        medicaid_facilities=("REVCHK5_MH", lambda x: (x == 1).sum())
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