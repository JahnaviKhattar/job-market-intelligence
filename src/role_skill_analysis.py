import pandas as pd


JOBS_FILE = "data/cleaned/jobs_cleaned.csv"
SKILLS_FILE = "data/cleaned/job_skills.csv"


# Load data
jobs = pd.read_csv(JOBS_FILE)
job_skills = pd.read_csv(SKILLS_FILE)


# Join jobs with extracted skills
merged = job_skills.merge(
    jobs[
        [
            "job_id",
            "role_category",
            "experience_tier",
            "is_fresher_friendly",
            "primary_city",
            "work_mode",
            "salary_disclosed",
            "salary_midpoint_lpa"
        ]
    ],
    on="job_id",
    how="left"
)


# Count skill demand by role
role_skill = (
    merged
    .groupby(["role_category", "skill"])
    .size()
    .reset_index(name="job_count")
)


# Calculate percentage of jobs in each role mentioning the skill
role_totals = (
    jobs
    .groupby("role_category")["job_id"]
    .nunique()
    .reset_index(name="total_jobs")
)


role_skill = role_skill.merge(
    role_totals,
    on="role_category",
    how="left"
)


role_skill["demand_pct"] = (
    role_skill["job_count"] /
    role_skill["total_jobs"] *
    100
)


# Top 10 skills for every role
top_skills = (
    role_skill
    .sort_values(
        ["role_category", "job_count"],
        ascending=[True, False]
    )
    .groupby("role_category")
    .head(10)
)


print("\n===== TOP SKILLS BY ROLE =====\n")

for role in top_skills["role_category"].unique():

    print(f"\n--- {role} ---")

    print(
        top_skills[
            top_skills["role_category"] == role
        ][
            ["skill", "job_count", "demand_pct"]
        ].to_string(index=False)
    )