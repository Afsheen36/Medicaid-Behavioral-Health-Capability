from pathlib import Path
import pandas as pd
from scipy.stats import pearsonr, spearmanr


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024.csv"
)


# --------------------------------------------------
# 2. Load integrated dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("INTEGRATED STATE ANALYSIS")
print("-" * 50)

print(f"States/jurisdictions: {len(df)}")


# --------------------------------------------------
# 3. Define capability measures
# --------------------------------------------------

capabilities = [
    "SETTINGOP",
    "SETTINGDTPH",
    "SETTINGRC",
    "SETTINGIP",
    "MHSUICIDE",
    "SMISEDSUD_MH",
    "PRIMARYCARE"
]


# --------------------------------------------------
# 4. Calculate state-level capability measures
# --------------------------------------------------

nsumhss_path = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nsumhss_mh_2024.csv"
)

nsumhss = pd.read_csv(nsumhss_path)

nsumhss = nsumhss[
    ~nsumhss["LOCATIONSTATE"].isin(["PR", "ZZ"])
].copy()

medicaid = nsumhss[
    nsumhss["REVCHK5_MH"] == 1
].copy()

for variable in capabilities:
    medicaid[variable] = pd.to_numeric(
        medicaid[variable],
        errors="coerce"
    )

state_capability = (
    medicaid
    .groupby("LOCATIONSTATE")[capabilities]
    .mean()
    .mul(100)
    .reset_index()
)


# --------------------------------------------------
# 5. Merge capability with workforce
# --------------------------------------------------

analysis_df = df.merge(
    state_capability,
    on="LOCATIONSTATE",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# 6. Correlation analysis
# --------------------------------------------------

results = []

for capability in capabilities:

    valid = analysis_df[
        [
            "psychiatrists_per_100k",
            capability
        ]
    ].dropna()

    pearson_r, pearson_p = pearsonr(
        valid["psychiatrists_per_100k"],
        valid[capability]
    )

    spearman_rho, spearman_p = spearmanr(
        valid["psychiatrists_per_100k"],
        valid[capability]
    )

    results.append({
        "capability": capability,
        "n_states": len(valid),
        "pearson_r": pearson_r,
        "pearson_p": pearson_p,
        "spearman_rho": spearman_rho,
        "spearman_p": spearman_p
    })


results_df = pd.DataFrame(results)

results_df[
    [
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p"
    ]
] = results_df[
    [
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p"
    ]
].round(3)


# --------------------------------------------------
# 7. Display results
# --------------------------------------------------

print("\nPSYCHIATRIST SUPPLY VS FACILITY CAPABILITY")
print("-" * 70)

print(
    results_df.to_string(index=False)
)


# --------------------------------------------------
# 8. Save results
# --------------------------------------------------

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "tables"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH = (
    RESULTS_DIR
    / "psychiatrist_supply_capability_correlations.csv"
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nResults saved to:")
print(OUTPUT_PATH)


# --------------------------------------------------
# 9. Diagnostic scatterplot:
# Psychiatrist supply vs suicide-related services
# --------------------------------------------------

import matplotlib.pyplot as plt

FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

x = analysis_df["psychiatrists_per_100k"]
y = analysis_df["MHSUICIDE"]

fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(x, y)

# Label every state
for _, row in analysis_df.iterrows():
    ax.annotate(
        row["LOCATIONSTATE"],
        (
            row["psychiatrists_per_100k"],
            row["MHSUICIDE"]
        ),
        xytext=(4, 4),
        textcoords="offset points",
        fontsize=8
    )

ax.set_xlabel("Psychiatrists per 100,000 population, 2023")

ax.set_ylabel(
    "Medicaid-accepting facilities offering "
    "suicide-related services (%)"
)

ax.set_title(
    "Psychiatrist Supply and Suicide-Related "
    "Service Capability by State"
)

ax.grid(alpha=0.25)

plt.tight_layout()

FIGURE_PATH = (
    FIGURES_DIR
    / "psychiatrist_supply_vs_suicide_services.png"
)

plt.savefig(
    FIGURE_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nDiagnostic figure saved to:")
print(FIGURE_PATH)

# --------------------------------------------------
# 10. Sensitivity analysis excluding DC
# --------------------------------------------------

analysis_no_dc = analysis_df[
    analysis_df["LOCATIONSTATE"] != "DC"
].copy()

sensitivity_results = []

for capability in capabilities:

    valid = analysis_no_dc[
        [
            "psychiatrists_per_100k",
            capability
        ]
    ].dropna()

    pearson_r, pearson_p = pearsonr(
        valid["psychiatrists_per_100k"],
        valid[capability]
    )

    spearman_rho, spearman_p = spearmanr(
        valid["psychiatrists_per_100k"],
        valid[capability]
    )

    sensitivity_results.append({
        "capability": capability,
        "n_states": len(valid),
        "pearson_r": pearson_r,
        "pearson_p": pearson_p,
        "spearman_rho": spearman_rho,
        "spearman_p": spearman_p
    })


sensitivity_df = pd.DataFrame(
    sensitivity_results
)

sensitivity_df[
    [
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p"
    ]
] = sensitivity_df[
    [
        "pearson_r",
        "pearson_p",
        "spearman_rho",
        "spearman_p"
    ]
].round(3)


print("\nSENSITIVITY ANALYSIS: EXCLUDING DC")
print("-" * 70)

print(
    sensitivity_df.to_string(index=False)
)


# Save sensitivity results
SENSITIVITY_PATH = (
    RESULTS_DIR
    / "psychiatrist_supply_capability_sensitivity_no_dc.csv"
)

sensitivity_df.to_csv(
    SENSITIVITY_PATH,
    index=False
)

print("\nSensitivity results saved to:")
print(SENSITIVITY_PATH)


# --------------------------------------------------
# 11. Multiple-testing correction
# Benjamini-Hochberg FDR
# --------------------------------------------------

from statsmodels.stats.multitest import multipletests


# Correct Spearman p-values from primary analysis
reject_all, q_all, _, _ = multipletests(
    results_df["spearman_p"],
    alpha=0.05,
    method="fdr_bh"
)

results_df["spearman_fdr_q"] = q_all.round(3)
results_df["spearman_fdr_significant"] = reject_all


# Correct Spearman p-values from sensitivity analysis
reject_no_dc, q_no_dc, _, _ = multipletests(
    sensitivity_df["spearman_p"],
    alpha=0.05,
    method="fdr_bh"
)

sensitivity_df["spearman_fdr_q"] = q_no_dc.round(3)
sensitivity_df["spearman_fdr_significant"] = reject_no_dc


print("\nMULTIPLE-TESTING CORRECTION: ALL 51")
print("-" * 70)

print(
    results_df[
        [
            "capability",
            "spearman_rho",
            "spearman_p",
            "spearman_fdr_q",
            "spearman_fdr_significant"
        ]
    ].to_string(index=False)
)


print("\nMULTIPLE-TESTING CORRECTION: EXCLUDING DC")
print("-" * 70)

print(
    sensitivity_df[
        [
            "capability",
            "spearman_rho",
            "spearman_p",
            "spearman_fdr_q",
            "spearman_fdr_significant"
        ]
    ].to_string(index=False)
)
