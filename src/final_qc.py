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

CAPACITY_PATH = (
    PROJECT_ROOT
    / "results"
    / "tables"
    / "medicaid_behavioral_health_capacity_2024.csv"
)


# --------------------------------------------------
# 2. Load data
# --------------------------------------------------

df = pd.read_csv(
    NSUMHSS_PATH,
    low_memory=False
)

capacity = pd.read_csv(
    CAPACITY_PATH
)


# --------------------------------------------------
# 3. Restrict to primary analytic geography
# --------------------------------------------------

df = df[
    ~df["LOCATIONSTATE"].isin(
        ["PR", "ZZ"]
    )
].copy()


# --------------------------------------------------
# 4. Mental-health facility counts
# --------------------------------------------------

print("FINAL PROJECT QC")
print("-" * 60)

print(
    f"Mental-health facilities in primary geography: "
    f"{len(df):,}"
)


# --------------------------------------------------
# 5. Medicaid analytic cohort
# --------------------------------------------------

medicaid = df[
    df["REVCHK5_MH"] == 1
].copy()

print(
    f"Medicaid-accepting mental-health facilities: "
    f"{len(medicaid):,}"
)

print(
    f"Overall Medicaid acceptance: "
    f"{len(medicaid) / len(df) * 100:.1f}%"
)


# --------------------------------------------------
# 6. National capability estimates
# --------------------------------------------------

capabilities = [
    "SETTINGOP",
    "SETTINGDTPH",
    "SETTINGRC",
    "SETTINGIP",
    "MHSUICIDE",
    "SMISEDSUD_MH",
    "PRIMARYCARE",
]

print("\nNATIONAL CAPABILITY PROFILE")
print("-" * 60)

for variable in capabilities:

    values = pd.to_numeric(
        medicaid[variable],
        errors="coerce"
    )

    valid = values.isin([0, 1])

    pct = (
        values.loc[valid].mean()
        * 100
    )

    print(
        f"{variable}: "
        f"{pct:.1f}% "
        f"(valid n={valid.sum():,})"
    )


# --------------------------------------------------
# 7. Arizona capability estimates
# --------------------------------------------------

az = medicaid[
    medicaid["LOCATIONSTATE"] == "AZ"
].copy()

print("\nARIZONA")
print("-" * 60)

print(
    f"Arizona Medicaid-accepting facilities: "
    f"{len(az):,}"
)

for variable in capabilities:

    values = pd.to_numeric(
        az[variable],
        errors="coerce"
    )

    valid = values.isin([0, 1])

    pct = (
        values.loc[valid].mean()
        * 100
    )

    print(
        f"{variable}: "
        f"{pct:.1f}% "
        f"(valid n={valid.sum():,})"
    )


# --------------------------------------------------
# 8. Medicaid capacity QC
# --------------------------------------------------

print("\nMEDICAID CAPACITY TABLE")
print("-" * 60)

print(
    f"Rows: {len(capacity)}"
)

usable_denominators = capacity[
    capacity["medicaid_enrollment"].notna()
    & (
        capacity["medicaid_enrollment"] > 0
    )
].copy()

print(
    f"Usable Medicaid denominators: "
    f"{len(usable_denominators)}"
)

print(
    f"Missing/invalid Medicaid denominators: "
    f"{len(capacity) - len(usable_denominators)}"
)

if len(capacity) != len(usable_denominators):

    print(
        "\nStates without a usable Medicaid denominator:"
    )

    print(
        capacity.loc[
            ~capacity["medicaid_enrollment"].notna()
            | (
                capacity["medicaid_enrollment"] <= 0
            ),
            "LOCATIONSTATE"
        ].tolist()
    )


# Use the same analytic sample for both medians:
# jurisdictions with a usable Medicaid denominator.
median_acceptance = (
    usable_denominators[
        "medicaid_acceptance_pct"
    ]
    .median()
)

median_capacity = (
    usable_denominators[
        "medicaid_accepting_mh_facilities_per_100k_medicaid"
    ]
    .median()
)

print(
    f"Median Medicaid acceptance "
    f"(usable-denominator sample): "
    f"{median_acceptance:.1f}%"
)

print(
    f"Median population-relative capacity "
    f"(usable-denominator sample): "
    f"{median_capacity:.2f}"
)


# --------------------------------------------------
# 9. Arizona capacity QC
# --------------------------------------------------

az_capacity = capacity[
    capacity["LOCATIONSTATE"] == "AZ"
].iloc[0]

print("\nARIZONA CAPACITY")
print("-" * 60)

print(
    f"Medicaid enrollment: "
    f"{az_capacity['medicaid_enrollment']:,.0f}"
)

print(
    f"Total MH facilities: "
    f"{az_capacity['total_mh_facilities']:.0f}"
)

print(
    f"Medicaid-accepting MH facilities: "
    f"{az_capacity['medicaid_facilities']:.0f}"
)

print(
    f"Medicaid acceptance: "
    f"{az_capacity['medicaid_acceptance_pct']:.1f}%"
)

print(
    f"Accepting facilities per 100k Medicaid: "
    f"{az_capacity['medicaid_accepting_mh_facilities_per_100k_medicaid']:.2f}"
)


# --------------------------------------------------
# 10. Final consistency checks
# --------------------------------------------------

print("\nFINAL CONSISTENCY CHECKS")
print("-" * 60)

print(
    f"Expected state/jurisdiction rows: 51"
)

print(
    f"Observed capacity rows: {len(capacity)}"
)

print(
    f"Expected usable denominator rows: 50"
)

print(
    f"Observed usable denominator rows: "
    f"{len(usable_denominators)}"
)

if (
    len(capacity) == 51
    and len(usable_denominators) == 50
):
    print(
        "State-count consistency: PASS"
    )
else:
    print(
        "State-count consistency: REVIEW"
    )


print("\nQC COMPLETE")