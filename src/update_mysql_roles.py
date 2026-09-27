import pandas as pd
import mysql.connector

df = pd.read_csv("data/cleaned/jobs_with_roles.csv")

print(f"Loaded {len(df):,} jobs")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_Password",
    database="Your_DB"
)

cursor = conn.cursor()

print("Connected to MySQL ✅")
print("Updating roles...")

query = """
UPDATE jobs
SET
    normalized_role = %s,
    role_family = %s
WHERE job_id = %s
"""

# Convert to tuples much faster than iterrows()
data = list(
    zip(
        df["normalized_role"],
        df["role_family"],
        df["job_id"]
    )
)

print(f"Prepared {len(data):,} updates")

# Update in batches
batch_size = 1000

for i in range(0, len(data), batch_size):

    batch = data[i:i + batch_size]

    cursor.executemany(query, batch)
    conn.commit()

    print(
        f"Updated {min(i + batch_size, len(data)):,} / {len(data):,}"
    )

print("\nRole update complete! ✅")

cursor.execute("""
    SELECT
        role_family,
        COUNT(*) AS job_count
    FROM jobs
    GROUP BY role_family
    ORDER BY job_count DESC
""")

print("\nMySQL Role Family Distribution:\n")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()

print("\nDone! 🎉")