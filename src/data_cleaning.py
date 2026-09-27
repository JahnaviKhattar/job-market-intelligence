import pandas as pd


# -----------------------------
# 1. Load raw data
# -----------------------------
INPUT_FILE = "data/raw/jobs.csv"
OUTPUT_FILE = "data/cleaned/jobs_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print(f"Original shape: {df.shape}")


# -----------------------------
# 2. Remove exact duplicates
# -----------------------------
before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"Duplicates removed: {before - after}")


# -----------------------------
# 3. Clean column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# -----------------------------
# 4. Clean text columns
# -----------------------------
text_columns = [
    "job_title",
    "company_name",
    "location",
    "primary_city",
    "role_category",
    "experience_raw",
    "salary_raw",
    "skills_required",
    "job_description",
    "work_mode",
    "skill_domain"
]

for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )


# -----------------------------
# 5. Standardize "Not Available"
# -----------------------------
df = df.replace(
    ["Not Available", "not available", "N/A", "NA", ""],
    pd.NA
)


# -----------------------------
# 6. Ensure numeric columns
# -----------------------------
numeric_columns = [
    "company_rating",
    "experience_min_yrs",
    "experience_max_yrs",
    "salary_min_lpa",
    "salary_max_lpa",
    "skills_count",
    "salary_midpoint_lpa",
    "days_since_posted"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# -----------------------------
# 7. Validate salary values
# -----------------------------
invalid_salary = (
    (df["salary_min_lpa"] < 0) |
    (df["salary_max_lpa"] < 0) |
    (df["salary_max_lpa"] < df["salary_min_lpa"])
)

print(f"Invalid salary records: {invalid_salary.sum()}")


# -----------------------------
# 8. Create cleaned-data folder
# -----------------------------
import os

os.makedirs("data/cleaned", exist_ok=True)


# -----------------------------
# 9. Save cleaned dataset
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print(f"Cleaned shape: {df.shape}")
print(f"Saved to: {OUTPUT_FILE}")