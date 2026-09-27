import pandas as pd
from itertools import combinations


df = pd.read_csv("data/cleaned/job_skills.csv")


# Create one row per job with its unique skills
job_skill_groups = (
    df.groupby("job_id")["skill"]
    .apply(set)
)


# Generate pairs of skills within each job
pairs = []

for skills in job_skill_groups:

    for skill_a, skill_b in combinations(sorted(skills), 2):

        pairs.append({
            "skill_1": skill_a,
            "skill_2": skill_b
        })


pairs_df = pd.DataFrame(pairs)


# Count how often each pair occurs
top_pairs = (
    pairs_df
    .value_counts(["skill_1", "skill_2"])
    .reset_index(name="job_count")
    .head(30)
)


print("\n===== TOP SKILL COMBINATIONS =====\n")

print(top_pairs.to_string(index=False))