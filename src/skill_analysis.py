import pandas as pd

df = pd.read_csv("data/cleaned/jobs_cleaned.csv")

print("Dataset shape:", df.shape)

print("\nTop raw skill entries:")
print(
    df["skills_required"]
    .dropna()
    .value_counts()
    .head(30)
    .to_string()
)

print("\nSkill counts:")
print(df["skills_count"].describe())

print("\nExamples of longer skill entries:")
print(
    df.loc[
        df["skills_required"].str.len() > 100,
        "skills_required"
    ]
    .head(20)
    .to_string(index=False)
)