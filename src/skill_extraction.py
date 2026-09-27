import pandas as pd
import re


INPUT_FILE = "data/cleaned/jobs_cleaned.csv"
OUTPUT_FILE = "data/cleaned/job_skills.csv"


# ---------------------------------------
# 1. Load cleaned dataset
# ---------------------------------------

df = pd.read_csv(INPUT_FILE)


# ---------------------------------------
# 2. Canonical skill dictionary
# ---------------------------------------

SKILL_ALIASES = {

    # Programming
    "Python": [
        "python",
        "python development",
        "python programming"
    ],

    "SQL": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "R": [
        " r ",
        "r programming",
        "r language"
    ],

    "C++": [
        "c++"
    ],

    "Java": [
        "java"
    ],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    # Data
    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Tableau": [
        "tableau"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics"
    ],

    "Data Science": [
        "data science"
    ],

    "Data Engineering": [
        "data engineering"
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation"
    ],

    # AI / ML
    "Machine Learning": [
        "machine learning",
        "ml"
    ],

    "Deep Learning": [
        "deep learning"
    ],

    "Artificial Intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "Generative AI": [
        "generative ai",
        "gen ai",
        "genai"
    ],

    "NLP": [
        "natural language processing",
        "nlp"
    ],

    "Computer Vision": [
        "computer vision"
    ],

    "TensorFlow": [
        "tensorflow"
    ],

    "PyTorch": [
        "pytorch"
    ],

    "LangChain": [
        "langchain"
    ],

    # Cloud
    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure",
        "microsoft azure"
    ],

    "GCP": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],

    # Data Engineering / Big Data
    "Spark": [
        "spark",
        "apache spark"
    ],

    "Hadoop": [
        "hadoop"
    ],

    "Hive": [
        "hive"
    ],

    "Airflow": [
        "airflow",
        "apache airflow"
    ],

    "BigQuery": [
        "bigquery",
        "google bigquery"
    ],

    # DevOps
    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "Git": [
        "git",
        "github"
    ],

    # Testing
    "Selenium": [
        "selenium"
    ],

    "API Testing": [
        "api testing"
    ]
}


# ---------------------------------------
# 3. Extract canonical skills
# ---------------------------------------

records = []


for _, row in df.iterrows():

    job_id = row["job_id"]

    skills_text = str(row["skills_required"]).lower()

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias.strip()) + r"(?![a-zA-Z0-9])"

            if re.search(pattern, skills_text):

                records.append({
                    "job_id": job_id,
                    "skill": canonical_skill
                })

                break


# ---------------------------------------
# 4. Create skill dataframe
# ---------------------------------------

job_skills = pd.DataFrame(records)

job_skills = job_skills.drop_duplicates(
    subset=["job_id", "skill"]
)


# ---------------------------------------
# 5. Save
# ---------------------------------------

job_skills.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------
# 6. Summary
# ---------------------------------------

print("Jobs processed:", df["job_id"].nunique())

print("Unique skills found:", job_skills["skill"].nunique())

print("Job-skill relationships:", len(job_skills))

print("\nTop extracted skills:")

print(
    job_skills["skill"]
    .value_counts()
    .head(20)
)