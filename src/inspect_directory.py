from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DIRECTORY_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "National Directory SU 2024_Final.xlsx"
)

# Check workbook sheets
excel_file = pd.ExcelFile(DIRECTORY_PATH)

print("NATIONAL DIRECTORY INSPECTION")
print("-" * 40)

print("Sheets:")
print(excel_file.sheet_names)

# Load facility list
df = pd.read_excel(
    DIRECTORY_PATH,
    sheet_name="Facilities List"
)

print(f"\nRows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
for column in df.columns:
    print(f"  {column}")