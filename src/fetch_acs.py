from pathlib import Path
import os

import pandas as pd
import requests
from dotenv import load_dotenv


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load API key
# --------------------------------------------------

load_dotenv(
    PROJECT_ROOT / ".env",
    override=True
)

CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

if not CENSUS_API_KEY:
    raise RuntimeError(
        "CENSUS_API_KEY was not found in .env"
    )


# --------------------------------------------------
# 3. Census ACS 2024 5-year API
# --------------------------------------------------

ACS_URL = (
    "https://api.census.gov/data/2024/acs/acs5"
)


# --------------------------------------------------
# 4. Variables
# --------------------------------------------------

VARIABLES = [
    "NAME",
    "B01003_001E",  # Total population
    "B17001_001E",  # Population for whom poverty status is determined
    "B17001_002E",  # Population below poverty level
    "B19013_001E",  # Median household income
]


# --------------------------------------------------
# 5. Request state-level data
# --------------------------------------------------

params = {
    "get": ",".join(VARIABLES),
    "for": "state:*",
    "key": CENSUS_API_KEY,
}


print("ACS 2024 STATE DATA REQUEST")
print("-" * 50)

response = requests.get(
    ACS_URL,
    params=params,
    timeout=30
)

print(f"HTTP status: {response.status_code}")

response.raise_for_status()


# --------------------------------------------------
# 6. Convert API response to dataframe
# --------------------------------------------------

data = response.json()

header = data[0]
rows = data[1:]

acs = pd.DataFrame(
    rows,
    columns=header
)


print(f"States returned: {len(acs)}")

print("\nRAW ACS DATA")
print("-" * 50)

print(
    acs.head().to_string(index=False)
)


# --------------------------------------------------
# 7. Convert numeric variables
# --------------------------------------------------

numeric_columns = [
    "B01003_001E",
    "B17001_001E",
    "B17001_002E",
    "B19013_001E",
]

for column in numeric_columns:
    acs[column] = pd.to_numeric(
        acs[column],
        errors="coerce"
    )


# --------------------------------------------------
# 8. Create derived measures
# --------------------------------------------------

acs["poverty_rate"] = (
    acs["B17001_002E"]
    / acs["B17001_001E"]
    * 100
).round(2)

acs["total_population"] = acs["B01003_001E"]

acs["median_household_income"] = (
    acs["B19013_001E"]
)


# --------------------------------------------------
# 9. Keep clean analysis columns
# --------------------------------------------------

acs_clean = acs[
    [
        "state",
        "NAME",
        "total_population",
        "poverty_rate",
        "median_household_income",
    ]
].copy()

acs_clean = acs_clean.rename(
    columns={
        "state": "state_fips",
        "NAME": "state_name",
    }
)

acs_clean = acs_clean.sort_values(
    "state_fips"
)


# --------------------------------------------------
# 10. Quality control
# --------------------------------------------------

print("\nACS QUALITY CONTROL")
print("-" * 50)

print(
    f"State records: {len(acs_clean)}"
)

print(
    f"Missing poverty rate: "
    f"{acs_clean['poverty_rate'].isna().sum()}"
)

print(
    f"Missing median income: "
    f"{acs_clean['median_household_income'].isna().sum()}"
)

print(
    f"Duplicate state FIPS: "
    f"{acs_clean['state_fips'].duplicated().sum()}"
)


# --------------------------------------------------
# 11. Save
# --------------------------------------------------

OUTPUT_PATH = (
    OUTPUT_DIR
    / "acs_state_context_2024.csv"
)

acs_clean.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nACS state context saved to:")
print(OUTPUT_PATH)