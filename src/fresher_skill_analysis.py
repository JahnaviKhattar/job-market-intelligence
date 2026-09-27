import pandas as pd


jobs = pd.read_csv("data/cleaned/jobs_cleaned.csv")
skills = pd.read_csv("data/cleaned/job_skills.csv")


# Attach fresher-friendly status to every skill occurrence
merged = skills.merge(
    jobs[["job_id", "is_fresher_friendly"]],
    on="job_id",
    how="left"
)


# Number of jobs in each group
group_totals = (
    jobs.groupby("is_fresher_friendly")["job_id"]
    .nunique()
)


# Count jobs mentioning each skill in each group
skill_counts = (
    merged
    .groupby(["is_fresher_friendly", "skill"])["job_id"]
    .nunique()
    .reset_index(name="job_count")
)


# Convert counts to percentages
skill_counts["demand_pct"] = skill_counts.apply(
    lambda row: (
        row["job_count"] /
        group_totals[row["is_fresher_friendly"]] *
        100
    ),
    axis=1
)


# Pivot into comparison format
comparison = (
    skill_counts
    .pivot(
        index="skill",
        columns="is_fresher_friendly",
        values="demand_pct"
    )
    .fillna(0)
)


comparison.columns = [
    "not_fresher_friendly",
    "fresher_friendly"
]


comparison["difference_pp"] = (
    comparison["fresher_friendly"] -
    comparison["not_fresher_friendly"]
)


# Sort by largest difference
comparison = comparison.sort_values(
    "difference_pp",
    ascending=False
)


print("\n===== FRESHER SKILL COMPARISON =====\n")

print(
    comparison
    .head(20)
    .round(2)
    .to_string()
)