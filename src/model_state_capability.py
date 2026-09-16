from pathlib import Path

import pandas as pd
import statsmodels.api as sm


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STATE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "integrated_state_2024_acs.csv"
)

NSUMHSS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nsumhss_mh_2024.csv"
)


# --------------------------------------------------
# 2. Load state context
# --------------------------------------------------

state_df = pd.read_csv(STATE_PATH)

nsumhss = pd.read_csv(
    NSUMHSS_PATH,
    low_memory=False
)


# --------------------------------------------------
# 3. Construct state suicide-service capability
# among Medicaid-accepting facilities
# --------------------------------------------------

nsumhss = nsumhss[
    ~nsumhss["LOCATIONSTATE"].isin(["PR", "ZZ"])
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
        ),
        medicaid_facilities=(
            "MPRID",
            "count"
        )
    )
    .reset_index()
)


# --------------------------------------------------
# 4. Merge outcome with state predictors
# --------------------------------------------------

model_df = state_df.merge(
    state_suicide,
    on="LOCATIONSTATE",
    how="left",
    validate="one_to_one"
)


# --------------------------------------------------
# 5. Prepare predictors
# --------------------------------------------------

predictors = [
    "psychiatrists_per_100k",
    "poverty_rate",
    "median_household_income"
]

analysis_columns = (
    ["LOCATIONSTATE", "suicide_service_pct"]
    + predictors
)

model_df = model_df[
    analysis_columns
].dropna()


print("STATE CAPABILITY MODEL")
print("-" * 60)

print(f"Observations: {len(model_df)}")


# --------------------------------------------------
# 6. Function for OLS model with robust SE
# --------------------------------------------------

def fit_model(data, label):

    X = data[predictors].copy()

    # Scale income to $10,000 units
    X["median_household_income"] = (
        X["median_household_income"] / 10000
    )

    X = sm.add_constant(X)

    y = data["suicide_service_pct"]

    model = sm.OLS(
        y,
        X
    ).fit(
        cov_type="HC3"
    )

    print(f"\n{label}")
    print("-" * 60)

    results = pd.DataFrame({
        "coefficient": model.params,
        "robust_se": model.bse,
        "p_value": model.pvalues,
        "ci_lower": model.conf_int()[0],
        "ci_upper": model.conf_int()[1]
    }).round(3)

    print(results)

    print(
        f"\nR-squared: "
        f"{model.rsquared:.3f}"
    )

    return model, results


# --------------------------------------------------
# 7. Primary model: all 51 jurisdictions
# --------------------------------------------------

model_all, results_all = fit_model(
    model_df,
    "MODEL 1: ALL 51 JURISDICTIONS"
)


# --------------------------------------------------
# 8. Sensitivity model: exclude DC
# --------------------------------------------------

model_no_dc_df = model_df[
    model_df["LOCATIONSTATE"] != "DC"
].copy()

model_no_dc, results_no_dc = fit_model(
    model_no_dc_df,
    "MODEL 2: EXCLUDING DC"
)


# --------------------------------------------------
# 9. Save model results
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

results_all.to_csv(
    RESULTS_DIR
    / "suicide_capability_model_all_states.csv"
)

results_no_dc.to_csv(
    RESULTS_DIR
    / "suicide_capability_model_no_dc.csv"
)

print("\nModel results saved.")