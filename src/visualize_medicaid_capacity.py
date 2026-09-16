from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024_full.csv"
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

df = pd.read_csv(DATA_PATH)


# --------------------------------------------------
# 3. Restrict to usable Medicaid denominators
# --------------------------------------------------

plot_df = df[
    df["medicaid_enrollment"].notna()
    & (df["medicaid_enrollment"] > 0)
].copy()


# --------------------------------------------------
# 4. Verify capacity measure
# --------------------------------------------------

plot_df[
    "medicaid_capacity"
] = (
    plot_df["medicaid_facilities"]
    / plot_df["medicaid_enrollment"]
    * 100000
)


print("MEDICAID CAPACITY VISUALIZATION")
print("-" * 60)

print(
    f"States/jurisdictions plotted: "
    f"{len(plot_df)}"
)


# --------------------------------------------------
# 5. Create figure
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(11, 8)
)

scatter = ax.scatter(
    plot_df["medicaid_acceptance_pct"],
    plot_df["medicaid_capacity"],
    s=(
        plot_df["total_mh_facilities"] ** 0.5
    ) * 20,
    c=plot_df["poverty_rate"],
    alpha=0.72,
    edgecolors="black",
    linewidths=0.5
)


# --------------------------------------------------
# 6. Label selected states
# --------------------------------------------------

states_to_label = [
    "AZ",
    "CA",
    "DC",
    "FL",
    "GA",
    "ME",
    "NY",
    "TX",
    "UT",
    "WY",
]

for _, row in plot_df.iterrows():

    if row["LOCATIONSTATE"] in states_to_label:

        ax.annotate(
            row["LOCATIONSTATE"],
            (
                row["medicaid_acceptance_pct"],
                row["medicaid_capacity"]
            ),
            xytext=(6, 5),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold"
        )


# --------------------------------------------------
# 7. Highlight Arizona
# --------------------------------------------------

az = plot_df[
    plot_df["LOCATIONSTATE"] == "AZ"
].iloc[0]

ax.scatter(
    az["medicaid_acceptance_pct"],
    az["medicaid_capacity"],
    s=260,
    facecolors="none",
    edgecolors="black",
    linewidths=2
)

ax.annotate(
    "Arizona",
    (
        az["medicaid_acceptance_pct"],
        az["medicaid_capacity"]
    ),
    xytext=(12, -18),
    textcoords="offset points",
    fontsize=10,
    fontweight="bold"
)


# --------------------------------------------------
# 8. Add national medians
# --------------------------------------------------

median_acceptance = (
    plot_df["medicaid_acceptance_pct"].median()
)

median_capacity = (
    plot_df["medicaid_capacity"].median()
)

ax.axvline(
    median_acceptance,
    linestyle="--",
    linewidth=1,
    alpha=0.55
)

ax.axhline(
    median_capacity,
    linestyle="--",
    linewidth=1,
    alpha=0.55
)


# --------------------------------------------------
# 9. Labels and title
# --------------------------------------------------

ax.set_xlabel(
    "Mental-health facilities accepting Medicaid (%)",
    fontsize=11
)

ax.set_ylabel(
    "Medicaid-accepting mental-health facilities\n"
    "per 100,000 Medicaid enrollees",
    fontsize=11
)

ax.set_title(
    "Medicaid Participation Does Not Fully Describe "
    "Behavioral Health Capacity",
    fontsize=15,
    pad=14
)

ax.text(
    0.5,
    1.01,
    "State facility participation versus "
    "population-relative infrastructure",
    transform=ax.transAxes,
    ha="center",
    fontsize=10
)

ax.grid(
    alpha=0.15
)


# --------------------------------------------------
# 10. Poverty scale
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
# 11. Figure note
# --------------------------------------------------

fig.text(
    0.5,
    0.015,
    (
        "Bubble size represents the number of N-SUMHSS mental-health "
        "facilities. Dashed lines indicate state medians. "
        "Rhode Island is excluded because the CMS December 2024 "
        "extract does not provide a usable Medicaid enrollment denominator."
    ),
    ha="center",
    fontsize=9
)


plt.tight_layout(
    rect=[0, 0.06, 1, 0.97]
)


# --------------------------------------------------
# 12. Save
# --------------------------------------------------

OUTPUT_PATH = (
    FIGURES_DIR
    / "medicaid_participation_vs_capacity.png"
)

plt.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 13. Console summary
# --------------------------------------------------

print("\nFigure saved to:")
print(OUTPUT_PATH)

print("\nState medians:")

print(
    f"  Medicaid acceptance: "
    f"{median_acceptance:.1f}%"
)

print(
    f"  Accepting facilities per 100k Medicaid: "
    f"{median_capacity:.2f}"
)

print("\nArizona:")

print(
    f"  Medicaid acceptance: "
    f"{az['medicaid_acceptance_pct']:.1f}%"
)

print(
    f"  Accepting facilities per 100k Medicaid: "
    f"{az['medicaid_capacity']:.2f}"
)