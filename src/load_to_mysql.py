import pandas as pd
import mysql.connector

# Load cleaned data
job_skills = pd.read_csv("data/cleaned/job_skills.csv")

# Convert missing values to None
job_skills = job_skills.astype(object).where(pd.notna(job_skills), None)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_Password",
    database="Your_Database"
)

cursor = conn.cursor()

# Insert jobs
job_columns = [
    "job_id",
    "job_title",
    "company_name",
    "company_rating",
    "location",
    "scraped_city",
    "role_category",
    "experience_raw",
    "experience_min_yrs",
    "experience_max_yrs",
    "salary_raw",
    "salary_min_lpa",
    "salary_max_lpa",
    "salary_disclosed",
    "skills_required",
    "job_description",
    "work_mode",
    "company_size_bucket",
    "salary_tier",
    "experience_tier",
    "is_senior",
    "primary_city",
    "skill_domain",
    "salary_midpoint_lpa",
    "days_since_posted",
    "is_fresher_friendly",
    "salary_negotiable"
]

jobs = jobs[job_columns]
jobs = jobs.astype(object).where(pd.notna(jobs), None)
placeholders = ", ".join(["%s"] * len(job_columns))
columns_sql = ", ".join(job_columns)

query = f"""
INSERT INTO jobs ({columns_sql})
VALUES ({placeholders})
"""

for row in jobs.itertuples(index=False, name=None):
    cursor.execute(query, row)

conn.commit()

print(f"Inserted {len(jobs)} jobs.")

# Insert job skills
skill_query = """
INSERT INTO job_skills (job_id, skill)
VALUES (%s, %s)
"""

for row in job_skills.itertuples(index=False, name=None):
    cursor.execute(skill_query, row)

conn.commit()

print(f"Inserted {len(job_skills)} job-skill relationships.")

cursor.close()
conn.close()
