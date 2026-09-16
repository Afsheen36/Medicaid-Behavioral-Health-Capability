from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024_full.csv"
)

NSUMHSS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nsumhss_mh_2024.csv"
)

FIGURES_DIR = (
    PROJECT_ROOT
    / "results"
    / "figures"
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 2. Load data
# --------------------------------------------------

state_df = pd.read_csv(
    STATE_PATH
)

nsumhss = pd.read_csv(
    NSUMHSS_PATH,
    low_memory=False
)


# --------------------------------------------------
# 3. Construct suicide-service capability
# among Medicaid-accepting facilities
# --------------------------------------------------

nsumhss = nsumhss[
    ~nsumhss["LOCATIONSTATE"].isin(
        ["PR", "ZZ"]
    )
].copy()

medicaid = nsumhss[
    nsumhss["REVCHK5_MH"] == 1
].copy()

medicaid["MHSUICIDE"] = pd.to_numeric(
    medicaid["MHSUICIDE"],
    errors="coerce"
)

state_suicide = (
    medicaid
    .groupby("LOCATIONSTATE")
    .agg(
        suicide_service_pct=(
            "MHSUICIDE",
            lambda x: x.mean() * 100
        )
    )
    .reset_index()
)


# --------------------------------------------------
# 4. Merge outcome with state context
# --------------------------------------------------

plot_df = state_df.merge(
    state_suicide,
    on="LOCATIONSTATE",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# 5. Create integrated figure
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(12, 8)
)

# Exclude states without a usable Medicaid
# enrollment denominator from this figure.
plot_df = plot_df[
    plot_df["medicaid_enrollment"].notna()
    & (
        plot_df["medicaid_enrollment"] > 0
    )
].copy()

# Bubble size represents number of
# mental-health facilities.
bubble_size = (
    plot_df["total_mh_facilities"] ** 0.5
) * 18

scatter = ax.scatter(
    plot_df["psychiatrists_per_100k"],
    plot_df["suicide_service_pct"],
    s=bubble_size,
    c=plot_df["poverty_rate"],
    alpha=0.70,
    edgecolors="black",
    linewidths=0.4
)


# --------------------------------------------------
# 6. Label selected states
# --------------------------------------------------

states_to_label = [
    "AZ",
    "CA",
    "DC",
    "MA",
    "MS",
    "NY",
    "RI",
    "TX",
    "UT",
    "VT",
    "WY"
]

for _, row in plot_df.iterrows():

    if row["LOCATIONSTATE"] in states_to_label:

        ax.annotate(
            row["LOCATIONSTATE"],
            (
                row["psychiatrists_per_100k"],
                row["suicide_service_pct"]
            ),
            xytext=(6, 5),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold"
        )


# --------------------------------------------------
# 7. Highlight Arizona
# --------------------------------------------------

az_rows = plot_df[
    plot_df["LOCATIONSTATE"] == "AZ"
]

if not az_rows.empty:

    az = az_rows.iloc[0]

    ax.scatter(
        az["psychiatrists_per_100k"],
        az["suicide_service_pct"],
        s=240,
        facecolors="none",
        edgecolors="black",
        linewidths=2
    )

    ax.annotate(
        "Arizona",
        (
            az["psychiatrists_per_100k"],
            az["suicide_service_pct"]
        ),
        xytext=(12, -18),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold"
    )


# --------------------------------------------------
# 8. Labels and title
# --------------------------------------------------

ax.set_xlabel(
    "Psychiatrists per 100,000 population (AHRF 2023)",
    fontsize=11
)

ax.set_ylabel(
    "Medicaid-accepting mental health facilities\n"
    "offering suicide-related services (%)",
    fontsize=11
)

ax.set_title(
    "Behavioral Health Service Capacity Across U.S. States",
    fontsize=15,
    pad=14
)

ax.text(
    0.5,
    1.01,
    "Workforce supply, facility capability, "
    "and socioeconomic context",
    transform=ax.transAxes,
    ha="center",
    fontsize=10
)

ax.grid(
    alpha=0.18
)


# --------------------------------------------------
# 9. Poverty scale
# --------------------------------------------------

colorbar = plt.colorbar(
    scatter,
    ax=ax,
    pad=0.02
)

colorbar.set_label(
    "ACS 2024 poverty rate (%)",
    fontsize=10
)


# --------------------------------------------------
# 10. Figure note
# --------------------------------------------------

fig.text(
    0.5,
    0.015,
    (
        "Bubble size reflects the number of N-SUMHSS "
        "mental-health facilities. State labels are "
        "shown selectively for readability. "
        "Associations are descriptive and do not imply causation."
    ),
    ha="center",
    fontsize=9
)


plt.tight_layout(
    rect=[0, 0.055, 1, 0.97]
)


# --------------------------------------------------
# 11. Save Figure 1
# --------------------------------------------------

OUTPUT_PATH = (
    FIGURES_DIR
    / "integrated_behavioral_health_capacity.png"
)

plt.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 12. Console confirmation
# --------------------------------------------------

print(
    "INTEGRATED VISUALIZATION"
)

print("-" * 60)

print(
    "Figure saved to:"
)

print(
    OUTPUT_PATH
)

print(
    f"\nStates plotted: "
    f"{len(plot_df)}"
)

print(
    f"States selectively labeled: "
    f"{len(states_to_label)}"
)

if not az_rows.empty:

    print("\nArizona:")

    print(
        f"  Psychiatrists per 100k: "
        f"{az['psychiatrists_per_100k']:.2f}"
    )

    print(
        f"  Suicide-service capability: "
        f"{az['suicide_service_pct']:.1f}%"
    )

    print(
        f"  Poverty rate: "
        f"{az['poverty_rate']:.2f}%"
    )